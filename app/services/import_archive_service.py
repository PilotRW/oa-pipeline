from io import BytesIO
from pathlib import PurePosixPath
from zipfile import BadZipFile, ZipFile


SUPPORTED_PRICE_SUFFIXES = {".csv", ".xlsx"}


def safe_member_path(value: str) -> str | None:
    normalized = str(value or "").replace("\\", "/")
    path = PurePosixPath(normalized)
    if path.is_absolute() or ".." in path.parts:
        return None
    if not path.name or path.name.startswith("."):
        return None
    return str(path)


def extract_price_files_from_zip(
    content: bytes,
    archive_name: str,
    *,
    max_files: int,
    max_uncompressed_bytes: int,
) -> tuple[list[tuple[str, bytes]], list[str]]:
    extracted: list[tuple[str, bytes]] = []
    skipped: list[str] = []

    try:
        with ZipFile(BytesIO(content)) as archive:
            members = [item for item in archive.infolist() if not item.is_dir()]
            if len(members) > max_files:
                raise ValueError(
                    f"Archive contains more than {max_files} files"
                )

            supported = []
            total_size = 0
            for member in members:
                member_path = safe_member_path(member.filename)
                display_name = f"{archive_name}/{member.filename}"
                if member_path is None:
                    skipped.append(display_name)
                    continue
                if member.flag_bits & 0x1:
                    raise ValueError(
                        f"Encrypted archive entry is not supported: {member_path}"
                    )
                if PurePosixPath(member_path).suffix.lower() not in SUPPORTED_PRICE_SUFFIXES:
                    skipped.append(f"{archive_name}/{member_path}")
                    continue

                total_size += member.file_size
                if total_size > max_uncompressed_bytes:
                    raise ValueError(
                        "Archive uncompressed size exceeds the configured limit"
                    )
                supported.append((member_path, member))

            if not supported:
                raise ValueError("Archive contains no supported CSV/XLSX files")

            for member_path, member in supported:
                extracted.append(
                    (
                        f"{archive_name}/{member_path}",
                        archive.read(member),
                    )
                )
    except BadZipFile as exc:
        raise ValueError(f"Invalid ZIP archive: {archive_name}") from exc

    return extracted, skipped
