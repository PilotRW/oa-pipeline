import unittest

import pandas as pd

from app.services.import_filter_service import (
    apply_import_filters,
    build_filter_suggestions,
    build_quality_report,
)


class ImportFilterServiceTests(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame(
            [
                {
                    "ean": "0879961008178",
                    "brand": "Razer",
                    "title": "Razer keyboard new",
                    "price": 50,
                },
                {
                    "ean": "0740617328295",
                    "brand": "Kingston",
                    "title": "Kingston SSD refurbished",
                    "price": 25,
                },
                {
                    "ean": "",
                    "brand": "be quiet!",
                    "title": "be quiet! fan",
                    "price": 8,
                },
            ]
        )

    def test_include_brand_price_and_condition_filters_compose(self):
        filtered, summary = apply_import_filters(
            self.df,
            {
                "brand_filter_mode": "include",
                "included_brands": ["Razer", "Kingston"],
                "exclude_non_new": True,
                "min_price": 10,
            },
        )

        self.assertEqual(["Razer"], filtered["brand"].tolist())
        self.assertEqual(1, summary["rows_after"])
        self.assertEqual(2, summary["rows_excluded"])

    def test_suggestions_include_all_unique_brands(self):
        suggestions = build_filter_suggestions(self.df)

        self.assertEqual(3, suggestions["brand_total_unique"])
        self.assertEqual(3, len(suggestions["brands"]))
        self.assertEqual(1, suggestions["missing_ean_count"])
        self.assertEqual(1, suggestions["non_new_count"])

    def test_quality_report_detects_missing_identifiers(self):
        report = build_quality_report(self.df, [])

        self.assertEqual(1, report["missing_ean_count"])
        self.assertEqual(0, report["invalid_ean_count"])
        self.assertEqual(0, report["missing_price_count"])

    def test_quality_report_detects_invalid_ean(self):
        source = pd.DataFrame(
            [
                {"ean": "4006381333931", "price": 10},
                {"ean": "4006381333932", "price": 10},
            ]
        )

        report = build_quality_report(source, [])

        self.assertEqual(1, report["invalid_ean_count"])

    def test_quality_report_separates_supplier_codes_from_invalid_gtin(self):
        source = pd.DataFrame(
            [
                {"ean": "99006108", "price": 10},
                {"ean": "4006381333932", "price": 10},
            ]
        )

        report = build_quality_report(source, [])

        self.assertEqual(1, report["supplier_code_count"])
        self.assertEqual(1, report["invalid_ean_count"])

    def test_non_gtin_length_is_reported_as_supplier_code(self):
        report = build_quality_report(
            pd.DataFrame([{"ean": "634349749", "price": 10}]),
            [],
        )

        self.assertEqual(1, report["supplier_code_count"])
        self.assertEqual(0, report["invalid_ean_count"])

    def test_tester_rows_are_always_excluded_and_marked(self):
        source = pd.DataFrame(
            [
                {"ean": "4006381333931", "title": "Retail", "price": 10},
                {
                    "ean": "708177131977",
                    "title": "Jurlique cream *Tester",
                    "price": 8,
                },
            ]
        )

        filtered, summary = apply_import_filters(source, {})
        report = build_quality_report(source, [])

        self.assertEqual(["Retail"], filtered["title"].tolist())
        self.assertEqual(1, summary["tester_rows_skipped"])
        self.assertEqual(1, report["tester_count"])


if __name__ == "__main__":
    unittest.main()
