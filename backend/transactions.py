import pandas as pd
import numpy as np


def load_transactions(file):
    try:
        df = pd.read_csv(file)
    except pd.errors.EmptyDataError:
        raise ValueError("CSV file is empty")

    df.columns = df.columns.str.strip().str.lower()

    required_columns = ["date", "description", "amount"]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing column: {column}")

    for column in required_columns:
        if df[column].isna().any():
            raise ValueError(f"Missing value in column: {column}")

        if df[column].astype(str).str.strip().eq("").any():
            raise ValueError(f"Empty value in column: {column}")

    df["date"] = pd.to_datetime(df["date"], errors="raise")
    df["amount"] = pd.to_numeric(df["amount"], errors="raise")

    if df["date"].isna().any():
        raise ValueError("Invalid transaction date")

    if not np.isfinite(df["amount"]).all():
        raise ValueError("Invalid transaction amount")

    return df
