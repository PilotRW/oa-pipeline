import asyncio
import ftplib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlparse

from app.config.settings import settings
from app.services.supplier_price_common import (
    ALLOWED_PRICE_FILE_EXTENSIONS,
    MAX_PRICE_FILE_BYTES,
    SupplierPriceDownloadError,
    utc_now,
)


def ftp_credentials(hostname: str) -> tuple[str, str]:
    try:
        credential_registry = json.loads(
            settings.SUPPLIER_FTP_CREDENTIALS_JSON or "{}"
        )
    except json.JSONDecodeError as exc:
        raise SupplierPriceDownloadError(
            "Supplier FTP credential registry is invalid JSON"
        ) from exc

    credentials = (
        credential_registry.get(hostname.lower())
        or credential_registry.get("*")
        or {}
    )
    username = credentials.get("username")
    password = credentials.get("password")

    if not username or not password:
        raise SupplierPriceDownloadError(
            f"FTP credentials are not configured for {hostname}"
        )
    return username, password


def ftp_parse_modify(value: str | None) -> datetime | None:
    if not value:
        return None

    raw = value.strip()
    if raw.startswith("213 "):
        raw = raw[4:].strip()
    raw = raw.split(".")[0]

    try:
        parsed = datetime.strptime(raw, "%Y%m%d%H%M%S")
    except ValueError:
        return None
    return parsed.replace(tzinfo=timezone.utc)


def ftp_format_modify(value: datetime | None) -> str | None:
    if not value:
        return None
    return value.astimezone(timezone.utc).strftime("%Y%m%d%H%M%S")


def ftp_safe_name(value: str) -> str:
    name = Path(unquote(value)).name
    if Path(name).suffix.lower() not in ALLOWED_PRICE_FILE_EXTENSIONS:
        raise SupplierPriceDownloadError(
            "FTP price source must point to a CSV or XLSX file"
        )
    return name


def ftp_metadata(
    *,
    source_url: str,
    filename: str,
    size: int | None,
    modified_at: datetime | None,
) -> dict:
    return {
        "etag": None,
        "last_modified": ftp_format_modify(modified_at),
        "content_length": size,
        "content_type": None,
        "resolved_url": source_url,
        "filename": filename,
    }


def ftp_connect(parsed):
    username, password = ftp_credentials(parsed.hostname or "")
    ftp = ftplib.FTP()
    ftp.connect(parsed.hostname, parsed.port or 21, timeout=45)
    ftp.login(username, password)
    ftp.voidcmd("TYPE I")
    return ftp


def ftp_stat_file(
    ftp: ftplib.FTP,
    filename: str,
) -> tuple[int | None, datetime | None]:
    try:
        size = ftp.size(filename)
    except ftplib.all_errors:
        size = None

    try:
        modified_at = ftp_parse_modify(ftp.sendcmd(f"MDTM {filename}"))
    except ftplib.all_errors:
        modified_at = None
    return size, modified_at


def ftp_select_price_file(
    ftp: ftplib.FTP,
    requested_path: str,
) -> tuple[str, int | None, datetime | None]:
    path = unquote(requested_path or "").strip("/")
    if path and Path(path).suffix.lower() in ALLOWED_PRICE_FILE_EXTENSIONS:
        filename = ftp_safe_name(path)
        size, modified_at = ftp_stat_file(ftp, path)
        return path, size, modified_at

    if path:
        ftp.cwd(path)

    try:
        entries = list(ftp.mlsd())
    except ftplib.all_errors:
        entries = [(name, {}) for name in ftp.nlst()]

    candidates = []
    for name, facts in entries:
        if name in {".", ".."}:
            continue
        if Path(name).suffix.lower() not in ALLOWED_PRICE_FILE_EXTENSIONS:
            continue

        size = None
        modified_at = ftp_parse_modify(facts.get("modify"))
        if facts.get("size"):
            try:
                size = int(facts["size"])
            except ValueError:
                pass

        if size is None or modified_at is None:
            stat_size, stat_modified_at = ftp_stat_file(ftp, name)
            size = size if size is not None else stat_size
            modified_at = modified_at or stat_modified_at
        candidates.append((name, size, modified_at))

    if not candidates:
        raise SupplierPriceDownloadError(
            "FTP directory does not contain a CSV or XLSX price file"
        )

    candidates.sort(
        key=lambda item: (
            item[2] or datetime.min.replace(tzinfo=timezone.utc),
            item[1] or 0,
            item[0],
        ),
        reverse=True,
    )
    return candidates[0]


def close_ftp(ftp: ftplib.FTP) -> None:
    try:
        ftp.quit()
    except ftplib.all_errors:
        ftp.close()


def check_supplier_price_ftp_sync(
    url: str,
    *,
    previous_last_modified: str | None = None,
    previous_content_length: int | None = None,
    has_downloaded_file: bool = False,
) -> dict:
    parsed = urlparse(url)
    ftp = ftp_connect(parsed)
    try:
        filename, size, modified_at = ftp_select_price_file(ftp, parsed.path)
        metadata = ftp_metadata(
            source_url=url,
            filename=ftp_safe_name(filename),
            size=size,
            modified_at=modified_at,
        )

        if not has_downloaded_file:
            update_status = "new_available"
        else:
            comparisons = []
            if previous_last_modified and metadata["last_modified"]:
                comparisons.append(
                    previous_last_modified == metadata["last_modified"]
                )
            if (
                previous_content_length is not None
                and metadata["content_length"] is not None
            ):
                comparisons.append(
                    previous_content_length == metadata["content_length"]
                )

            if comparisons and all(comparisons):
                update_status = "no_changes"
            elif comparisons:
                update_status = "new_available"
            else:
                update_status = "verification_required"
    finally:
        close_ftp(ftp)

    return {
        "update_status": update_status,
        "checked_at": utc_now(),
        **metadata,
    }


async def check_supplier_price_ftp(
    url: str,
    *,
    previous_last_modified: str | None = None,
    previous_content_length: int | None = None,
    has_downloaded_file: bool = False,
) -> dict:
    try:
        return await asyncio.to_thread(
            check_supplier_price_ftp_sync,
            url,
            previous_last_modified=previous_last_modified,
            previous_content_length=previous_content_length,
            has_downloaded_file=has_downloaded_file,
        )
    except SupplierPriceDownloadError:
        raise
    except ftplib.all_errors as exc:
        raise SupplierPriceDownloadError(
            f"Could not check supplier price via FTP: {exc}"
        ) from exc


def download_supplier_price_ftp_sync(url: str) -> tuple[bytes, str, dict]:
    parsed = urlparse(url)
    ftp = ftp_connect(parsed)
    try:
        filename, size, modified_at = ftp_select_price_file(ftp, parsed.path)
        if size and size > MAX_PRICE_FILE_BYTES:
            raise SupplierPriceDownloadError(
                "Price file exceeds the 500 MB limit"
            )

        chunks = []
        total_bytes = 0

        def append_chunk(chunk: bytes):
            nonlocal total_bytes
            total_bytes += len(chunk)
            if total_bytes > MAX_PRICE_FILE_BYTES:
                raise SupplierPriceDownloadError(
                    "Price file exceeds the 500 MB limit"
                )
            chunks.append(chunk)

        ftp.retrbinary(f"RETR {filename}", append_chunk)
        content = b"".join(chunks)
        safe_filename = ftp_safe_name(filename)
        metadata = ftp_metadata(
            source_url=url,
            filename=safe_filename,
            size=size or total_bytes,
            modified_at=modified_at,
        )
    finally:
        close_ftp(ftp)

    if not content:
        raise SupplierPriceDownloadError("Supplier price file is empty")
    if content.startswith(b"PK") and not safe_filename.lower().endswith(
        ".xlsx"
    ):
        safe_filename = f"{Path(safe_filename).stem or 'supplier-price'}.xlsx"
    return content, safe_filename, metadata


async def download_supplier_price_ftp(url: str) -> tuple[bytes, str, dict]:
    try:
        return await asyncio.to_thread(download_supplier_price_ftp_sync, url)
    except SupplierPriceDownloadError:
        raise
    except ftplib.all_errors as exc:
        raise SupplierPriceDownloadError(
            f"Could not download supplier price via FTP: {exc}"
        ) from exc
