import hashlib

import pandas as pd

from app.ingestion.cleaners import clean_dataframe
from app.ingestion.normalizer import normalize_columns
from app.ingestion.parser import parse_content
from app.services.import_draft_service import (
    apply_import_filters,
    build_quality_report,
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


def combine_import_dataframes(
    files: list[tuple[str, pd.DataFrame, list, list[dict]]],
) -> tuple[pd.DataFrame, list, list[dict], list[str]]:
    if not files:
        raise ValueError("At least one supplier file is required")

    frames: list[pd.DataFrame] = []
    original_columns: list = []
    normalization_report: list[dict] = []
    filenames: list[str] = []

    for filename, df, file_columns, file_report in files:
        safe_filename = str(filename or "supplier-file")
        frame = df.copy()
        frame["source_file"] = safe_filename
        frames.append(frame)
        filenames.append(safe_filename)

        for column in file_columns:
            if column not in original_columns:
                original_columns.append(column)
        normalization_report.extend(
            {**item, "file": safe_filename}
            for item in file_report
        )

    combined = pd.concat(frames, ignore_index=True, sort=False).fillna("")
    return combined, original_columns, normalization_report, filenames


def build_file_diagnostics(
    files: list[tuple[str, pd.DataFrame, list, list[dict]]],
) -> list[dict]:
    diagnostics = []
    for filename, df, _original_columns, report in files:
        quality = build_quality_report(df, report)
        diagnostics.append(
            {
                "filename": filename,
                "rows": len(df),
                "columns": len(df.columns),
                "mapped_columns": len({
                    item.get("mapped_to")
                    for item in report
                    if item.get("mapped_to")
                }),
                "unmapped_columns": len(quality["unmapped_columns"]),
                "missing_ean": quality["missing_ean_count"],
                "invalid_ean": quality["invalid_ean_count"],
                "supplier_code": quality["supplier_code_count"],
                "tester": quality["tester_count"],
                "missing_price": quality["missing_price_count"],
                "duplicate_ean": quality["duplicate_ean_count"],
                "suspicious_price": quality["suspicious_price_count"],
            }
        )
    return diagnostics


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
