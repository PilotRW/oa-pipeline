import unittest
from io import BytesIO
from zipfile import ZipFile

from app.services.supply_channel_service import (
    infer_supply_channel,
    validate_supply_channel_assignments,
)


def workbook_bytes(text: str) -> bytes:
    buffer = BytesIO()
    with ZipFile(buffer, "w") as archive:
        archive.writestr(
            "xl/sharedStrings.xml",
            f"<sst><si><t>{text}</t></si></sst>",
        )
    return buffer.getvalue()


class SupplyChannelServiceTests(unittest.TestCase):
    def test_detects_incoming_and_lead_time(self):
        result = infer_supply_channel(
            "SKUNDYS INCOMING STOCKLIST.xlsx",
            workbook_bytes("1-2 weeks Leadtime"),
        )

        self.assertEqual("incoming", result["channel"])
        self.assertEqual(7, result["lead_time_min_days"])
        self.assertEqual(14, result["lead_time_max_days"])

    def test_detects_preorder_and_lead_time(self):
        result = infer_supply_channel(
            "SKUNDYS PREORDER STOCKLIST.xlsx",
            workbook_bytes("4-6 weeks Leadtime"),
        )

        self.assertEqual("preorder", result["channel"])
        self.assertEqual(28, result["lead_time_min_days"])
        self.assertEqual(42, result["lead_time_max_days"])

    def test_detects_immediately_available_stock(self):
        result = infer_supply_channel(
            "SKUNDYS STOCKLIST.xlsx",
            workbook_bytes(
                "Goods in stock available for immediate delivery"
            ),
        )

        self.assertEqual("stock", result["channel"])
        self.assertEqual(0, result["lead_time_min_days"])
        self.assertEqual(0, result["lead_time_max_days"])

    def test_requires_confirmation_for_every_file(self):
        with self.assertRaisesRegex(ValueError, "PREORDER"):
            validate_supply_channel_assignments(
                ["STOCK.xlsx", "PREORDER.xlsx"],
                {"STOCK.xlsx": "stock"},
            )

    def test_rejects_unknown_category(self):
        with self.assertRaisesRegex(ValueError, "stock, incoming"):
            validate_supply_channel_assignments(
                ["STOCK.xlsx"],
                {"STOCK.xlsx": "later"},
            )


if __name__ == "__main__":
    unittest.main()
