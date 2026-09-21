import unittest

import pandas as pd

from app.ingestion.cleaners import clean_dataframe, clean_ean, clean_price
from app.ingestion.normalizer import normalize_columns, score_column


class ColumnNormalizationTests(unittest.TestCase):
    def test_vedelec_columns_use_exact_mappings(self):
        expected = {
            "ProductID": "supplier_sku",
            "ProductDesc": "title",
            "CostPriceExclVat": "price",
            "VAT": "vat_rate",
            "Barcode": "ean",
            "Barcode2": "ean",
            "GTIN Code": "ean",
        }

        for source, target in expected.items():
            with self.subTest(source=source):
                result = score_column(source)
                self.assertEqual(target, result["mapped_to"])
                self.assertEqual(100, result["confidence"])

    def test_normalization_keeps_duplicate_canonical_columns(self):
        source = pd.DataFrame(
            [["123", "4006381333931", "9.99", "19"]],
            columns=["ProductID", "Barcode", "CostPriceExclVat", "VAT"],
        )

        normalized, _ = normalize_columns(source)

        self.assertEqual(
            ["supplier_sku", "ean", "price", "vat_rate"],
            list(normalized.columns),
        )


class DataCleaningTests(unittest.TestCase):
    def test_duplicate_ean_prefers_valid_identifier(self):
        source = pd.DataFrame(
            [["invalid", "4006381333931", "", "12.50"]],
            columns=["ean", "ean", "price", "price"],
        )

        cleaned = clean_dataframe(source)

        self.assertEqual("4006381333931", cleaned.loc[0, "ean"])
        self.assertEqual(12.5, cleaned.loc[0, "price"])

    def test_clean_ean_preserves_leading_zeroes(self):
        self.assertEqual("0879961008178", clean_ean("0879961008178"))
        self.assertEqual("0740617328295", clean_ean("0740617328295.0"))

    def test_clean_price_supports_common_european_formats(self):
        cases = {
            "1.234,56 EUR": 1234.56,
            "1,234.56": 1234.56,
            "12,50 EUR": 12.5,
            "9.99": 9.99,
        }

        for value, expected in cases.items():
            with self.subTest(value=value):
                self.assertEqual(expected, clean_price(value))


if __name__ == "__main__":
    unittest.main()
