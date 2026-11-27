
import json
import calendar

from langchain_core.tools import tool

from backend.engine import run_finwise
from backend.transactions import load_transactions
from backend.categorizer import categorize_transactions
from backend.analysis import analyze_spending
from backend.recurring import detect_recurring_expenses
from backend.anomaly import detect_anomalies


DATA_FILE = "data/transactions.csv"


def get_transactions():

    df = load_transactions(DATA_FILE)

    return categorize_transactions(df)


@tool
def analyze_transactions(
    month: int = 0,
    year: int = 0
) -> str:
    """Analyze historical income, spending and balance.
    Month: 1 to 12, or 0 for all months.
    Year: four-digit year, or 0 for all years."""

    if not 0 <= month <= 12:
        raise ValueError("Month must be between 0 and 12.")

    if year != 0 and not 1900 <= year <= 9999:
        raise ValueError("Invalid year.")

    df = get_transactions()

    if month:
        df = df[df["date"].dt.month == month]

    if year:
        df = df[df["date"].dt.year == year]

    if df.empty:
        return json.dumps({
            "error": "No matching transactions.",
            "month": month,
            "year": year
        })

    result = analyze_spending(df)

    result["month"] = month
    result["year"] = year

    period = []

    if month:
        period.append(calendar.month_name[month])

    if year:
        period.append(str(year))

    result["period"] = (
        " ".join(period)
        if period else "Entire Dataset"
    )

    return json.dumps(result, default=str)


@tool
def detect_subscriptions() -> str:
    """Identify recurring subscription payments only."""

    df = get_transactions()

    categories = (
        df["category"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    subscription_df = df[
        categories.isin(["subscription", "subscriptions"])
        & (df["amount"] < 0)
    ].copy()

    result = detect_recurring_expenses(subscription_df)

    return json.dumps(result, default=str)


@tool
def detect_recurring_payments() -> str:
    """Identify all recurring expenses, including
    subscriptions, groceries and transport payments."""

    df = get_transactions()

    result = detect_recurring_expenses(df)

    return json.dumps(result, default=str)


@tool
def identify_unusual_expenses() -> str:
    """Identify unusual expenses from historical transactions."""

    df = get_transactions()

    result = detect_anomalies(df)

    return json.dumps(result, default=str)


@tool
def create_budget_plan(monthly_income: float) -> str:
    """Generate a monthly budget using the user's
    monthly income and actual transaction data."""

    if monthly_income <= 0:
        raise ValueError(
            "Monthly income must be greater than zero."
        )

    result = run_finwise(DATA_FILE, monthly_income)

    return json.dumps(result["budget"], default=str)
