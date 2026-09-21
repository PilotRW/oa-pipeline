import ipaddress
import socket
from datetime import datetime, timezone
from urllib.parse import urlparse


MAX_PRICE_FILE_BYTES = 500 * 1024 * 1024
ALLOWED_PRICE_FILE_EXTENSIONS = {".csv", ".xlsx"}


class SupplierPriceDownloadError(ValueError):
    pass


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def validate_public_host(hostname: str, port: int) -> None:
    try:
        addresses = {
            result[4][0]
            for result in socket.getaddrinfo(
                hostname,
                port,
                type=socket.SOCK_STREAM,
            )
        }
    except socket.gaierror as exc:
        raise SupplierPriceDownloadError(
            "Price URL host could not be resolved"
        ) from exc

    for address in addresses:
        if not ipaddress.ip_address(address).is_global:
            raise SupplierPriceDownloadError(
                "Price URL must point to a public host"
            )


def validate_public_price_url(value: str) -> str:
    url = str(value or "").strip()
    parsed = urlparse(url)

    if parsed.scheme not in {"http", "https", "ftp"} or not parsed.hostname:
        raise SupplierPriceDownloadError(
            "Price URL must use http, https, or ftp"
        )

    if parsed.scheme == "ftp" and (parsed.username or parsed.password):
        raise SupplierPriceDownloadError(
            "FTP credentials must be configured via environment variables"
        )

    default_port = {"http": 80, "https": 443, "ftp": 21}[parsed.scheme]
    validate_public_host(parsed.hostname, parsed.port or default_port)
    return url
