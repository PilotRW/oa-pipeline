import unittest
from types import SimpleNamespace

from app.services.amazon_match_filters import (
    external_filter_reasons,
    normalize_filter_terms,
    offer_matches_external_filters,
    skipped_breakdown,
    title_keywords,
)


class AmazonMatchFilterTests(unittest.TestCase):
    def test_terms_support_comma_separated_values(self):
        self.assertEqual(
            ["Apple", "Lenovo", "Razer"],
            normalize_filter_terms(["Razer, Apple", "Lenovo", "Razer"]),
        )

    def test_filter_reasons_explain_every_matching_rule(self):
        offer = SimpleNamespace(
            brand="Apple",
            title="Apple refurbished notebook",
            cost=5,
        )

        reasons = external_filter_reasons(
            offer,
            exclude_brands=["Apple"],
            exclude_title_keywords=["refurbished"],
            min_cost=10,
        )

        self.assertEqual(
            [
                "excluded_brand",
                "excluded_title_keyword",
                "below_min_cost",
            ],
            [reason["reason"] for reason in reasons],
        )
        self.assertFalse(
            offer_matches_external_filters(
                offer,
                exclude_brands=["Apple"],
                min_cost=10,
            )
        )

    def test_breakdown_aggregates_rejections(self):
        candidates = [
            {
                "offer": SimpleNamespace(
                    brand="Apple",
                    title="Notebook",
                    cost=5,
                )
            },
            {
                "offer": SimpleNamespace(
                    brand="Apple",
                    title="Phone",
                    cost=6,
                )
            },
        ]

        breakdown = skipped_breakdown(
            candidates,
            exclude_brands=["Apple"],
            min_cost=10,
        )

        self.assertEqual(2, breakdown[0]["count"])
        self.assertEqual(2, breakdown[1]["count"])

    def test_title_keywords_count_each_word_once_per_title(self):
        keywords = title_keywords(["Razer Razer Keyboard", "Razer Mouse"])
        counts = {item["value"]: item["count"] for item in keywords}

        self.assertEqual(2, counts["razer"])
        self.assertEqual(1, counts["keyboard"])


if __name__ == "__main__":
    unittest.main()
