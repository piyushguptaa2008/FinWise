import pandas as pd


def load_transactions(file):
    df = pd.read_csv(file)

    df.columns = df.columns.str.strip().str.lower()

    required_columns = ["date", "description", "amount"]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing column: {column}")

    df["date"] = pd.to_datetime(df["date"], errors="raise")
    df["amount"] = pd.to_numeric(df["amount"], errors="raise")

    return df