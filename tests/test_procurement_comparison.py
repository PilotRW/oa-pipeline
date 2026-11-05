import unittest

from app.services.procurement_comparison_service import (
    compare_product_offers,
    parse_product_list,
    price_candidate,
)


class ProductListParsingTests(unittest.TestCase):
    def test_parses_numbered_products_and_preserves_leading_zeroes(self):
        products, invalid = parse_product_list(
            "1. Armani Code 75 ml — ЕТАН 3614273604833\n"
            "2. Shiseido Cream — ЕТАН 00768614149514"
        )

        self.assertEqual([], invalid)
        self.assertEqual(
            ["3614273604833", "00768614149514"],
            [item["ean"] for item in products],
        )
        self.assertEqual("Armani Code 75 ml", products[0]["title"])

    def test_reports_lines_without_an_ean(self):
        products, invalid = parse_product_list("Product without code")

        self.assertEqual([], products)
        self.assertEqual(1, invalid[0]["line"])

    def test_removes_word_joiners_after_list_number(self):
        products, invalid = parse_product_list(
            "1.\u2060 \u2060Armani Code — ЕТАН 3614273604833"
        )

        self.assertEqual([], invalid)
        self.assertEqual("Armani Code", products[0]["title"])


class ProcurementPricingTests(unittest.TestCase):
    def test_uses_supplier_price_without_vat_adjustment(self):
        result = price_candidate(
            {
                "cost": "10.00",
                "currency": "EUR",
                "vat_rate": "19",
                "prices_include_vat": False,
            },
            "EUR",
        )

        self.assertEqual(10.0, result["source_cost"])
        self.assertTrue(result["comparable"])
        self.assertNotIn("gross_cost", result)
        self.assertNotIn("vat_rate", result)

    def test_selects_lowest_supplier_price(self):
        products = [{"line": 1, "title": "Product", "ean": "4006381333931"}]
        candidates = [
            {
                "ean": "4006381333931",
                "supplier": "lower-price",
                "cost": "9.50",
                "currency": "EUR",
                "vat_rate": "25",
                "prices_include_vat": False,
            },
            {
                "ean": "4006381333931",
                "supplier": "higher-price",
                "cost": "10.00",
                "currency": "EUR",
                "vat_rate": "10",
                "prices_include_vat": False,
            },
        ]

        result = compare_product_offers(products, candidates)[0]

        self.assertEqual("matched", result["status"])
        self.assertEqual("lower-price", result["winner"]["supplier"])
        self.assertEqual(9.5, result["winner"]["source_cost"])

    def test_matches_gtin_14_to_zero_padded_upc(self):
        products = [{"line": 1, "title": "Product", "ean": "00768614149514"}]
        candidates = [
            {
                "ean": "768614149514",
                "supplier": "supplier",
                "cost": "10.00",
                "currency": "EUR",
                "prices_include_vat": True,
            }
        ]

        result = compare_product_offers(products, candidates)[0]

        self.assertEqual("matched", result["status"])
        self.assertEqual("supplier", result["winner"]["supplier"])

    def test_missing_vat_does_not_block_comparison(self):
        products = [{"line": 1, "title": "Product", "ean": "4006381333931"}]
        candidates = [
            {
                "ean": "4006381333931",
                "supplier": "unknown-vat",
                "cost": "1.00",
                "currency": "EUR",
                "prices_include_vat": False,
            }
        ]

        result = compare_product_offers(products, candidates)[0]

        self.assertEqual("matched", result["status"])
        self.assertEqual("unknown-vat", result["winner"]["supplier"])

    def test_purchase_quantity_uses_volume_price(self):
        result = price_candidate(
            {
                "cost": "10.00",
                "price_tiers": [
                    {"min_quantity": 1, "unit_cost": 10.0, "source": "base"},
                    {"min_quantity": 10, "unit_cost": 8.0, "source": "volume"},
                ],
                "currency": "EUR",
                "vat_rate": "20",
                "prices_include_vat": False,
            },
            "EUR",
            purchase_quantity=12,
        )

        self.assertEqual(8.0, result["source_cost"])
        self.assertEqual(10, result["tier_min_quantity"])


if __name__ == "__main__":
    unittest.main()
