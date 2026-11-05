import re
from decimal import Decimal, InvalidOperation


QUANTITY_KEYS = {
    "moq",
    "minamount",
    "minimumorderquantity",
    "minimumquantity",
    "minqty",
    "mindestbestellmenge",
}
TIER_QUANTITY_PATTERNS = [
    re.compile(pattern)
    for pattern in (
        r"^(?:bulk|tier|volume|staffel)(\d+)(?:qty|quantity|menge)$",
        r"^(?:bulk|tier|volume|staffel)(?:qty|quantity|menge)(\d+)$",
        r"^(?:qty|quantity|menge)(\d+)$",
    )
]
TIER_PRICE_PATTERNS = [
    re.compile(pattern)
    for pattern in (
        r"^(?:bulk|tier|volume|staffel)(\d+)(?:price|preis|cost)$",
        r"^(?:bulk|tier|volume|staffel)(?:price|preis|cost)(\d+)$",
        r"^(?:price|preis|cost)(\d+)$",
    )
]


def normalized_key(value) -> str:
    return re.sub(r"[^a-z0-9]", "", str(value or "").lower())


def decimal_or_none(value) -> Decimal | None:
    if value is None or value == "":
        return None

    normalized = str(value).strip()
    normalized = re.sub(r"(?:EUR|eur|€|\s)", "", normalized)
    if "," in normalized and "." in normalized:
        if normalized.rfind(",") > normalized.rfind("."):
            normalized = normalized.replace(".", "").replace(",", ".")
        else:
            normalized = normalized.replace(",", "")
    elif "," in normalized:
        normalized = normalized.replace(",", ".")

    try:
        return Decimal(normalized)
    except (InvalidOperation, TypeError, ValueError):
        return None


def positive_integer(value) -> int | None:
    number = decimal_or_none(value)
    if number is None or number <= 0:
        return None
    return int(number)


def tier_number(key: str, patterns: list[re.Pattern]) -> int | None:
    for pattern in patterns:
        match = pattern.match(key)
        if match:
            return int(match.group(1))
    return None


def extract_price_tiers(
    values: dict | None,
    base_cost=None,
) -> list[dict]:
    values = values if isinstance(values, dict) else {}
    normalized = {normalized_key(key): value for key, value in values.items()}
    base_price = decimal_or_none(
        base_cost if base_cost not in (None, "") else normalized.get("price")
    )
    base_quantity = next(
        (
            quantity
            for key in QUANTITY_KEYS
            if (quantity := positive_integer(normalized.get(key))) is not None
        ),
        1,
    )

    tiers: dict[int, dict] = {}
    if base_price is not None and base_price >= 0:
        tiers[base_quantity] = {
            "min_quantity": base_quantity,
            "unit_cost": float(base_price),
            "source": "base",
        }

    quantities: dict[int, tuple[int, str]] = {}
    prices: dict[int, tuple[Decimal, str]] = {}
    for raw_key, value in values.items():
        key = normalized_key(raw_key)
        quantity_tier = tier_number(key, TIER_QUANTITY_PATTERNS)
        if quantity_tier is not None:
            quantity = positive_integer(value)
            if quantity is not None:
                quantities[quantity_tier] = (quantity, str(raw_key))

        price_tier = tier_number(key, TIER_PRICE_PATTERNS)
        if price_tier is not None:
            price = decimal_or_none(value)
            if price is not None and price > 0:
                prices[price_tier] = (price, str(raw_key))

    for number in sorted(set(quantities) & set(prices)):
        quantity, quantity_column = quantities[number]
        price, price_column = prices[number]
        tiers[quantity] = {
            "min_quantity": quantity,
            "unit_cost": float(price),
            "source": "volume",
            "quantity_column": quantity_column,
            "price_column": price_column,
        }

    return [tiers[quantity] for quantity in sorted(tiers)]


def select_price_tier(
    price_tiers: list[dict] | None,
    purchase_quantity: int,
    *,
    raw_data: dict | None = None,
    base_cost=None,
) -> tuple[dict | None, int | None]:
    tiers = price_tiers or extract_price_tiers(raw_data, base_cost)
    valid_tiers = [
        tier
        for tier in tiers
        if positive_integer(tier.get("min_quantity")) is not None
        and decimal_or_none(tier.get("unit_cost")) is not None
    ]
    eligible = [
        tier
        for tier in valid_tiers
        if int(tier["min_quantity"]) <= purchase_quantity
    ]
    if not eligible:
        minimum = min(
            (int(tier["min_quantity"]) for tier in valid_tiers),
            default=None,
        )
        return None, minimum

    return max(eligible, key=lambda tier: int(tier["min_quantity"])), None
