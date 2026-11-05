import unittest

from app.models.supplier import Supplier
from app.services.supplier_import_service import reset_supplier_price_tracking


class SupplierImportServiceTests(unittest.TestCase):
    def test_reset_tracking_preserves_source_but_removes_import_baseline(self):
        supplier = Supplier(
            name="supplier",
            price_url="https://example.com/price.csv",
            price_etag="etag",
            price_file_hash="file-hash",
            price_data_hash="data-hash",
            price_last_filename="price.csv",
            price_update_status="current",
        )

        reset_supplier_price_tracking(supplier)

        self.assertEqual(
            "https://example.com/price.csv",
            supplier.price_url,
        )
        self.assertEqual("never_downloaded", supplier.price_update_status)
        self.assertIsNone(supplier.price_file_hash)
        self.assertIsNone(supplier.price_data_hash)
        self.assertIsNone(supplier.price_last_filename)


if __name__ == "__main__":
    unittest.main()
