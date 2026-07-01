import hashlib

from app.ingestion.cleaners import clean_dataframe
from app.ingestion.normalizer import normalize_columns
from app.ingestion.parser import parse_content


def dataframe_hash(df) -> str:
    canonical = df.fillna("").to_csv(
        index=False,
        lineterminator="\n",
    )
    return hashlib.sha256(
        canonical.encode("utf-8")
    ).hexdigest()


def build_import_dataframe_from_content(
    content: bytes,
    filename: str,
):
    df = parse_content(
        content=content,
        filename=filename,
    )

    if df.empty:
        raise ValueError("Uploaded file contains no rows")

    original_columns = list(df.columns)
    df, normalization_report = normalize_columns(df)
    df = clean_dataframe(df)

    return df, original_columns, normalization_report


def price_file_fingerprint(
    content: bytes,
    filename: str,
) -> dict:
    df, _original_columns, _normalization_report = (
        build_import_dataframe_from_content(
            content=content,
            filename=filename,
        )
    )

    return {
        "file_hash": hashlib.sha256(content).hexdigest(),
        "data_hash": dataframe_hash(df),
        "row_count": len(df),
    }
