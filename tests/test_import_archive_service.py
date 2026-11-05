from io import BytesIO
import unittest
from zipfile import ZipFile

from app.services.import_archive_service import extract_price_files_from_zip


def build_zip(files: dict[str, bytes]) -> bytes:
    output = BytesIO()
    with ZipFile(output, "w") as archive:
        for name, content in files.items():
            archive.writestr(name, content)
    return output.getvalue()


class ImportArchiveServiceTests(unittest.TestCase):
    def test_extracts_multiple_price_files_and_reports_unsupported_entries(self):
        content = build_zip(
            {
                "prices/part-a.csv": b"EAN;Price\n11111111;10\n",
                "prices/part-b.xlsx": b"xlsx-placeholder",
                "README.txt": b"notes",
            }
        )

        extracted, skipped = extract_price_files_from_zip(
            content,
            "prices.zip",
            max_files=10,
            max_uncompressed_bytes=10_000,
        )

        self.assertEqual(
            ["prices.zip/prices/part-a.csv", "prices.zip/prices/part-b.xlsx"],
            [name for name, _ in extracted],
        )
        self.assertEqual(["prices.zip/README.txt"], skipped)

    def test_skips_unsafe_archive_paths(self):
        content = build_zip(
            {
                "../outside.csv": b"EAN;Price\n11111111;10\n",
                "inside.csv": b"EAN;Price\n22222222;20\n",
            }
        )

        extracted, skipped = extract_price_files_from_zip(
            content,
            "prices.zip",
            max_files=10,
            max_uncompressed_bytes=10_000,
        )

        self.assertEqual(["prices.zip/inside.csv"], [name for name, _ in extracted])
        self.assertEqual(["prices.zip/../outside.csv"], skipped)

    def test_rejects_archive_over_uncompressed_size_limit(self):
        content = build_zip({"large.csv": b"x" * 101})

        with self.assertRaisesRegex(ValueError, "uncompressed size"):
            extract_price_files_from_zip(
                content,
                "prices.zip",
                max_files=10,
                max_uncompressed_bytes=100,
            )


if __name__ == "__main__":
    unittest.main()
