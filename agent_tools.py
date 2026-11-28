
import json
from io import StringIO
from contextvars import ContextVar
from datetime import date

import pandas as pd

from langchain_core.tools import tool
from backend.engine import run_finwise


DATA_FILE = "data/transactions.csv"


# =====================================================
# LIVE FRONTEND DATA CONTEXT
# =====================================================

live_transactions = ContextVar(
    "live_transactions",
    default=None
)

live_monthly_budget = ContextVar(
    "live_monthly_budget",
    default=None
)


def get_data_source():

    data = live_transactions.get()

    if data is not None:
        return StringIO(data)

    return DATA_FILE


# =====================================================
# TRANSACTION ANALYSIS
# =====================================================

@tool
def analyze_transactions(monthly_income: float) -> str:
    """Analyze transaction data and identify spending patterns."""

    result = run_finwise(
        get_data_source(),
        monthly_income
    )

    return json.dumps(
        result["analysis"],
        default=str
    )


# =====================================================
# SUBSCRIPTION DETECTION
# =====================================================

@tool
def detect_subscriptions(monthly_income: float) -> str:
    """Identify recurring expenses and subscriptions."""

    result = run_finwise(
        get_data_source(),
        monthly_income
    )

    return json.dumps(
        result["recurring_expenses"],
        default=str
    )


# =====================================================
# UNUSUAL EXPENSE DETECTION
# =====================================================

@tool
def identify_unusual_expenses(monthly_income: float) -> str:
    """Identify unusual spending from transaction data."""

    result = run_finwise(
        get_data_source(),
        monthly_income
    )

    return json.dumps(
        result["anomalies"],
        default=str
    )


# =====================================================
# BUDGET PLANNING
# =====================================================

@tool
def create_budget_plan(monthly_income: float) -> str:
    """Generate a budget plan using actual transaction data."""

    result = run_finwise(
        get_data_source(),
        monthly_income
    )

    return json.dumps(
        result["budget"],
        default=str
    )


# =====================================================
# REMAINING MONTHLY BUDGET
# =====================================================

@tool
def calculate_remaining_budget() -> str:
    """Calculate remaining monthly budget using live frontend data."""

    budget = live_monthly_budget.get()

    if budget is None:

        return json.dumps({
            "error": "Monthly budget is unavailable."
        })

    try:

        df = pd.read_csv(get_data_source())

        required_columns = {"date", "amount"}

        if not required_columns.issubset(df.columns):

            return json.dumps({
                "error": "Transaction data has an invalid format."
            })

        if df.empty:

            spending = 0.0

        else:

            df["date"] = pd.to_datetime(
                df["date"],
                errors="coerce"
            )

            df["amount"] = pd.to_numeric(
                df["amount"],
                errors="coerce"
            )

            today = date.today()

            monthly = df[
                (df["date"].dt.month == today.month) &
                (df["date"].dt.year == today.year)
            ]

            # Expenses are represented by negative amounts.
            spending = abs(
                monthly.loc[
                    monthly["amount"] < 0,
                    "amount"
                ].sum()
            )

        remaining = float(budget) - float(spending)

        result = {
            "monthly_budget": round(float(budget), 2),
            "monthly_spending": round(float(spending), 2),
            "remaining_budget": round(remaining, 2),
            "status": (
                "Within budget"
                if remaining >= 0
                else "Over budget"
            )
        }

        return json.dumps(result)

    except Exception as error:

        return json.dumps({
            "error": f"Budget calculation failed: {str(error)}"
        })
