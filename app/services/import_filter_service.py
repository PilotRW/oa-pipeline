import re

import pandas as pd


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


def _missing_count(df: pd.DataFrame, column: str) -> int:
    if column not in df.columns:
        return len(df)
    return int((df[column].astype(str).str.strip() == "").sum())


def _examples(
    df: pd.DataFrame,
    mask,
    columns: list[str],
    limit: int = 5,
) -> list[dict]:
    available = [column for column in columns if column in df.columns]
    if not available:
        return []
    return df.loc[mask, available].head(limit).to_dict(orient="records")


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
        present = ean != ""
        duplicates = present & ean.duplicated(keep=False)
        report["duplicate_ean_count"] = int(duplicates.sum())
        report["examples"]["duplicate_ean"] = _examples(
            df,
            duplicates,
            ["ean", "brand", "title", "price", "stock"],
        )
        report["examples"]["missing_ean"] = _examples(
            df,
            ~present,
            ["brand", "title", "price", "stock"],
        )

    if "price" in df.columns:
        prices = pd.to_numeric(df["price"], errors="coerce")
        missing = prices.isna()
        suspicious = prices.notna() & (
            (prices < SUSPICIOUS_LOW_PRICE)
            | (prices > SUSPICIOUS_HIGH_PRICE)
        )
        report["suspicious_price_count"] = int(suspicious.sum())
        report["examples"]["missing_price"] = _examples(
            df,
            missing,
            ["ean", "brand", "title", "stock"],
        )
        report["examples"]["suspicious_price"] = _examples(
            df,
            suspicious,
            ["ean", "brand", "title", "price", "stock"],
        )

    for item in normalization_report:
        if not item.get("mapped_to"):
            report["unmapped_columns"].append(item["column"])
        elif item.get("confidence", 0) < WEAK_MAPPING_CONFIDENCE:
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
        {"value": str(value), "count": int(count)}
        for value, count in counts.items()
    ]


def _unique_text_count(df: pd.DataFrame, column: str) -> int:
    if column not in df.columns:
        return 0
    values = df[column].astype(str).str.strip()
    return int(values[values != ""].nunique())


def _title_keywords(
    df: pd.DataFrame,
    limit: int = KEYWORD_FILTER_SUGGESTION_LIMIT,
) -> list[dict]:
    if "title" not in df.columns:
        return []

    counts: dict[str, int] = {}
    for title in df["title"].astype(str):
        seen = {
            token
            for token in re.findall(r"[A-Za-zÀ-ž0-9]+", title.lower())
            if len(token) >= MIN_KEYWORD_LENGTH
            and token not in TITLE_KEYWORD_STOPWORDS
        }
        for token in seen:
            counts[token] = counts.get(token, 0) + 1

    return [
        {"value": value, "count": count}
        for value, count in sorted(
            counts.items(),
            key=lambda item: (-item[1], item[0]),
        )[:limit]
    ]


def _price_summary(df: pd.DataFrame) -> dict:
    empty = {"min": None, "max": None, "median": None}
    if "price" not in df.columns:
        return empty
    prices = pd.to_numeric(df["price"], errors="coerce").dropna()
    if prices.empty:
        return empty
    return {
        "min": float(prices.min()),
        "max": float(prices.max()),
        "median": float(prices.median()),
    }


def non_new_mask(df: pd.DataFrame) -> pd.Series:
    mask = pd.Series(False, index=df.index)
    fields = [
        column
        for column in ("condition", "title", "description")
        if column in df.columns
    ]
    if not fields:
        return mask

    pattern = "|".join(
        re.escape(value.casefold()) for value in NON_NEW_PATTERNS
    )
    for field in fields:
        mask |= df[field].astype(str).str.casefold().str.contains(
            pattern,
            na=False,
        )
    return mask


def build_filter_suggestions(df: pd.DataFrame) -> dict:
    return {
        "brands": _top_text_values(df, "brand"),
        "title_keywords": _title_keywords(df),
        "brand_total_unique": _unique_text_count(df, "brand"),
        "brand_suggestion_limit": BRAND_FILTER_SUGGESTION_LIMIT,
        "title_keyword_suggestion_limit": KEYWORD_FILTER_SUGGESTION_LIMIT,
        "missing_ean_count": _missing_count(df, "ean"),
        "non_new_count": int(non_new_mask(df).sum()),
        "price": _price_summary(df),
    }


def _normalized_text_set(values) -> set[str]:
    return {
        str(value).strip().casefold()
        for value in values
        if str(value).strip()
    }


def apply_import_filters(
    df: pd.DataFrame,
    filters: dict | None,
) -> tuple[pd.DataFrame, dict]:
    filters = filters or {}
    include_mask = pd.Series(True, index=df.index)
    excluded_brands = _normalized_text_set(
        filters.get("excluded_brands", [])
    )
    included_brands = _normalized_text_set(
        filters.get("included_brands", [])
    )
    mode = str(filters.get("brand_filter_mode") or "exclude").strip().casefold()

    if (included_brands or excluded_brands) and "brand" in df.columns:
        brands = df["brand"].astype(str).str.strip().str.casefold()
        brand_mask = pd.Series(False, index=df.index)
        active = included_brands if mode == "include" else excluded_brands
        for brand in active:
            brand_mask |= brands.str.contains(re.escape(brand), na=False)
        include_mask &= brand_mask if mode == "include" else ~brand_mask

    excluded_keywords = [
        str(value).strip().casefold()
        for value in filters.get("excluded_keywords", [])
        if str(value).strip()
    ]
    if excluded_keywords and "title" in df.columns:
        titles = df["title"].astype(str).str.casefold()
        keyword_mask = pd.Series(False, index=df.index)
        for keyword in excluded_keywords:
            keyword_mask |= titles.str.contains(re.escape(keyword), na=False)
        include_mask &= ~keyword_mask

    if filters.get("exclude_missing_ean") and "ean" in df.columns:
        include_mask &= df["ean"].astype(str).str.strip() != ""
    if filters.get("exclude_non_new"):
        include_mask &= ~non_new_mask(df)

    if "price" in df.columns:
        prices = pd.to_numeric(df["price"], errors="coerce")
        min_price = filters.get("min_price")
        max_price = filters.get("max_price")
        if min_price not in (None, ""):
            include_mask &= prices.ge(float(min_price)).fillna(False)
        if max_price not in (None, ""):
            include_mask &= prices.le(float(max_price)).fillna(False)

    filtered = df.loc[include_mask].copy()
    return filtered, {
        "rows_before": int(len(df)),
        "rows_after": int(len(filtered)),
        "rows_excluded": int(len(df) - len(filtered)),
        "filters": {
            "brand_filter_mode": mode,
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
