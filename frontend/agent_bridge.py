
import sys
from pathlib import Path
from io import StringIO

import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from agents import run_agent
from agent_tools import (
    live_transactions,
    live_monthly_budget
)


def get_live_transactions():

    expenses = st.session_state.get("expenses", [])

    rows = []

    for expense in expenses:

        rows.append({
            "date": str(expense["Date"]),
            "description": expense["Name"],
            "amount": -abs(float(expense["Amount"])),
            "category": expense["Category"]
        })

    return pd.DataFrame(
        rows,
        columns=["date", "description", "amount", "category"]
    )


def get_transaction_file():

    df = get_live_transactions()

    return StringIO(df.to_csv(index=False))


def get_financial_context():

    return {
        "monthly_budget": float(
            st.session_state.get("monthly_budget", 5000)
        ),
        "transactions": get_live_transactions()
    }


def ask_finwise(question):

    context = get_financial_context()

    transactions = context["transactions"]
    budget = context["monthly_budget"]

    transaction_token = live_transactions.set(
        transactions.to_csv(index=False)
    )

    budget_token = live_monthly_budget.set(budget)

    try:

        enriched_question = (
            f"User's monthly spending budget: ₹{budget:.2f}\n"
            "Use the live transaction data available through tools.\n"
            "For remaining budget questions, use the "
            "calculate_remaining_budget tool.\n"
            "Do not confuse monthly budget with monthly income.\n"
            f"User question: {question}"
        )

        result = run_agent(
            enriched_question,
            return_trace=True
        )

        return result

    finally:

        live_transactions.reset(transaction_token)
        live_monthly_budget.reset(budget_token)
