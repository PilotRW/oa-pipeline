import unittest
from datetime import datetime, timezone

import httpx

from app.services.supplier_price_service import (
    SupplierPriceDownloadError,
    ftp_parse_modify,
    ftp_select_price_file,
    validate_public_price_url,
)
from app.services.supplier_price_http import (
    response_filename,
    response_metadata,
    update_status_from_metadata,
)


class FakeFtp:
    def __init__(self, entries):
        self.entries = entries
        self.directory = None

    def cwd(self, path):
        self.directory = path

    def mlsd(self):
        return iter(self.entries)

    def size(self, _filename):
        return None

    def sendcmd(self, _command):
        raise RuntimeError("metadata unavailable")


class FtpPriceSelectionTests(unittest.TestCase):
    def test_parse_modify_supports_ftp_response_and_fraction(self):
        expected = datetime(2026, 9, 20, 21, 46, 31, tzinfo=timezone.utc)

        self.assertEqual(expected, ftp_parse_modify("213 20260920214631"))
        self.assertEqual(expected, ftp_parse_modify("20260920214631.912"))

    def test_directory_selects_newest_supported_price_file(self):
        ftp = FakeFtp(
            [
                ("old.csv", {"modify": "20260901080000", "size": "10"}),
                ("notes.txt", {"modify": "20260921100000", "size": "20"}),
                ("Products_26834.xlsx", {"modify": "20260920214631", "size": "30"}),
            ]
        )

        filename, size, modified_at = ftp_select_price_file(ftp, "/")

        self.assertEqual("Products_26834.xlsx", filename)
        self.assertEqual(30, size)
        self.assertEqual(
            datetime(2026, 9, 20, 21, 46, 31, tzinfo=timezone.utc),
            modified_at,
        )

    def test_directory_path_is_selected_before_listing(self):
        ftp = FakeFtp(
            [("stock.csv", {"modify": "20260920214631", "size": "30"})]
        )

        ftp_select_price_file(ftp, "/Stock/")

        self.assertEqual("Stock", ftp.directory)


class PriceUrlValidationTests(unittest.TestCase):
    def test_rejects_credentials_embedded_in_ftp_url(self):
        with self.assertRaises(SupplierPriceDownloadError):
            validate_public_price_url("ftp://user:secret@example.com/file.csv")


class HttpPriceResponseTests(unittest.TestCase):
    def test_filename_prefers_content_disposition(self):
        response = httpx.Response(
            200,
            headers={
                "content-disposition": "attachment; filename=latest-price.csv",
                "content-type": "text/csv",
            },
            request=httpx.Request("GET", "https://example.com/download"),
        )

        self.assertEqual(
            "latest-price.csv",
            response_filename(response, str(response.url)),
        )

    def test_metadata_ignores_invalid_content_length(self):
        response = httpx.Response(
            200,
            headers={"content-length": "unknown", "etag": "abc"},
            request=httpx.Request("GET", "https://example.com/price.csv"),
        )

        metadata = response_metadata(response)

        self.assertIsNone(metadata["content_length"])
        self.assertEqual("abc", metadata["etag"])

    def test_metadata_comparison_detects_changed_file(self):
        metadata = {
            "etag": "new",
            "last_modified": "Mon, 21 Sep 2026 10:00:00 GMT",
            "content_length": 200,
        }

        status = update_status_from_metadata(
            metadata,
            previous_etag="old",
            previous_last_modified="Mon, 20 Sep 2026 10:00:00 GMT",
            previous_content_length=100,
            has_downloaded_file=True,
        )

        self.assertEqual("new_available", status)


if __name__ == "__main__":
    unittest.main()
