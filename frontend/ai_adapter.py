import math
import pandas as pd

COLUMNS = ["date", "description", "category", "amount"]


def build_user_transactions(expenses):
    records = []

    for expense in expenses:
        amount = float(expense["Amount"])

        if not math.isfinite(amount) or amount <= 0:
            raise ValueError("Invalid expense amount")

        records.append({
            "date": expense["Date"],
            "description": expense["Name"],
            "category": expense["Category"],
            "amount": -amount
        })

    return pd.DataFrame(records, columns=COLUMNS)


def get_ai_answer(question, expenses):
    from agents import run_agent

    transactions = build_user_transactions(expenses)

    result = run_agent(
        question,
        return_trace=True,
        transactions=transactions
    )

    return result
