import re
from pathlib import Path
from urllib.parse import unquote, urlparse

import httpx

from app.services.supplier_price_common import (
    ALLOWED_PRICE_FILE_EXTENSIONS,
    MAX_PRICE_FILE_BYTES,
    SupplierPriceDownloadError,
    utc_now,
    validate_public_price_url,
)


def response_filename(response: httpx.Response, source_url: str) -> str:
    disposition = response.headers.get("content-disposition", "")
    encoded_match = re.search(
        r"filename\*=UTF-8''([^;]+)",
        disposition,
        flags=re.IGNORECASE,
    )
    plain_match = re.search(
        r'filename="?([^";]+)"?',
        disposition,
        flags=re.IGNORECASE,
    )

    if encoded_match:
        filename = unquote(encoded_match.group(1))
    elif plain_match:
        filename = plain_match.group(1).strip()
    else:
        filename = Path(unquote(urlparse(source_url).path)).name

    if Path(filename).suffix.lower() in ALLOWED_PRICE_FILE_EXTENSIONS:
        return filename

    content_type = response.headers.get("content-type", "").lower()
    if "spreadsheet" in content_type or "excel" in content_type:
        return f"{filename or 'supplier-price'}.xlsx"
    if any(
        value in content_type
        for value in ("csv", "text/plain", "octet-stream")
    ):
        return f"{filename or 'supplier-price'}.csv"

    raise SupplierPriceDownloadError(
        "Price URL must return a CSV or XLSX file"
    )


def response_metadata(response: httpx.Response) -> dict:
    content_length = response.headers.get("content-length")
    try:
        parsed_length = int(content_length) if content_length else None
    except ValueError:
        parsed_length = None

    return {
        "etag": response.headers.get("etag"),
        "last_modified": response.headers.get("last-modified"),
        "content_length": parsed_length,
        "content_type": response.headers.get("content-type"),
        "resolved_url": str(response.url),
    }


async def send_with_public_redirects(
    client: httpx.AsyncClient,
    method: str,
    url: str,
    headers: dict | None = None,
) -> httpx.Response:
    current_url = validate_public_price_url(url)

    for _redirect in range(6):
        current_url = validate_public_price_url(current_url)
        request = client.build_request(method, current_url, headers=headers)
        response = await client.send(request, stream=True)
        if not response.is_redirect:
            return response

        location = response.headers.get("location")
        next_url = str(response.url.join(location)) if location else None
        await response.aclose()
        if not next_url:
            raise SupplierPriceDownloadError(
                "Price URL returned an invalid redirect"
            )
        current_url = next_url

    raise SupplierPriceDownloadError("Price URL has too many redirects")


def update_status_from_metadata(
    metadata: dict,
    *,
    previous_etag: str | None,
    previous_last_modified: str | None,
    previous_content_length: int | None,
    has_downloaded_file: bool,
) -> str:
    if not has_downloaded_file:
        return "new_available"

    comparisons = []
    if previous_etag and metadata["etag"]:
        comparisons.append(previous_etag == metadata["etag"])
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

    if comparisons and not all(comparisons):
        return "new_available"
    if comparisons and (metadata["etag"] or metadata["last_modified"]):
        return "no_changes"
    return "verification_required"


async def check_supplier_price_http(
    url: str,
    *,
    previous_etag: str | None = None,
    previous_last_modified: str | None = None,
    previous_content_length: int | None = None,
    has_downloaded_file: bool = False,
) -> dict:
    timeout = httpx.Timeout(connect=20, read=30, write=20, pool=20)
    headers = {}
    if previous_etag:
        headers["If-None-Match"] = previous_etag
    if previous_last_modified:
        headers["If-Modified-Since"] = previous_last_modified

    try:
        async with httpx.AsyncClient(
            follow_redirects=False,
            timeout=timeout,
        ) as client:
            response = await send_with_public_redirects(
                client,
                "HEAD",
                url,
                headers=headers,
            )
            if response.status_code in {405, 501}:
                await response.aclose()
                response = await send_with_public_redirects(
                    client,
                    "GET",
                    url,
                    headers=headers,
                )

            try:
                metadata = response_metadata(response)
                if response.status_code == 304:
                    update_status = "no_changes"
                else:
                    response.raise_for_status()
                    update_status = update_status_from_metadata(
                        metadata,
                        previous_etag=previous_etag,
                        previous_last_modified=previous_last_modified,
                        previous_content_length=previous_content_length,
                        has_downloaded_file=has_downloaded_file,
                    )
            finally:
                await response.aclose()
    except SupplierPriceDownloadError:
        raise
    except httpx.HTTPError as exc:
        raise SupplierPriceDownloadError(
            f"Could not check supplier price: {exc}"
        ) from exc

    return {
        "update_status": update_status,
        "checked_at": utc_now(),
        **metadata,
    }


async def download_supplier_price_http(url: str) -> tuple[bytes, str, dict]:
    timeout = httpx.Timeout(connect=20, read=180, write=20, pool=20)
    try:
        async with httpx.AsyncClient(
            follow_redirects=False,
            timeout=timeout,
        ) as client:
            response = await send_with_public_redirects(client, "GET", url)
            try:
                response.raise_for_status()
                metadata = response_metadata(response)
                content_length = metadata["content_length"]
                if content_length and content_length > MAX_PRICE_FILE_BYTES:
                    raise SupplierPriceDownloadError(
                        "Price file exceeds the 500 MB limit"
                    )

                chunks = []
                total_bytes = 0
                async for chunk in response.aiter_bytes():
                    total_bytes += len(chunk)
                    if total_bytes > MAX_PRICE_FILE_BYTES:
                        raise SupplierPriceDownloadError(
                            "Price file exceeds the 500 MB limit"
                        )
                    chunks.append(chunk)

                content = b"".join(chunks)
                filename = response_filename(response, str(response.url))
                if content.startswith(b"PK") and not filename.lower().endswith(
                    ".xlsx"
                ):
                    filename = (
                        f"{Path(filename).stem or 'supplier-price'}.xlsx"
                    )
            finally:
                await response.aclose()
    except SupplierPriceDownloadError:
        raise
    except httpx.HTTPError as exc:
        raise SupplierPriceDownloadError(
            f"Could not download supplier price: {exc}"
        ) from exc

    if not content:
        raise SupplierPriceDownloadError("Supplier price file is empty")
    return content, filename, metadata
