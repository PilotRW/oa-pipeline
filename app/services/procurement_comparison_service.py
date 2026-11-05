import re
from decimal import Decimal, InvalidOperation

from app.services.price_tier_service import extract_price_tiers, select_price_tier


EAN_CANDIDATE = re.compile(r"(?<!\d)(\d[\d\s-]{6,18}\d)(?!\d)")
LINE_NUMBER = re.compile(
    r"^\s*\d+[.)]?(?:\s|[\u200b-\u200f\u2060\ufeff])*"
)
EAN_LABEL = re.compile(r"\s*(?:[-—:]\s*)?(?:EAN|ETAN|ЕТАН)\s*$", re.IGNORECASE)


def normalize_ean(value: str) -> str | None:
    digits = re.sub(r"\D", "", str(value or ""))
    if 8 <= len(digits) <= 14:
        return digits
    return None


def canonical_ean(value: str) -> str | None:
    normalized = normalize_ean(value)
    if normalized is None:
        return None
    return normalized.lstrip("0") or "0"


def ean_lookup_variants(value: str) -> set[str]:
    normalized = normalize_ean(value)
    canonical = canonical_ean(value)
    if normalized is None or canonical is None:
        return set()

    variants = {normalized}
    for length in range(max(8, len(canonical)), 15):
        variants.add(canonical.zfill(length))
    return variants


def parse_product_list(text: str) -> tuple[list[dict], list[dict]]:
    products: list[dict] = []
    invalid_lines: list[dict] = []

    for line_number, raw_line in enumerate(str(text or "").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue

        matches = list(EAN_CANDIDATE.finditer(line))
        match = next(
            (
                candidate
                for candidate in reversed(matches)
                if normalize_ean(candidate.group(1))
            ),
            None,
        )
        if match is None:
            invalid_lines.append({"line": line_number, "text": line})
            continue

        ean = normalize_ean(match.group(1))
        title = LINE_NUMBER.sub("", line[:match.start()]).strip()
        title = EAN_LABEL.sub("", title).strip(" -—:.,")

        products.append(
            {
                "line": line_number,
                "title": title or None,
                "ean": ean,
                "input": line,
            }
        )

    return products, invalid_lines


def decimal_or_none(value) -> Decimal | None:
    if value is None or value == "":
        return None
    try:
        return Decimal(str(value).replace(",", "."))
    except (InvalidOperation, TypeError, ValueError):
        return None


def price_candidate(
    candidate: dict,
    target_currency: str,
    purchase_quantity: int = 1,
) -> dict:
    price_tiers = candidate.get("price_tiers") or extract_price_tiers(
        candidate.get("raw_data"),
        candidate.get("cost"),
    )
    selected_tier, minimum_quantity = select_price_tier(
        price_tiers,
        purchase_quantity,
    )
    source_cost = decimal_or_none(
        selected_tier.get("unit_cost") if selected_tier else None
    )
    currency = str(candidate.get("currency") or "").strip().upper()
    unavailable_reason = None

    if selected_tier is None and minimum_quantity is not None:
        unavailable_reason = "minimum_quantity"
    elif source_cost is None or source_cost < 0:
        unavailable_reason = "missing_cost"
    elif currency != target_currency:
        unavailable_reason = "currency_mismatch"

    return {
        "offer_id": candidate.get("offer_id"),
        "supplier_id": candidate.get("supplier_id"),
        "supplier": candidate.get("supplier"),
        "supplier_sku": candidate.get("supplier_sku"),
        "title": candidate.get("title"),
        "brand": candidate.get("brand"),
        "source_file": candidate.get("source_file"),
        "source_cost": float(source_cost) if source_cost is not None else None,
        "currency": currency or None,
        "stock": candidate.get("stock"),
        "supply_channel": candidate.get("supply_channel") or "stock",
        "lead_time_min_days": candidate.get("lead_time_min_days"),
        "lead_time_max_days": candidate.get("lead_time_max_days"),
        "purchase_quantity": purchase_quantity,
        "tier_min_quantity": (
            int(selected_tier["min_quantity"])
            if selected_tier
            else None
        ),
        "price_tier_source": selected_tier.get("source") if selected_tier else None,
        "minimum_quantity": minimum_quantity,
        "available_tiers": len(price_tiers),
        "comparable": unavailable_reason is None,
        "unavailable_reason": unavailable_reason,
        "imported_at": candidate.get("imported_at"),
    }


def compare_product_offers(
    products: list[dict],
    candidates: list[dict],
    target_currency: str = "EUR",
    purchase_quantity: int = 1,
) -> list[dict]:
    target_currency = str(target_currency or "EUR").strip().upper()
    candidates_by_ean: dict[str, list[dict]] = {}

    for candidate in candidates:
        ean = canonical_ean(candidate.get("ean"))
        if ean:
            candidates_by_ean.setdefault(ean, []).append(candidate)

    results = []
    for product in products:
        priced = [
            price_candidate(candidate, target_currency, purchase_quantity)
            for candidate in candidates_by_ean.get(
                canonical_ean(product["ean"]),
                [],
            )
        ]
        priced.sort(
            key=lambda offer: (
                not offer["comparable"],
                offer["source_cost"] if offer["source_cost"] is not None else float("inf"),
                str(offer.get("supplier") or "").lower(),
            )
        )
        comparable = [offer for offer in priced if offer["comparable"]]
        winner = comparable[0] if comparable else None

        if winner:
            status = "matched"
        elif not priced:
            status = "not_found"
        elif any(
            offer["unavailable_reason"] == "minimum_quantity"
            for offer in priced
        ):
            status = "minimum_quantity"
        else:
            status = "currency_mismatch"

        if winner:
            for offer in priced:
                offer["difference_to_best"] = (
                    round(offer["source_cost"] - winner["source_cost"], 2)
                    if offer["source_cost"] is not None
                    else None
                )

        results.append(
            {
                **product,
                "status": status,
                "offers_found": len(priced),
                "winner": winner,
                "offers": priced,
            }
        )

    return results
