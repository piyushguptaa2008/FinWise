
import re
import math

from rag import retrieve_context

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

            # RAG recovery does not require income
            if name == "search_financial_knowledge":

                result = recover_financial_knowledge(
                    question
                )

                if result:
                    recovered[name] = result
                    print("Recovered tool:", name)

                continue

            # Backend tools require income
            if name in BACKEND_TOOLS:

                if income is None:
                    continue

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
        "Explain the 50/30/20 budgeting rule "
        "using the financial knowledge base."
    )

    results = recover_missing_tools(
        question,
        ["search_financial_knowledge"]
    )

    print(results)
