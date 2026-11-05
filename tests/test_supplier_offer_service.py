import unittest
from decimal import Decimal

import pandas as pd

from app.services.supplier_offer_service import json_safe_value, optional_decimal


class SupplierOfferServiceTests(unittest.TestCase):
    def test_optional_decimal_preserves_numeric_values(self):
        self.assertEqual(Decimal("170.25"), optional_decimal("170.25"))

    def test_optional_decimal_rejects_empty_and_invalid_values(self):
        self.assertIsNone(optional_decimal(None))
        self.assertIsNone(optional_decimal(""))
        self.assertIsNone(optional_decimal("not-a-price"))

    def test_json_safe_value_replaces_non_finite_values_recursively(self):
        result = json_safe_value({
            "lead_time": float("nan"),
            "nested": [float("inf"), pd.NA, Decimal("4.75")],
        })

        self.assertEqual(
            {
                "lead_time": None,
                "nested": [None, None, "4.75"],
            },
            result,
        )


if __name__ == "__main__":
    unittest.main()
