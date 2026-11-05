import unittest

from app.services.price_tier_service import (
    extract_price_tiers,
    select_price_tier,
)


class PriceTierTests(unittest.TestCase):
    def test_extracts_vedelec_bulk_price_columns(self):
        tiers = extract_price_tiers(
            {
                "MinAmount": "2",
                "price": "12.00",
                "Bulk1Qty": "10",
                "Bulk1Price": "10.50",
                "Bulk2Qty": "25",
                "Bulk2Price": "9,75",
                "Bulk3Qty": "0",
                "Bulk3Price": "0",
            }
        )

        self.assertEqual([2, 10, 25], [tier["min_quantity"] for tier in tiers])
        self.assertEqual([12.0, 10.5, 9.75], [tier["unit_cost"] for tier in tiers])

    def test_selects_highest_eligible_quantity_tier(self):
        tiers = [
            {"min_quantity": 1, "unit_cost": 12.0, "source": "base"},
            {"min_quantity": 10, "unit_cost": 10.5, "source": "volume"},
            {"min_quantity": 25, "unit_cost": 9.75, "source": "volume"},
        ]

        selected, minimum = select_price_tier(tiers, 20)

        self.assertIsNone(minimum)
        self.assertEqual(10, selected["min_quantity"])
        self.assertEqual(10.5, selected["unit_cost"])

    def test_reports_minimum_quantity_when_order_is_too_small(self):
        selected, minimum = select_price_tier(
            [{"min_quantity": 5, "unit_cost": 10.0}],
            2,
        )

        self.assertIsNone(selected)
        self.assertEqual(5, minimum)

    def test_supports_european_thousands_separator_in_tier_price(self):
        tiers = extract_price_tiers(
            {
                "price": "1.499,99 EUR",
                "Bulk1Qty": "10",
                "Bulk1Price": "1.234,56 €",
            }
        )

        self.assertEqual([1499.99, 1234.56], [tier["unit_cost"] for tier in tiers])


if __name__ == "__main__":
    unittest.main()
