import csv
from io import BytesIO, StringIO

import pandas as pd


DELIMITERS = [",", ";", "|", "\t"]

ENCODINGS = [
    "utf-8-sig",
    "utf-8",
    "cp1252",
    "latin1",
    "iso-8859-1",
]

HEADER_KEYWORDS = {
    "ean",
    "ean code",
    "barcode",
    "gtin",
    "upc",
    "descrizione",
    "description",
    "product name",
    "name",
    "title",
    "prezzo",
    "price",
    "preis",
    "sku",
    "artnr",
    "moq",
    "stock",
    "bestand",
}


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


def clean_cell(value) -> str:
    if pd.isna(value):
        return ""

    return str(value).strip().lower()


def score_header_row(row) -> int:
    values = [
        clean_cell(value)
        for value in row
        if clean_cell(value)
    ]

    if not values:
        return 0

    score = 0

    for value in values:
        for keyword in HEADER_KEYWORDS:
            if keyword in value:
                score += 1

    return score


def detect_excel_header_row(
    content: bytes,
    max_rows: int = 30,
) -> int:
    preview_df = pd.read_excel(
        BytesIO(content),
        header=None,
        dtype=str,
        engine="openpyxl",
        nrows=max_rows,
    )

    best_row_index = 0
    best_score = 0

    for row_index, row in preview_df.iterrows():
        score = score_header_row(row)

        if score > best_score:
            best_score = score
            best_row_index = row_index

    return best_row_index


def parse_excel(content: bytes) -> pd.DataFrame:
    header_row = detect_excel_header_row(content)

    df = pd.read_excel(
        BytesIO(content),
        header=header_row,
        dtype=str,
        engine="openpyxl",
    )

    df = df.dropna(how="all")

    return df


async def parse_file(file) -> pd.DataFrame:
    content = await file.read()
    return parse_content(
        content=content,
        filename=file.filename,
    )


def parse_content(
    content: bytes,
    filename: str,
) -> pd.DataFrame:
    filename = filename.lower()

    if filename.endswith(".xlsx"):
        return parse_excel(content)

    if filename.endswith(".csv"):
        text = decode_content(content)
        delimiter = detect_delimiter(text)

        return pd.read_csv(
            StringIO(text),
            sep=delimiter,
            dtype=str,
        )

    raise ValueError(f"Unsupported file type: {filename}")
