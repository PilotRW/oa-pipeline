from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pandas as pd


IMPORT_DRAFT_TTL = timedelta(minutes=30)

_drafts: dict[str, dict] = {}

WEAK_MAPPING_CONFIDENCE = 90
SUSPICIOUS_LOW_PRICE = 0.01
SUSPICIOUS_HIGH_PRICE = 10000


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _cleanup_expired_drafts() -> None:
    cutoff = _now()
    expired_tokens = [
        token
        for token, draft in _drafts.items()
        if draft["expires_at"] <= cutoff
    ]

    for token in expired_tokens:
        _drafts.pop(token, None)


def create_import_draft(
    supplier_name: str,
    filename: str,
    df: pd.DataFrame,
    original_columns: list,
    normalization_report: list[dict],
) -> dict:
    _cleanup_expired_drafts()

    token = uuid4().hex
    expires_at = _now() + IMPORT_DRAFT_TTL

    _drafts[token] = {
        "token": token,
        "supplier_name": supplier_name,
        "filename": filename,
        "df": df.copy(),
        "original_columns": list(original_columns),
        "normalization_report": normalization_report,
        "quality_report": build_quality_report(
            df=df,
            normalization_report=normalization_report,
        ),
        "expires_at": expires_at,
    }

    return _drafts[token]


def get_import_draft(token: str) -> dict | None:
    _cleanup_expired_drafts()
    return _drafts.get(token)


def consume_import_draft(token: str) -> dict | None:
    _cleanup_expired_drafts()
    return _drafts.pop(token, None)


def _missing_count(df: pd.DataFrame, column: str) -> int:
    if column not in df.columns:
        return len(df)

    return int((df[column].astype(str).str.strip() == "").sum())


def _examples(df: pd.DataFrame, mask, columns: list[str], limit: int = 5) -> list[dict]:
    available_columns = [
        column
        for column in columns
        if column in df.columns
    ]

    if not available_columns:
        return []

    return df.loc[mask, available_columns].head(limit).to_dict(orient="records")


def build_quality_report(
    df: pd.DataFrame,
    normalization_report: list[dict],
) -> dict:
    report = {
        "total_rows": len(df),
        "missing_ean_count": _missing_count(df, "ean"),
        "missing_price_count": _missing_count(df, "price"),
        "duplicate_ean_count": 0,
        "suspicious_price_count": 0,
        "unmapped_columns": [],
        "weak_mappings": [],
        "examples": {
            "missing_ean": [],
            "missing_price": [],
            "duplicate_ean": [],
            "suspicious_price": [],
        },
    }

    if "ean" in df.columns:
        ean = df["ean"].astype(str).str.strip()
        present_ean = ean != ""
        duplicate_ean_mask = present_ean & ean.duplicated(keep=False)
        report["duplicate_ean_count"] = int(duplicate_ean_mask.sum())
        report["examples"]["duplicate_ean"] = _examples(
            df,
            duplicate_ean_mask,
            ["ean", "brand", "title", "price", "stock"],
        )
        report["examples"]["missing_ean"] = _examples(
            df,
            ~present_ean,
            ["brand", "title", "price", "stock"],
        )

    if "price" in df.columns:
        numeric_price = pd.to_numeric(df["price"], errors="coerce")
        missing_price_mask = numeric_price.isna()
        suspicious_price_mask = (
            numeric_price.notna()
            & (
                (numeric_price < SUSPICIOUS_LOW_PRICE)
                | (numeric_price > SUSPICIOUS_HIGH_PRICE)
            )
        )
        report["suspicious_price_count"] = int(suspicious_price_mask.sum())
        report["examples"]["missing_price"] = _examples(
            df,
            missing_price_mask,
            ["ean", "brand", "title", "stock"],
        )
        report["examples"]["suspicious_price"] = _examples(
            df,
            suspicious_price_mask,
            ["ean", "brand", "title", "price", "stock"],
        )

    for item in normalization_report:
        if not item.get("mapped_to"):
            report["unmapped_columns"].append(item["column"])
            continue

        if item.get("confidence", 0) < WEAK_MAPPING_CONFIDENCE:
            report["weak_mappings"].append(
                {
                    "column": item["column"],
                    "mapped_to": item["mapped_to"],
                    "confidence": item["confidence"],
                }
            )

    return report


def serialize_import_draft(draft: dict, preview_rows: int = 10) -> dict:
    df = draft["df"]

    return {
        "import_token": draft["token"],
        "supplier_name": draft["supplier_name"],
        "filename": draft["filename"],
        "rows": len(df),
        "rows_valid": len(df),
        "rows_failed": 0,
        "original_columns": draft["original_columns"],
        "normalized_columns": list(df.columns),
        "normalization_report": draft["normalization_report"],
        "quality_report": draft["quality_report"],
        "preview": df.head(preview_rows).to_dict(orient="records"),
        "expires_at": draft["expires_at"].isoformat(),
    }
