
import json
from langchain_core.tools import tool
from backend.engine import run_finwise

DATA_FILE = "data/transactions.csv"


@tool
def analyze_transactions(monthly_income: float) -> str:
    """Analyze transaction data and identify spending patterns."""

    result = run_finwise(DATA_FILE, monthly_income)

    return json.dumps(result["analysis"], default=str)


@tool
def detect_subscriptions(monthly_income: float) -> str:
    """Identify recurring expenses and subscriptions."""

    result = run_finwise(DATA_FILE, monthly_income)

    return json.dumps(result["recurring_expenses"], default=str)


@tool
def identify_unusual_expenses(monthly_income: float) -> str:
    """Identify unusual spending from transaction data."""

    result = run_finwise(DATA_FILE, monthly_income)

    return json.dumps(result["anomalies"], default=str)


@tool
def create_budget_plan(monthly_income: float) -> str:
    """Generate a budget plan using actual transaction data."""

    result = run_finwise(DATA_FILE, monthly_income)

    return json.dumps(result["budget"], default=str)
