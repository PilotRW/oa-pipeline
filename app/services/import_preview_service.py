import hashlib

import pandas as pd

from app.ingestion.cleaners import clean_dataframe
from app.ingestion.normalizer import normalize_columns
from app.ingestion.parser import parse_content
from app.services.import_draft_service import (
    apply_import_filters,
    serialize_import_draft,
)


def export_filename(value: str) -> str:
    safe = "".join(
        character.lower() if character.isalnum() else "-"
        for character in value
    )
    safe = "-".join(part for part in safe.split("-") if part)
    return safe or "import-preview"


def spreadsheet_safe_csv(df: pd.DataFrame) -> bytes:
    export_df = df.copy()
    identifier_columns = {"ean", "gtin", "upc", "barcode"}

    for column in export_df.columns:
        if str(column).strip().lower() not in identifier_columns:
            continue
        export_df[column] = export_df[column].apply(
            lambda value: f'="{value}"' if str(value).strip() else ""
        )

    return export_df.to_csv(index=False).encode("utf-8-sig")


def dataframe_hash(df: pd.DataFrame) -> str:
    canonical = df.fillna("").to_csv(index=False, lineterminator="\n")
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def content_hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def search_dataframe(
    df: pd.DataFrame,
    query: str,
    limit: int,
) -> dict:
    needle = query.strip()
    if not needle:
        raise ValueError("Search query is required")

    result_limit = max(1, min(limit, 500))
    mask = pd.Series(False, index=df.index)
    for column in df.columns:
        values = df[column].fillna("").astype(str)
        mask |= values.str.contains(
            needle,
            case=False,
            regex=False,
            na=False,
        )

    matches = df.loc[mask]
    return {
        "query": needle,
        "total_matches": int(len(matches)),
        "limit": result_limit,
        "columns": list(df.columns),
        "rows": matches.head(result_limit).to_dict(orient="records"),
    }


def normalize_import_dataframe(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, list, list[dict]]:
    if df.empty:
        raise ValueError("Uploaded file contains no rows")

    original_columns = list(df.columns)
    normalized, report = normalize_columns(df)
    return clean_dataframe(normalized), original_columns, report


def build_import_dataframe_from_content(
    content: bytes,
    filename: str,
) -> tuple[pd.DataFrame, list, list[dict]]:
    return normalize_import_dataframe(
        parse_content(content=content, filename=filename)
    )


def apply_saved_filter_profile(
    draft: dict,
    filters: dict | None,
) -> dict:
    if not filters:
        return serialize_import_draft(draft)

    filtered_df, filter_summary = apply_import_filters(draft["df"], filters)
    if filtered_df.empty:
        return {
            **serialize_import_draft(draft),
            "saved_filter_warning": (
                "Saved supplier filters excluded all rows and were not applied"
            ),
        }

    draft["confirmed_filters"] = filter_summary["filters"]
    draft["filter_summary"] = filter_summary
    return serialize_import_draft(
        {
            **draft,
            "df": filtered_df,
            "filter_summary": filter_summary,
        }
    )
