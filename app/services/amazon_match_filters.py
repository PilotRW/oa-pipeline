import re


def normalize_filter_terms(values: list[str] | None = None) -> list[str]:
    terms = []
    for value in values or []:
        terms.extend(
            part.strip()
            for part in str(value or "").split(",")
            if part.strip()
        )
    return sorted(set(terms), key=str.casefold)


def title_keywords(
    titles: list[str | None],
    limit: int = 12,
) -> list[dict]:
    counts: dict[str, int] = {}
    for title in titles:
        seen = {
            token
            for token in re.findall(
                r"[A-Za-zÀ-ž0-9]+",
                str(title or "").lower(),
            )
            if len(token) >= 4
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


def external_filter_reasons(
    offer,
    *,
    exclude_brands: list[str] | None = None,
    exclude_title_keywords: list[str] | None = None,
    min_cost: float | None = None,
    max_cost: float | None = None,
) -> list[dict]:
    reasons = []
    brand = str(offer.brand or "").casefold()
    title = str(offer.title or "").casefold()
    cost = float(offer.cost) if offer.cost is not None else None

    for value in normalize_filter_terms(exclude_brands):
        if value.casefold() in brand:
            reasons.append({"reason": "excluded_brand", "value": value})
    for value in normalize_filter_terms(exclude_title_keywords):
        if value.casefold() in title:
            reasons.append(
                {"reason": "excluded_title_keyword", "value": value}
            )

    if cost is None and (min_cost is not None or max_cost is not None):
        reasons.append({"reason": "missing_cost", "value": None})
    elif min_cost is not None and cost < min_cost:
        reasons.append({"reason": "below_min_cost", "value": min_cost})
    elif max_cost is not None and cost > max_cost:
        reasons.append({"reason": "above_max_cost", "value": max_cost})
    return reasons


def offer_matches_external_filters(offer, **filters) -> bool:
    return not external_filter_reasons(offer, **filters)


def skipped_breakdown(candidates: list[dict], **filters) -> list[dict]:
    counts: dict[str, int] = {}
    values: dict[str, dict[str, int]] = {}

    for candidate in candidates:
        for reason in external_filter_reasons(candidate["offer"], **filters):
            key = reason["reason"]
            value = reason["value"]
            counts[key] = counts.get(key, 0) + 1
            if value is not None:
                value_key = str(value)
                bucket = values.setdefault(key, {})
                bucket[value_key] = bucket.get(value_key, 0) + 1

    return [
        {
            "reason": reason,
            "count": count,
            "values": [
                {"value": value, "count": value_count}
                for value, value_count in sorted(
                    values.get(reason, {}).items(),
                    key=lambda item: (-item[1], item[0]),
                )[:8]
            ],
        }
        for reason, count in sorted(
            counts.items(),
            key=lambda item: (-item[1], item[0]),
        )
    ]
