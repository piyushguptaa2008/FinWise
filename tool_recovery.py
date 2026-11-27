
import re
import math

from agent_tools import (
    analyze_transactions,
    detect_subscriptions,
    identify_unusual_expenses,
    create_budget_plan
)


BACKEND_TOOLS = {
    "analyze_transactions": analyze_transactions,
    "detect_subscriptions": detect_subscriptions,
    "identify_unusual_expenses": identify_unusual_expenses,
    "create_budget_plan": create_budget_plan
}


def extract_monthly_income(question):
    pattern = (
        r"\b(?:monthly\s+)?income"
        r"\s*(?:is|of|=|:)?\s*"
        r"(?:₹|rs\.?|inr)?\s*"
        r"(\d[\d,]*(?:\.\d+)?)"
        r"(?![\d,.])"
    )

    matches = re.findall(
        pattern, question.lower()
    )

    if len(matches) != 1:
        return None

    income = float(matches[0].replace(",", ""))

    if not math.isfinite(income) or income <= 0:
        return None

    return income


def recover_missing_tools(question, missing_tools):

    recovered = {}
    income = extract_monthly_income(question)

    if income is None:
        return recovered

    for name in missing_tools:

        if name not in BACKEND_TOOLS:
            continue

        try:
            result = BACKEND_TOOLS[name].invoke({
                "monthly_income": income
            })

            recovered[name] = result

            print("Recovered tool:", name)

        except Exception as error:
            print("Recovery failed:", name, error)

    return recovered


if __name__ == "__main__":

    question = (
        "Analyze transactions and create a "
        "monthly budget plan with an income "
        "of 15000 rupees."
    )

    results = recover_missing_tools(
        question,
        ["create_budget_plan"]
    )

    print(results)
