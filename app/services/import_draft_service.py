from datetime import datetime, timedelta, timezone
import gc
import re
from uuid import uuid4

import pandas as pd


IMPORT_DRAFT_TTL = timedelta(minutes=30)

_drafts: dict[str, dict] = {}

WEAK_MAPPING_CONFIDENCE = 90
SUSPICIOUS_LOW_PRICE = 0.01
SUSPICIOUS_HIGH_PRICE = 10000
BRAND_FILTER_SUGGESTION_LIMIT = None
KEYWORD_FILTER_SUGGESTION_LIMIT = 40
MIN_KEYWORD_LENGTH = 4
NON_NEW_PATTERNS = [
    "refurbished",
    "renewed",
    "remanufactured",
    "used",
    "used like new",
    "like new",
    "open box",
    "open-box",
    "pre-owned",
    "preowned",
    "second hand",
    "second-hand",
    "gebraucht",
    "generaluberholt",
    "generalüberholt",
    "erneuert",
    "wie neu",
    "b-ware",
    "retoure",
    "rückläufer",
    "rucklaufer",
    "reconditioned",
]
TITLE_KEYWORD_STOPWORDS = {
    "with",
    "from",
    "for",
    "und",
    "oder",
    "eine",
    "einer",
    "the",
    "and",
    "der",
    "die",
    "das",
    "von",
    "mit",
}


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
    expires_at = _now() + IMPORT_DRAFT_TTL

    _drafts[token] = {
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
        "expires_at": expires_at,
    }

    return _drafts[token]


def get_import_draft(token: str) -> dict | None:
    _cleanup_expired_drafts()
    return _drafts.get(token)


def consume_import_draft(token: str) -> dict | None:
    _cleanup_expired_drafts()
    return _drafts.pop(token, None)


def get_import_draft_stats() -> dict:
    _cleanup_expired_drafts()

    draft_count = len(_drafts)
    row_count = 0
    estimated_bytes = 0

    for draft in _drafts.values():
        df = draft.get("df")

        if df is None:
            continue

        row_count += len(df)
        estimated_bytes += int(
            df.memory_usage(
                index=True,
                deep=True,
            ).sum()
        )

    return {
        "drafts": draft_count,
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


def _top_text_values(
    df: pd.DataFrame,
    column: str,
    limit: int | None = BRAND_FILTER_SUGGESTION_LIMIT,
) -> list[dict]:
    if column not in df.columns:
        return []

    values = df[column].astype(str).str.strip()
    values = values[values != ""]

    if values.empty:
        return []

    counts = values.value_counts()

    if limit is not None:
        counts = counts.head(limit)

    return [
        {
            "value": str(value),
            "count": int(count),
        }
        for value, count in counts.items()
    ]


def _unique_text_count(
    df: pd.DataFrame,
    column: str,
) -> int:
    if column not in df.columns:
        return 0

    values = df[column].astype(str).str.strip()
    values = values[values != ""]

    return int(values.nunique())


def _title_keywords(
    df: pd.DataFrame,
    limit: int = KEYWORD_FILTER_SUGGESTION_LIMIT,
) -> list[dict]:
    if "title" not in df.columns:
        return []

    counts: dict[str, int] = {}

    for title in df["title"].astype(str):
        seen = set()

        for token in re.findall(r"[A-Za-zÀ-ž0-9]+", title.lower()):
            if (
                len(token) < MIN_KEYWORD_LENGTH
                or token in TITLE_KEYWORD_STOPWORDS
            ):
                continue

            seen.add(token)

        for token in seen:
            counts[token] = counts.get(token, 0) + 1

    return [
        {
            "value": value,
            "count": count,
        }
        for value, count in sorted(
            counts.items(),
            key=lambda item: (-item[1], item[0]),
        )[:limit]
    ]


def _price_summary(df: pd.DataFrame) -> dict:
    if "price" not in df.columns:
        return {
            "min": None,
            "max": None,
            "median": None,
        }

    prices = pd.to_numeric(
        df["price"],
        errors="coerce",
    ).dropna()

    if prices.empty:
        return {
            "min": None,
            "max": None,
            "median": None,
        }

    return {
        "min": float(prices.min()),
        "max": float(prices.max()),
        "median": float(prices.median()),
    }


def non_new_mask(df: pd.DataFrame) -> pd.Series:
    mask = pd.Series(False, index=df.index)
    fields = [
        column
        for column in ["condition", "title", "description"]
        if column in df.columns
    ]

    if not fields:
        return mask

    pattern = "|".join(
        re.escape(value.casefold())
        for value in NON_NEW_PATTERNS
    )

    for field in fields:
        values = df[field].astype(str).str.casefold()
        mask |= values.str.contains(pattern, na=False)

    return mask


def build_filter_suggestions(df: pd.DataFrame) -> dict:
    brand_values = _top_text_values(df, "brand")
    keyword_values = _title_keywords(df)

    return {
        "brands": brand_values,
        "title_keywords": keyword_values,
        "brand_total_unique": _unique_text_count(df, "brand"),
        "brand_suggestion_limit": BRAND_FILTER_SUGGESTION_LIMIT,
        "title_keyword_suggestion_limit": KEYWORD_FILTER_SUGGESTION_LIMIT,
        "missing_ean_count": _missing_count(df, "ean"),
        "non_new_count": int(non_new_mask(df).sum()),
        "price": _price_summary(df),
    }


def apply_import_filters(
    df: pd.DataFrame,
    filters: dict | None,
) -> tuple[pd.DataFrame, dict]:
    filters = filters or {}
    include_mask = pd.Series(True, index=df.index)

    excluded_brands = {
        str(value).strip().casefold()
        for value in filters.get("excluded_brands", [])
        if str(value).strip()
    }
    included_brands = {
        str(value).strip().casefold()
        for value in filters.get("included_brands", [])
        if str(value).strip()
    }
    brand_filter_mode = str(
        filters.get("brand_filter_mode") or "exclude"
    ).strip().casefold()

    if (included_brands or excluded_brands) and "brand" in df.columns:
        brands = df["brand"].astype(str).str.strip().str.casefold()
        brand_mask = pd.Series(False, index=df.index)

        active_brands = (
            included_brands
            if brand_filter_mode == "include"
            else excluded_brands
        )

        for brand in active_brands:
            brand_mask |= brands.str.contains(
                re.escape(brand),
                na=False,
            )

        if brand_filter_mode == "include":
            include_mask &= brand_mask
        else:
            include_mask &= ~brand_mask

    excluded_keywords = [
        str(value).strip().casefold()
        for value in filters.get("excluded_keywords", [])
        if str(value).strip()
    ]

    if excluded_keywords and "title" in df.columns:
        titles = df["title"].astype(str).str.casefold()
        keyword_mask = pd.Series(False, index=df.index)

        for keyword in excluded_keywords:
            keyword_mask |= titles.str.contains(
                re.escape(keyword),
                na=False,
            )

        include_mask &= ~keyword_mask

    if filters.get("exclude_missing_ean") and "ean" in df.columns:
        ean = df["ean"].astype(str).str.strip()
        include_mask &= ean != ""

    if filters.get("exclude_non_new"):
        include_mask &= ~non_new_mask(df)

    if "price" in df.columns:
        prices = pd.to_numeric(
            df["price"],
            errors="coerce",
        )
        min_price = filters.get("min_price")
        max_price = filters.get("max_price")

        if min_price not in (None, ""):
            include_mask &= prices.ge(float(min_price)).fillna(False)

        if max_price not in (None, ""):
            include_mask &= prices.le(float(max_price)).fillna(False)

    filtered_df = df.loc[include_mask].copy()

    return filtered_df, {
        "rows_before": int(len(df)),
        "rows_after": int(len(filtered_df)),
        "rows_excluded": int(len(df) - len(filtered_df)),
        "filters": {
            "brand_filter_mode": brand_filter_mode,
            "excluded_brands": sorted(excluded_brands),
            "included_brands": sorted(included_brands),
            "excluded_keywords": excluded_keywords,
            "exclude_missing_ean": bool(filters.get("exclude_missing_ean")),
            "exclude_non_new": bool(filters.get("exclude_non_new")),
            "min_price": filters.get("min_price"),
            "max_price": filters.get("max_price"),
        },
    }


def serialize_import_draft(draft: dict, preview_rows: int = 50) -> dict:
    df = draft["df"]

    filter_summary = draft.get("filter_summary")

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
        "quality_report": build_quality_report(
            df=df,
            normalization_report=draft["normalization_report"],
        ),
        "filter_suggestions": build_filter_suggestions(df),
        "filter_summary": filter_summary,
        "is_filtered_preview": filter_summary is not None,
        "preview": df.head(preview_rows).to_dict(orient="records"),
        "expires_at": draft["expires_at"].isoformat(),
    }
