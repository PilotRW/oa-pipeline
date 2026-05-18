import re
from typing import Any

from rapidfuzz import fuzz
from unidecode import unidecode

from app.ingestion.synonyms import COLUMN_SYNONYMS

MATCH_THRESHOLD = 80


def clean_column_name(column: str) -> str:
    column = str(column).strip().lower()
    column = unidecode(column)
    column = re.sub(r"[^a-z0-9]+", " ", column)
    column = re.sub(r"\s+", " ", column)
    return column.strip()


def tokenize_column(column: str) -> list[str]:
    cleaned = clean_column_name(column)
    tokens = cleaned.split(" ")

    return [token for token in tokens if token]


def score_against_synonym(
    cleaned_column: str,
    column_tokens: list[str],
    synonym: str,
) -> tuple[int, int]:
    cleaned_synonym = clean_column_name(synonym)
    synonym_tokens = tokenize_column(synonym)

    full_score = fuzz.ratio(cleaned_column, cleaned_synonym)

    token_scores = []

    for column_token in column_tokens:
        for synonym_token in synonym_tokens:
            token_scores.append(
                fuzz.ratio(column_token, synonym_token)
            )

    best_token_score = max(token_scores) if token_scores else 0

    exact_matches = len(set(column_tokens) & set(synonym_tokens))

    final_score = int(max(full_score, best_token_score))

    if exact_matches > 0:
        final_score = max(final_score, 100)

    return final_score, exact_matches


def score_column(column: str) -> dict[str, Any]:
    cleaned = clean_column_name(column)
    tokens = tokenize_column(column)

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


def normalize_columns(df):
    rename_map = {}
    report = []

    for column in df.columns:
        result = score_column(column)
        report.append(result)

        if result["mapped_to"]:
            rename_map[column] = result["mapped_to"]

    normalized_df = df.rename(columns=rename_map)

    return normalized_df, report