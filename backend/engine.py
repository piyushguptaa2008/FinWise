
from backend.transactions import load_transactions
from backend.categorizer import categorize_transactions
from backend.analysis import analyze_spending
from backend.recurring import detect_recurring_expenses
from backend.anomaly import detect_anomalies
from backend.budget import generate_budget


def run_finwise(file, monthly_income):
    df = load_transactions(file)
    df = categorize_transactions(df)

    analysis = analyze_spending(df)
    recurring = detect_recurring_expenses(df)
    anomalies = detect_anomalies(df)

    latest_month = df["date"].max().to_period("M") if not df.empty else None

    monthly_spending = df.loc[
        (df["date"].dt.to_period("M") == latest_month)
        & (df["amount"] < 0),
        "amount"
    ].abs().sum() if not df.empty else 0

    budget = generate_budget(
        monthly_income,
        float(monthly_spending)
    )

    return {
        "transactions": df,
        "analysis": analysis,
        "recurring_expenses": recurring,
        "anomalies": anomalies,
        "budget": budget
    }
