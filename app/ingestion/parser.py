import csv
from io import StringIO

import pandas as pd


DELIMITERS = [",", ";", "|", "\t"]

ENCODINGS = [
    "utf-8-sig",
    "utf-8",
    "cp1252",
    "latin1",
    "iso-8859-1",
]


def detect_delimiter(text: str) -> str:
    sample = text[:5000]

    try:
        dialect = csv.Sniffer().sniff(
            sample,
            delimiters=DELIMITERS,
        )
        return dialect.delimiter

    except csv.Error:
        counts = {
            delimiter: sample.count(delimiter)
            for delimiter in DELIMITERS
        }

        return max(counts, key=counts.get)


def decode_content(content: bytes) -> str:

    for encoding in ENCODINGS:
        try:
            return content.decode(encoding)
        except UnicodeDecodeError:
            continue

    return content.decode(
        "utf-8",
        errors="replace",
    )


async def parse_csv(file):
    content = await file.read()

    text = decode_content(content)

    delimiter = detect_delimiter(text)

    df = pd.read_csv(
        StringIO(text),
        sep=delimiter,
        dtype=str,
    )

    return df