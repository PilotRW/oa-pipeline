import csv
import re
from io import BytesIO, StringIO

import pandas as pd
from unidecode import unidecode


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
    "product",
    "product code",
    "name",
    "title",
    "prezzo",
    "price",
    "price eur",
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


def clean_header_cell(value) -> str:
    value = unidecode(clean_cell(value))
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def score_header_row(row) -> int:
    values = [
        clean_header_cell(value)
        for value in row
        if clean_header_cell(value)
    ]

    if not values:
        return 0

    score = 0

    cleaned_keywords = {
        clean_header_cell(keyword)
        for keyword in HEADER_KEYWORDS
    }
    for value in values:
        if value in cleaned_keywords:
            score += 2
            continue
        if any(
            value.startswith(f"{keyword} ")
            or value.endswith(f" {keyword}")
            for keyword in cleaned_keywords
        ):
            score += 1

    return score


def detect_excel_header_row(
    content: bytes,
    max_rows: int = 30,
) -> int | None:
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

    return best_row_index if best_score >= 2 else None


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
