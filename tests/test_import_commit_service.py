import unittest
from types import SimpleNamespace

from app.services.import_commit_service import apply_price_tracking


class ImportCommitServiceTests(unittest.TestCase):
    def test_price_tracking_marks_supplier_current(self):
        supplier = SimpleNamespace(
            price_etag=None,
            price_last_modified=None,
            price_content_length=None,
            price_file_hash=None,
            price_data_hash=None,
            price_last_filename=None,
            price_update_status=None,
            price_last_checked_at=None,
            price_last_downloaded_at=None,
            price_last_changed_at=None,
        )

        apply_price_tracking(
            supplier,
            {
                "etag": "abc",
                "last_modified": "20260920214631",
                "content_length": 123,
                "file_hash": "file-hash",
                "data_hash": "data-hash",
                "changed": True,
            },
            "Products_26834.xlsx",
        )

        self.assertEqual("current", supplier.price_update_status)
        self.assertEqual("Products_26834.xlsx", supplier.price_last_filename)
        self.assertEqual("file-hash", supplier.price_file_hash)
        self.assertIsNotNone(supplier.price_last_changed_at)


if __name__ == "__main__":
    unittest.main()
