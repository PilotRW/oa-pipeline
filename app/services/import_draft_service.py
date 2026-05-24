from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pandas as pd


IMPORT_DRAFT_TTL = timedelta(minutes=30)

_drafts: dict[str, dict] = {}


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
        "expires_at": expires_at,
    }

    return _drafts[token]


def get_import_draft(token: str) -> dict | None:
    _cleanup_expired_drafts()
    return _drafts.get(token)


def consume_import_draft(token: str) -> dict | None:
    _cleanup_expired_drafts()
    return _drafts.pop(token, None)


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
        "preview": df.head(preview_rows).to_dict(orient="records"),
        "expires_at": draft["expires_at"].isoformat(),
    }
