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


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = drop_garbage_columns(df)

    # remove duplicate columns after normalization
    df = df.loc[:, ~df.columns.duplicated()]

    if "ean" in df.columns:
        df["ean"] = df["ean"].apply(clean_ean)

    if "price" in df.columns:
        df["price"] = df["price"].apply(clean_price)

    if "stock" in df.columns:
        df["stock"] = df["stock"].apply(clean_stock)

    df = df.fillna("")

    return df