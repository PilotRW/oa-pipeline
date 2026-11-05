import re

import pandas as pd


TESTER_PATTERNS = ("tester", "testeur", "тестер")
GTIN_LENGTHS = {8, 12, 13, 14}


def is_valid_gtin(value: str) -> bool:
    value = re.sub(r"\.0$", "", str(value).strip())
    if not value.isdigit() or len(value) not in GTIN_LENGTHS:
        return False

    digits = [int(character) for character in value]
    check_digit = digits.pop()
    weighted_sum = sum(
        digit * (3 if offset % 2 == 0 else 1)
        for offset, digit in enumerate(reversed(digits))
    )
    return (10 - weighted_sum % 10) % 10 == check_digit


def is_supplier_internal_code(value: str) -> bool:
    digits = re.sub(r"\D", "", str(value or "").strip())
    return bool(digits) and (
        len(digits) not in GTIN_LENGTHS
        or digits.startswith("990")
    )


def gtin_check_digit(value: str) -> str:
    digits = [int(character) for character in str(value).strip()]
    weighted_sum = sum(
        digit * (3 if offset % 2 == 0 else 1)
        for offset, digit in enumerate(reversed(digits))
    )
    return str((10 - weighted_sum % 10) % 10)


def tester_mask(df: pd.DataFrame) -> pd.Series:
    mask = pd.Series(False, index=df.index)
    fields = [
        column
        for column in ("condition", "title", "description")
        if column in df.columns
    ]
    for field in fields:
        values = df[field].astype(str).str.casefold()
        for pattern in TESTER_PATTERNS:
            mask |= values.str.contains(
                rf"(?<![a-z]){re.escape(pattern)}(?![a-z])",
                regex=True,
                na=False,
            )
    return mask


def recover_gtin(value: str) -> str:
    value = re.sub(r"\.0$", "", str(value).strip())
    if is_valid_gtin(value):
        return value
    # Supplier exports can strip one or two leading zeroes from UPC-A values.
    # Shorter values are not padded because internal product codes would then
    # produce too many accidental checksum matches.
    if len(value) in {10, 11}:
        candidate = value.zfill(12)
        if is_valid_gtin(candidate):
            return candidate
    # Some supplier exports omit the final check digit instead of stripping a
    # leading zero. Eleven digits form a UPC-A body and twelve digits form an
    # EAN-13 body, so appending the calculated digit is unambiguous.
    if len(value) in {11, 12} and value.isdigit():
        candidate = f"{value}{gtin_check_digit(value)}"
        if is_valid_gtin(candidate):
            return candidate
    return ""


def drop_garbage_columns(df: pd.DataFrame) -> pd.DataFrame:
    columns_to_drop = []

    for column in df.columns:
        column_str = str(column).strip().lower()

        if column_str.startswith("unnamed"):
            columns_to_drop.append(column)
            continue

        column_data = df[column]

        # duplicate column names return DataFrame
        if isinstance(column_data, pd.DataFrame):
            continue

        if column_data.isna().all():
            columns_to_drop.append(column)
            continue

    return df.drop(columns=columns_to_drop)


def clean_ean(value) -> str:
    if pd.isna(value):
        return ""

    value = str(value).strip()

    if value.endswith(".0"):
        value = value[:-2]

    value = re.sub(r"[^0-9]", "", value)

    recovered = recover_gtin(value)
    if recovered:
        return recovered

    return value


def clean_row_ean(value, title) -> str:
    cleaned = clean_ean(value)
    title_text = str(title or "").lower()
    if (
        "tester" in title_text
        and cleaned.endswith("1")
        and len(cleaned) in {13, 14}
        and not is_valid_gtin(cleaned)
        and is_valid_gtin(cleaned[:-1])
    ):
        return cleaned[:-1]
    return cleaned


def clean_price(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    value = value.replace("€", "")
    value = value.replace("EUR", "")
    value = value.replace("eur", "")
    value = value.replace(" ", "")

    if "," in value and "." in value:
        last_comma = value.rfind(",")
        last_dot = value.rfind(".")

        if last_comma > last_dot:
            value = value.replace(".", "")
            value = value.replace(",", ".")
        else:
            value = value.replace(",", "")
    elif "," in value:
        value = value.replace(",", ".")

    try:
        return float(value)
    except ValueError:
        return None


def clean_msrp(value):
    return clean_price(value)


def clean_stock(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value == "":
        return None

    if value.endswith(".0"):
        value = value[:-2]

    value = re.sub(r"[^0-9]", "", value)

    if value == "":
        return None

    return int(value)


def clean_integer(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value == "":
        return None

    # handles "936.0", "936,0", "12 pcs"
    value = value.replace(",", ".")
    match = re.search(r"\d+(\.\d+)?", value)

    if not match:
        return None

    return int(float(match.group()))


def clean_lead_time(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value == "":
        return None

    match = re.search(r"\d+", value)

    if not match:
        return None

    return int(match.group())


def clean_weight(value):
    if pd.isna(value):
        return None

    value = str(value).strip().lower()

    value = value.replace("kg", "")
    value = value.replace(",", ".")

    value = re.sub(r"[^0-9.]", "", value)

    if value == "":
        return None

    try:
        return float(value)
    except ValueError:
        return None


def clean_vat_rate(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    value = value.replace("%", "")
    value = value.replace(",", ".")

    value = re.sub(r"[^0-9.]", "", value)

    if value == "":
        return None

    try:
        return float(value)
    except ValueError:
        return None


def is_present(value) -> bool:
    if pd.isna(value):
        return False

    return str(value).strip() != ""


def first_present(values):
    for value in values:
        if is_present(value):
            return value

    return ""


def first_valid_ean(values):
    first_value = first_present(values)

    for value in values:
        cleaned = clean_ean(value)

        if 8 <= len(cleaned) <= 14:
            return value

    return first_value


def first_valid_price(values):
    first_value = first_present(values)

    for value in values:
        cleaned = clean_price(value)

        if cleaned is not None:
            return value

    return first_value


def merge_duplicate_columns(df: pd.DataFrame) -> pd.DataFrame:
    merged_columns = []
    seen = set()

    for position, column in enumerate(df.columns):
        if column in seen:
            continue
        seen.add(column)
        matching = df.loc[:, df.columns == column]

        if matching.shape[1] == 1 or not str(column).strip():
            merged = df.iloc[:, position]
        elif column == "ean":
            merged = matching.apply(
                lambda row: first_valid_ean(row.tolist()),
                axis=1,
            )
        elif column == "price":
            merged = matching.apply(
                lambda row: first_valid_price(row.tolist()),
                axis=1,
            )
        else:
            merged = matching.apply(
                lambda row: first_present(row.tolist()),
                axis=1,
            )

        merged_columns.append(merged.rename(column))

    return pd.concat(merged_columns, axis=1)


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = drop_garbage_columns(df)

    df = merge_duplicate_columns(df)
    non_empty_rows = df.apply(
        lambda row: any(is_present(value) for value in row),
        axis=1,
    )
    df = df.loc[non_empty_rows].copy()

    price_like_columns = {"price", "msrp"}
    descriptive_columns = [
        column
        for column in df.columns
        if column not in price_like_columns
    ]
    if descriptive_columns:
        has_product_data = df[descriptive_columns].apply(
            lambda row: any(is_present(value) for value in row),
            axis=1,
        )
        price_values = pd.Series(None, index=df.index, dtype=object)
        for column in price_like_columns & set(df.columns):
            cleaned_values = df[column].apply(clean_price)
            price_values = price_values.where(
                price_values.notna(),
                cleaned_values,
            )
        zero_price_only = ~has_product_data & price_values.fillna(0).eq(0)
        df = df.loc[~zero_price_only].copy()

    if "ean" in df.columns:
        if "title" in df.columns:
            df["ean"] = df.apply(
                lambda row: clean_row_ean(row["ean"], row["title"]),
                axis=1,
            )
        else:
            df["ean"] = df["ean"].apply(clean_ean)

    if "price" in df.columns:
        df["price"] = df["price"].apply(clean_price)

    if "ean" in df.columns and "price" in df.columns:
        has_ean_or_price = df.apply(
            lambda row: (
                is_present(row["ean"])
                or is_present(row["price"])
            ),
            axis=1,
        )
        df = df.loc[has_ean_or_price].copy()

    if "msrp" in df.columns:
        df["msrp"] = df["msrp"].apply(clean_msrp)

    if "stock" in df.columns:
        df["stock"] = df["stock"].apply(clean_stock)

    for column in [
        "units_per_box",
        "boxes_per_pallet",
        "units_per_pallet",
    ]:
        if column in df.columns:
            df[column] = df[column].apply(clean_integer)

    if "lead_time_days" in df.columns:
        df["lead_time_days"] = df["lead_time_days"].apply(clean_lead_time)

    if "weight" in df.columns:
        df["weight"] = df["weight"].apply(clean_weight)

    if "vat_rate" in df.columns:
        df["vat_rate"] = df["vat_rate"].apply(clean_vat_rate)

    df["offer_type"] = ""
    df.loc[tester_mask(df), "offer_type"] = "tester"

    df = df.fillna("")

    return df
