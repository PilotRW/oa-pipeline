import unittest

from app.services.ingestion_service import column_mapping_from_report


class ColumnMappingPersistenceTests(unittest.TestCase):
    def test_numeric_headerless_column_name_is_saved_as_text(self):
        mapping = column_mapping_from_report(
            21,
            {
                "column": 0,
                "mapped_to": "ean",
                "confidence": 95,
            },
        )

        self.assertEqual("0", mapping.source_column)
        self.assertEqual("ean", mapping.target_column)


if __name__ == "__main__":
    unittest.main()
