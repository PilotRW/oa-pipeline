import re

import pandas as pd


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

    return value


def clean_price(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    value = value.replace("€", "")
    value = value.replace("EUR", "")
    value = value.replace("eur", "")
    value = value.replace(" ", "")
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


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = drop_garbage_columns(df)

    # remove duplicate columns after normalization
    df = df.loc[:, ~df.columns.duplicated()]

    if "ean" in df.columns:
        df["ean"] = df["ean"].apply(clean_ean)

    if "price" in df.columns:
        df["price"] = df["price"].apply(clean_price)

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

    df = df.fillna("")

    return df