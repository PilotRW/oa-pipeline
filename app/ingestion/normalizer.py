import re
from typing import Any

import pandas as pd
from rapidfuzz import fuzz
from unidecode import unidecode

from app.ingestion.cleaners import is_valid_gtin, recover_gtin
from app.ingestion.synonyms import COLUMN_SYNONYMS

MATCH_THRESHOLD = 80

EXACT_COLUMN_MAPPINGS = {
    "barcode": "ean",
    "barcode2": "ean",
    "barcode3": "ean",
    "barcode4": "ean",
    "gtin code": "ean",
    "gtincode": "ean",
    "product desc": "title",
    "productdesc": "title",
    "product id": "supplier_sku",
    "productid": "supplier_sku",
    "product code": "supplier_sku",
    "cost price excl vat": "price",
    "costpriceexclvat": "price",
    "cost price excl vat excl tax": "price",
    "costpriceexclvatexcltax": "price",
    "prices": "price",
    "vat": "vat_rate",
}

GENERIC_IDENTIFIER_COLUMNS = {
    "c",
    "code",
    "code sap",
    "product code",
}

STOPWORDS = {
    "code",
    "number",
    "nr",
    "no",
}

IGNORED_COLUMNS = {
    "text",
    "text 1",
    "zip code",
}


def clean_column_name(column: str) -> str:
    column = str(column).strip().lower()
    column = unidecode(column)
    column = re.sub(r"[^a-z0-9]+", " ", column)
    column = re.sub(r"\s+", " ", column)
    return column.strip()


def tokenize_column(column: str) -> list[str]:
    cleaned = clean_column_name(column)
    tokens = cleaned.split(" ")

    return [
        token
        for token in tokens
        if token and token not in STOPWORDS
    ]


def should_ignore_column(column: str) -> bool:
    cleaned = clean_column_name(column)

    if cleaned.startswith("unnamed"):
        return True

    if cleaned in IGNORED_COLUMNS:
        return True

    return False


def preferred_mapping_priority(column: Any, mapped_to: str | None) -> int:
    if mapped_to != "price":
        return 0
    tokens = set(tokenize_column(column))
    return 100 if {"new", "price"}.issubset(tokens) else 0


def reorder_duplicate_mappings(
    df: pd.DataFrame,
    source_columns: list[Any],
    mapped_columns: list[Any],
) -> pd.DataFrame:
    positions = list(range(len(source_columns)))
    duplicate_targets = {
        column
        for column in mapped_columns
        if mapped_columns.count(column) > 1
    }

    for target in duplicate_targets:
        slots = [
            index
            for index, column in enumerate(mapped_columns)
            if column == target
        ]
        preferred = sorted(
            slots,
            key=lambda index: preferred_mapping_priority(
                source_columns[index],
                str(target),
            ),
            reverse=True,
        )
        for slot, source_index in zip(slots, preferred):
            positions[slot] = source_index

    reordered = df.iloc[:, positions].copy()
    reordered.columns = [mapped_columns[index] for index in positions]
    return reordered


def score_against_synonym(
    cleaned_column: str,
    column_tokens: list[str],
    synonym: str,
) -> tuple[int, int]:
    cleaned_synonym = clean_column_name(synonym)
    synonym_tokens = tokenize_column(synonym)

    if cleaned_column == cleaned_synonym:
        return 100, len(synonym_tokens)

    full_score = fuzz.ratio(cleaned_column, cleaned_synonym)

    token_scores = []

    for column_token in column_tokens:
        for synonym_token in synonym_tokens:
            token_scores.append(
                fuzz.ratio(column_token, synonym_token)
            )

    best_token_score = max(token_scores) if token_scores else 0

    intersection = set(column_tokens) & set(synonym_tokens)
    exact_matches = len(intersection)

    if exact_matches >= 2:
        return 100, exact_matches

    if exact_matches == 1:
        return int(max(full_score, best_token_score, 92)), exact_matches

    fuzzy_only_score = int(max(full_score, best_token_score) * 0.7)

    return fuzzy_only_score, exact_matches


def score_column(column: str) -> dict[str, Any]:
    cleaned = clean_column_name(column)
    tokens = tokenize_column(column)
    exact_mapping = EXACT_COLUMN_MAPPINGS.get(cleaned)

    if exact_mapping:
        return {
            "column": column,
            "cleaned_column": cleaned,
            "tokens": tokens,
            "mapped_to": exact_mapping,
            "confidence": 100,
            "exact_matches": len(tokens),
            "matched_synonym": cleaned,
            "alternatives": [
                {
                    "field": exact_mapping,
                    "score": 100,
                    "exact_matches": len(tokens),
                    "matched_synonym": cleaned,
                }
            ],
        }

    candidates = []

    for canonical_name, synonyms in COLUMN_SYNONYMS.items():
        best_score = 0
        best_exact_matches = 0
        best_synonym = None

        for synonym in synonyms:
            score, exact_matches = score_against_synonym(
                cleaned_column=cleaned,
                column_tokens=tokens,
                synonym=synonym,
            )

            if (
                score > best_score
                or (
                    score == best_score
                    and exact_matches > best_exact_matches
                )
            ):
                best_score = score
                best_exact_matches = exact_matches
                best_synonym = synonym

        candidates.append(
            {
                "field": canonical_name,
                "score": best_score,
                "exact_matches": best_exact_matches,
                "matched_synonym": best_synonym,
            }
        )

    candidates = sorted(
        candidates,
        key=lambda item: (
            item["score"],
            item["exact_matches"],
        ),
        reverse=True,
    )

    best = candidates[0]
    mapped_to = best["field"] if best["score"] >= MATCH_THRESHOLD else None

    return {
        "column": column,
        "cleaned_column": cleaned,
        "tokens": tokens,
        "mapped_to": mapped_to,
        "confidence": best["score"],
        "exact_matches": best["exact_matches"],
        "matched_synonym": best["matched_synonym"],
        "alternatives": candidates[:3],
    }


def identifier_ratio(series: pd.Series) -> float:
    values = [
        re.sub(r"\.0$", "", str(value).strip())
        for value in series
        if pd.notna(value) and str(value).strip()
    ]
    if not values:
        return 0.0
    matches = sum(bool(recover_gtin(value)) for value in values)
    return matches / len(values)


def numeric_ratio(series: pd.Series) -> float:
    values = [
        str(value).strip()
        for value in series
        if pd.notna(value) and str(value).strip()
    ]
    if not values:
        return 0.0
    numeric = pd.to_numeric(
        pd.Series(values).str.replace(",", ".", regex=False),
        errors="coerce",
    )
    return float(numeric.notna().mean())


def text_ratio(series: pd.Series) -> float:
    values = [
        str(value).strip()
        for value in series
        if pd.notna(value) and str(value).strip()
    ]
    if not values:
        return 0.0
    matches = sum(
        bool(re.search(r"[A-Za-zÀ-ž]", value)) and len(value) >= 5
        for value in values
    )
    return matches / len(values)


def text_score(series: pd.Series) -> float:
    values = [
        str(value).strip()
        for value in series
        if pd.notna(value) and str(value).strip()
    ]
    if not values:
        return 0.0
    average_length = sum(len(value) for value in values) / len(values)
    return text_ratio(series) * average_length


def infer_headerless_mappings(df: pd.DataFrame) -> dict[Any, str]:
    if not all(isinstance(column, int) for column in df.columns):
        return {}

    mappings: dict[Any, str] = {}
    remaining = list(df.columns)

    ean_candidates = sorted(
        remaining,
        key=lambda column: identifier_ratio(df[column]),
        reverse=True,
    )
    if ean_candidates and identifier_ratio(df[ean_candidates[0]]) >= 0.7:
        mappings[ean_candidates[0]] = "ean"
        remaining.remove(ean_candidates[0])

    title_candidates = sorted(
        remaining,
        key=lambda column: text_score(df[column]),
        reverse=True,
    )
    if title_candidates and text_ratio(df[title_candidates[0]]) >= 0.7:
        mappings[title_candidates[0]] = "title"
        remaining.remove(title_candidates[0])

    price_candidates = sorted(
        remaining,
        key=lambda column: numeric_ratio(df[column]),
        reverse=True,
    )
    if price_candidates and numeric_ratio(df[price_candidates[0]]) >= 0.7:
        mappings[price_candidates[0]] = "price"

    return mappings


def infer_content_mappings(df: pd.DataFrame) -> dict[Any, str]:
    mappings = infer_headerless_mappings(df)

    for column in df.columns:
        if identifier_ratio(df[column]) >= 0.7:
            mappings[column] = "ean"

    effective_mappings = {}
    for column in df.columns:
        result = score_column(column)
        effective_mappings[column] = mappings.get(
            column,
            result["mapped_to"],
        )

    unnamed_columns = [
        column
        for column in df.columns
        if clean_column_name(column).startswith("unnamed")
        and column not in mappings
    ]

    if "title" not in effective_mappings.values():
        title_candidates = [
            column
            for column in unnamed_columns
            if text_ratio(df[column]) >= 0.7
        ]
        if title_candidates:
            best = max(
                title_candidates,
                key=lambda column: text_score(df[column]),
            )
            mappings[best] = "title"
            effective_mappings[best] = "title"

    if "price" not in effective_mappings.values():
        price_candidates = [
            column
            for column in unnamed_columns
            if column not in mappings
            and numeric_ratio(df[column]) >= 0.7
            and identifier_ratio(df[column]) < 0.5
        ]
        if price_candidates:
            best = max(
                price_candidates,
                key=lambda column: numeric_ratio(df[column]),
            )
            mappings[best] = "price"

    return mappings


def normalize_columns(df):
    rename_map = {}
    report = []
    inferred_mappings = infer_content_mappings(df)

    for column in df.columns:
        if should_ignore_column(column) and column not in inferred_mappings:
            continue

        result = score_column(column)
        inferred_mapping = inferred_mappings.get(column)
        cleaned_column = result["cleaned_column"]
        if (
            cleaned_column in GENERIC_IDENTIFIER_COLUMNS
            and identifier_ratio(df[column]) >= 0.7
        ):
            inferred_mapping = "ean"

        if inferred_mapping:
            result = {
                **result,
                "mapped_to": inferred_mapping,
                "confidence": 95,
                "matched_synonym": "inferred from column values",
            }
        report.append(result)

        if result["mapped_to"]:
            rename_map[column] = result["mapped_to"]

    source_columns = list(df.columns)
    mapped_columns = [
        rename_map.get(column, column)
        for column in source_columns
    ]
    normalized_df = reorder_duplicate_mappings(
        df,
        source_columns,
        mapped_columns,
    )

    return normalized_df, report
