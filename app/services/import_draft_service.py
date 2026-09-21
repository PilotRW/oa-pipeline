import gc
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pandas as pd

from app.services.import_filter_service import (
    apply_import_filters,
    build_filter_suggestions,
    build_quality_report,
    non_new_mask,
    serialize_import_draft,
)


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
    supplier_id: int | None = None,
) -> dict:
    _cleanup_expired_drafts()
    token = uuid4().hex
    draft = {
        "token": token,
        "supplier_name": supplier_name,
        "supplier_id": supplier_id,
        "filename": filename,
        "df": df.copy(),
        "original_columns": list(original_columns),
        "normalization_report": normalization_report,
        "quality_report": build_quality_report(
            df=df,
            normalization_report=normalization_report,
        ),
        "expires_at": _now() + IMPORT_DRAFT_TTL,
    }
    _drafts[token] = draft
    return draft


def get_import_draft(token: str) -> dict | None:
    _cleanup_expired_drafts()
    return _drafts.get(token)


def consume_import_draft(token: str) -> dict | None:
    _cleanup_expired_drafts()
    return _drafts.pop(token, None)


def get_import_draft_stats() -> dict:
    _cleanup_expired_drafts()
    row_count = 0
    estimated_bytes = 0
    for draft in _drafts.values():
        df = draft.get("df")
        if df is None:
            continue
        row_count += len(df)
        estimated_bytes += int(
            df.memory_usage(index=True, deep=True).sum()
        )
    return {
        "drafts": len(_drafts),
        "rows": row_count,
        "estimated_bytes": estimated_bytes,
    }


def clear_import_drafts() -> dict:
    stats = get_import_draft_stats()
    _drafts.clear()
    gc.collect()
    return {
        "drafts_cleared": stats["drafts"],
        "rows_released": stats["rows"],
        "estimated_bytes_released": stats["estimated_bytes"],
    }


__all__ = [
    "apply_import_filters",
    "build_filter_suggestions",
    "build_quality_report",
    "clear_import_drafts",
    "consume_import_draft",
    "create_import_draft",
    "get_import_draft",
    "get_import_draft_stats",
    "non_new_mask",
    "serialize_import_draft",
]
