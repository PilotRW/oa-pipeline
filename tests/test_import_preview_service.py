import csv
import io
import unittest

import pandas as pd

from app.services.import_preview_service import (
    content_hash,
    dataframe_hash,
    export_filename,
    search_dataframe,
    spreadsheet_safe_csv,
)


class ImportPreviewServiceTests(unittest.TestCase):
    def test_export_filename_is_filesystem_safe(self):
        self.assertEqual(
            "supplier-catalog-xlsx-preview",
            export_filename("Supplier catalog.xlsx preview"),
        )

    def test_csv_preserves_identifier_leading_zeroes(self):
        content = spreadsheet_safe_csv(
            pd.DataFrame([{"ean": "0879961008178", "price": 12.5}])
        ).decode("utf-8-sig")
        row = next(csv.DictReader(io.StringIO(content)))

        self.assertEqual('="0879961008178"', row["ean"])
        self.assertEqual("12.5", row["price"])

    def test_search_scans_all_columns_and_clamps_limit(self):
        source = pd.DataFrame(
            [
                {"supplier_sku": "7304-106", "brand": "Razer"},
                {"supplier_sku": "other", "brand": "Makita"},
            ]
        )

        result = search_dataframe(source, "razer", 1000)

        self.assertEqual(1, result["total_matches"])
        self.assertEqual(500, result["limit"])
        self.assertEqual("7304-106", result["rows"][0]["supplier_sku"])

    def test_search_rejects_blank_query(self):
        with self.assertRaisesRegex(ValueError, "Search query is required"):
            search_dataframe(pd.DataFrame([{"ean": "1"}]), " ", 10)

    def test_hashes_are_stable(self):
        source = pd.DataFrame([{"ean": "0879961008178", "price": 12.5}])

        self.assertEqual(dataframe_hash(source), dataframe_hash(source.copy()))
        self.assertEqual(content_hash(b"price"), content_hash(b"price"))


if __name__ == "__main__":
    unittest.main()
