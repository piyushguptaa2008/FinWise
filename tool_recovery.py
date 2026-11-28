
import re
import math

from rag import retrieve_context
from intent_router import extract_period
from backend.transactions import load_transactions

from agent_tools import (
    analyze_transactions,
    detect_subscriptions,
    detect_recurring_payments,
    identify_unusual_expenses,
    create_budget_plan
)


from transaction_context import get_transaction_source


BACKEND_TOOLS = {
    "analyze_transactions": analyze_transactions,
    "detect_subscriptions": detect_subscriptions,
    "detect_recurring_payments": detect_recurring_payments,
    "identify_unusual_expenses": identify_unusual_expenses,
    "create_budget_plan": create_budget_plan
}


def extract_amount(question, label):

    pattern = (
        rf"\b(?:{label})\b"
        r"\s*(?:is|are|of|=|:)?\s*"
        r"(?:₹|rs\.?|inr)?\s*"
        r"(\d[\d,]*(?:\.\d+)?)"
        r"(?![\d,]|\.\d)"
    )

    matches = re.findall(pattern, question.lower())

    if len(matches) != 1:
        return None

    amount = float(matches[0].replace(",", ""))

    if not math.isfinite(amount) or amount < 0:
        return None

    return amount


def extract_monthly_income(question):

    return extract_amount(question, "income")


def get_dataset_totals(question=""):

    df = load_transactions(get_transaction_source())

    period = extract_period(question)

    month = period["month"]
    year = period["year"]

    if month:
        df = df[df["date"].dt.month == month]

    if year:
        df = df[df["date"].dt.year == year]

    if df.empty:
        raise ValueError("No matching transactions.")

    income = float(
        df.loc[df["amount"] > 0, "amount"].sum()
    )

    expenses = float(
        df.loc[df["amount"] < 0, "amount"].abs().sum()
    )

    return {
        "income": income,
        "expenses": expenses,
        "balance": round(income - expenses, 2)
    }


def recover_calculation(question):

    income = extract_amount(question, "income")

    expenses = extract_amount(
        question,
        "expenses?|spending"
    )

    if income is not None and expenses is not None:
        return str(round(income - expenses, 2))

    if income is not None or expenses is not None:
        return None

    totals = get_dataset_totals(question)

    return str(totals["balance"])


def recover_financial_knowledge(question):

    results = retrieve_context(question)

    if not results:
        return None

    return "\n".join(
        f"[{doc['id']}] {doc['content']}"
        for doc in results
    )


def recover_missing_tools(question, missing_tools):

    recovered = {}

    income = extract_monthly_income(question)

    for name in missing_tools:

        try:

            if name == "calculate_remaining_balance":

                result = recover_calculation(question)

            elif name == "search_financial_knowledge":

                result = recover_financial_knowledge(
                    question
                )

            elif name == "analyze_transactions":

                period = extract_period(question)

                result = analyze_transactions.invoke({
                    "month": period["month"],
                    "year": period["year"]
                })

            elif name == "create_budget_plan":

                if income is None or income <= 0:
                    continue

                result = create_budget_plan.invoke({
                    "monthly_income": income
                })

            elif name in BACKEND_TOOLS:

                result = BACKEND_TOOLS[name].invoke({})

            else:
                continue

            if result is not None:

                recovered[name] = result

                print("Recovered tool:", name)

        except Exception as error:

            print("Recovery failed:", name, error)

    return recovered
