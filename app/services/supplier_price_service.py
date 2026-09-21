from urllib.parse import urlparse

from app.services.supplier_price_common import (
    SupplierPriceDownloadError,
    validate_public_price_url,
)
from app.services.supplier_price_ftp import (
    check_supplier_price_ftp,
    download_supplier_price_ftp,
    ftp_parse_modify,
    ftp_select_price_file,
)
from app.services.supplier_price_http import (
    check_supplier_price_http,
    download_supplier_price_http,
)


async def check_supplier_price(
    url: str,
    *,
    previous_etag: str | None = None,
    previous_last_modified: str | None = None,
    previous_content_length: int | None = None,
    has_downloaded_file: bool = False,
) -> dict:
    validated_url = validate_public_price_url(url)
    if urlparse(validated_url).scheme == "ftp":
        return await check_supplier_price_ftp(
            validated_url,
            previous_last_modified=previous_last_modified,
            previous_content_length=previous_content_length,
            has_downloaded_file=has_downloaded_file,
        )

    return await check_supplier_price_http(
        validated_url,
        previous_etag=previous_etag,
        previous_last_modified=previous_last_modified,
        previous_content_length=previous_content_length,
        has_downloaded_file=has_downloaded_file,
    )


async def download_supplier_price(url: str) -> tuple[bytes, str, dict]:
    validated_url = validate_public_price_url(url)
    if urlparse(validated_url).scheme == "ftp":
        return await download_supplier_price_ftp(validated_url)
    return await download_supplier_price_http(validated_url)


__all__ = [
    "SupplierPriceDownloadError",
    "check_supplier_price",
    "download_supplier_price",
    "ftp_parse_modify",
    "ftp_select_price_file",
    "validate_public_price_url",
]
