import unittest
from io import BytesIO

import pandas as pd

from app.ingestion.cleaners import (
    clean_dataframe,
    clean_ean,
    clean_row_ean,
    clean_price,
    clean_stock,
    clean_vat_rate,
    is_valid_gtin,
)
from app.ingestion.normalizer import (
    normalize_columns,
    score_column,
)
from app.ingestion.parser import detect_excel_header_row


class ColumnNormalizationTests(unittest.TestCase):
    def test_product_feed_columns_use_exact_mappings(self):
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

    def test_new_price_precedes_price_with_row_fallback(self):
        source = pd.DataFrame(
            {
                "EAN": ["4006381333931", "5901234123457"],
                "Price": ["10.00", "12.00"],
                "New Price": ["8.50", ""],
            }
        )

        normalized, _ = normalize_columns(source)
        cleaned = clean_dataframe(normalized)

        self.assertEqual([8.5, 12.0], cleaned["price"].tolist())

    def test_generic_code_is_ean_only_when_values_are_identifiers(self):
        source = pd.DataFrame(
            {
                "CODE": ["194251077161", "194251077215"],
                "Description": ["Lipshine", "Mascara"],
                "Price": ["9.85", "12.50"],
            }
        )

        normalized, _ = normalize_columns(source)

        self.assertIn("ean", normalized.columns)

    def test_product_code_with_valid_upcs_is_inferred_as_ean(self):
        source = pd.DataFrame(
            {
                "PRODUCT CODE": ["020714598976", "020714598983"],
                "DESCRIPTION": ["Skin type 1", "Skin type 2"],
                "PRICE": ["7.84", "7.85"],
            }
        )

        normalized, _ = normalize_columns(source)

        self.assertIn("ean", normalized.columns)

    def test_invalid_numeric_item_codes_are_not_inferred_as_ean(self):
        source = pd.DataFrame(
            {
                "CODE": ["403108811", "403105561"],
                "DESCRIPTION": ["Treatment", "Serum"],
                "PRICE": ["63.37", "33.80"],
            }
        )

        normalized, _ = normalize_columns(source)

        self.assertNotIn("ean", normalized.columns)

    def test_unnamed_numeric_column_is_price_when_no_named_price_exists(self):
        source = pd.DataFrame(
            {
                "EAN": ["773602435760", "773602435746"],
                "DESCRIPTION": ["Brows lingering", "Brows taupe"],
                "Unnamed: 3": ["11.268", "11.268"],
            }
        )

        normalized, _ = normalize_columns(source)

        self.assertIn("price", normalized.columns)

    def test_content_can_override_misleading_header_and_map_unnamed_fields(self):
        source = pd.DataFrame(
            {
                "Unnamed: 0": ["Loewe", "Loewe"],
                "MOQ": ["Loewe", "Loewe"],
                "30000 EUR": ["8426017063081", "8426017063104"],
                "Unnamed: 3": ["001 Man EDP 50ml", "001 Man EDP 100ml"],
                "Unnamed: 4": ["55.88", "78.74"],
            }
        )

        normalized, _ = normalize_columns(source)

        self.assertIn("ean", normalized.columns)
        self.assertIn("title", normalized.columns)
        self.assertIn("price", normalized.columns)

    def test_gtin_validation_checks_the_check_digit(self):
        self.assertTrue(is_valid_gtin("020714598976"))
        self.assertFalse(is_valid_gtin("020714598977"))

    def test_headerless_feed_columns_are_inferred_from_values(self):
        source = pd.DataFrame(
            [
                ["3614272761759", "Lancome perfume 50 ml", "30.66"],
                ["3614272091894", "Lancome perfume 100 ml", "49.23"],
            ]
        )

        normalized, _ = normalize_columns(source)

        self.assertEqual(["ean", "title", "price"], list(normalized.columns))


class ExcelHeaderDetectionTests(unittest.TestCase):
    @staticmethod
    def workbook_bytes(rows) -> bytes:
        output = BytesIO()
        pd.DataFrame(rows).to_excel(
            output,
            index=False,
            header=False,
            engine="openpyxl",
        )
        return output.getvalue()

    def test_prefers_structured_header_over_marketing_text(self):
        content = self.workbook_bytes(
            [
                ["READY STOCK & PRE-ORDER FORM"],
                [],
                ["PRODUCT CODE", "PRODUCT", "BARCODE", "PRICE EUR"],
                ["L003010000", "Cologne", "690251000036", "33"],
            ]
        )

        self.assertEqual(2, detect_excel_header_row(content))

    def test_returns_none_for_headerless_product_rows(self):
        content = self.workbook_bytes(
            [
                ["3614272761759", "Lancome perfume 50 ml", "30.66"],
                ["3614272091894", "Lancome dry skin cream", "49.23"],
            ]
        )

        self.assertIsNone(detect_excel_header_row(content))


class DataCleaningTests(unittest.TestCase):
    def test_duplicate_ean_prefers_valid_identifier(self):
        source = pd.DataFrame(
            [["invalid", "4006381333931", "", "12.50"]],
            columns=["ean", "ean", "price", "price"],
        )

        cleaned = clean_dataframe(source)

        self.assertEqual("4006381333931", cleaned.loc[0, "ean"])
        self.assertEqual(12.5, cleaned.loc[0, "price"])

    def test_clean_dataframe_removes_fully_blank_rows(self):
        source = pd.DataFrame(
            [
                {"ean": "", "title": "", "price": ""},
                {"ean": "4006381333931", "title": "Product", "price": ""},
            ]
        )

        cleaned = clean_dataframe(source)

        self.assertEqual(1, len(cleaned))
        self.assertEqual("4006381333931", cleaned.iloc[0]["ean"])

    def test_clean_dataframe_removes_formula_zero_only_rows(self):
        source = pd.DataFrame(
            [
                {"ean": "", "title": "", "price": "0"},
                {"ean": "4006381333931", "title": "Product", "price": "0"},
            ]
        )

        cleaned = clean_dataframe(source)

        self.assertEqual(1, len(cleaned))
        self.assertEqual("4006381333931", cleaned.iloc[0]["ean"])

    def test_clean_dataframe_removes_section_rows_without_ean_and_price(self):
        source = pd.DataFrame(
            [
                {"ean": "", "title": "FOUNDATION", "price": ""},
                {"ean": "4006381333931", "title": "Product", "price": ""},
                {"ean": "", "title": "Product without EAN", "price": "10"},
            ]
        )

        cleaned = clean_dataframe(source)

        self.assertEqual(2, len(cleaned))

    def test_clean_ean_preserves_leading_zeroes(self):
        self.assertEqual("0879961008178", clean_ean("0879961008178"))
        self.assertEqual("0740617328295", clean_ean("0740617328295.0"))

    def test_clean_ean_recovers_excel_stripped_upc_zero(self):
        self.assertEqual("085805261078", clean_ean("85805261078"))

    def test_clean_ean_recovers_two_stripped_upc_zeroes(self):
        self.assertEqual("008952160100", clean_ean("8952160100"))

    def test_clean_ean_appends_missing_upc_check_digit(self):
        self.assertEqual("602004134318", clean_ean("60200413431"))

    def test_clean_ean_appends_missing_ean_check_digit(self):
        self.assertEqual("3360372058878", clean_ean("336037205887"))

    def test_clean_ean_does_not_pad_short_internal_codes(self):
        self.assertEqual("910037486", clean_ean("910037486"))

    def test_tester_ean_removes_valid_supplier_suffix(self):
        self.assertEqual(
            "708177131977",
            clean_row_ean("7081771319771", "Jurlique *Tester"),
        )

    def test_clean_dataframe_marks_tester_offer_type(self):
        cleaned = clean_dataframe(pd.DataFrame([
            {
                "ean": "708177131977",
                "title": "Jurlique cream *Tester",
                "price": 8,
            },
        ]))

        self.assertEqual("tester", cleaned.iloc[0]["offer_type"])

    def test_non_tester_ean_preserves_supplier_suffix(self):
        self.assertEqual(
            "7081771319771",
            clean_row_ean("7081771319771", "Jurlique retail"),
        )

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

    def test_clean_vat_rate_supports_percent_values(self):
        self.assertEqual(19.0, clean_vat_rate("19%"))
        self.assertEqual(20.5, clean_vat_rate("20,5 %"))

    def test_clean_stock_returns_none_for_blank_database_value(self):
        self.assertIsNone(clean_stock(""))
        self.assertEqual(12, clean_stock("12.0"))


if __name__ == "__main__":
    unittest.main()
