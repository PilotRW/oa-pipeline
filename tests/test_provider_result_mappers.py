import unittest
from types import SimpleNamespace

from app.services.provider_result_mappers import (
    apply_keepa_metric_result,
    apply_market_snapshot_result,
    apply_presence_result,
    mock_amazon_presence,
)


class ProviderResultMapperTests(unittest.TestCase):
    def test_market_snapshot_mapping_clears_old_error(self):
        snapshot = SimpleNamespace(error_message="old")
        apply_market_snapshot_result(
            snapshot,
            {
                "marketplace": "DE",
                "buy_box_price": 99.99,
                "snapshot_source": "keepa_real",
            },
        )

        self.assertEqual("DE", snapshot.marketplace)
        self.assertEqual(99.99, snapshot.buy_box_price)
        self.assertIsNone(snapshot.error_message)

    def test_keepa_mapping_uses_marketplace_currency_fallback(self):
        metric = SimpleNamespace()
        apply_keepa_metric_result(
            metric,
            {
                "buy_box_price": 25,
                "currency": None,
                "sales_rank": 100,
                "amazon_in_stock": False,
                "estimated_monthly_sales": 10,
                "raw_data": {"source": "keepa_real"},
            },
            "EUR",
        )

        self.assertEqual("EUR", metric.currency)
        self.assertEqual("completed", metric.data_status)

    def test_presence_mapping_records_timestamp(self):
        check = SimpleNamespace()
        apply_presence_result(
            check,
            amazon_present=True,
            data_source="keepa_real",
            marketplace="DE",
            raw_data={},
        )

        self.assertTrue(check.amazon_present)
        self.assertIsNotNone(check.checked_at)

    def test_mock_presence_is_deterministic(self):
        self.assertEqual(
            mock_amazon_presence("B000TEST01"),
            mock_amazon_presence("B000TEST01"),
        )


if __name__ == "__main__":
    unittest.main()
