from transaction_context import transaction_context


import re
import json
import math

from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from model_config import get_model
from rag import retrieve_context

from intent_router import (
    identify_required_tools,
    extract_period
)

from tool_recovery import (
    recover_missing_tools,
    recover_calculation,
    extract_monthly_income
)

from agent_tools import (
    analyze_transactions,
    detect_subscriptions,
    detect_recurring_payments,
    identify_unusual_expenses,
    create_budget_plan
)


@tool
def search_financial_knowledge(query: str) -> str:
    """Retrieve relevant financial knowledge."""

    results = retrieve_context(query)

    if not results:
        return "No relevant knowledge found."

    return "\n".join(
        f"[{doc['id']}] {doc['content']}"
        for doc in results
    )


@tool
def calculate_remaining_balance(
    income: float,
    expenses: float
) -> float:
    """Calculate remaining balance in Indian rupees."""

    return round(income - expenses, 2)


def create_finwise_agent():

    model = get_model()

    tools = [
        search_financial_knowledge,
        calculate_remaining_balance,
        analyze_transactions,
        detect_subscriptions,
        detect_recurring_payments,
        identify_unusual_expenses,
        create_budget_plan
    ]

    return create_react_agent(model, tools=tools)


def verify_calculation(question, output):

    try:

        actual = float(output)

        if not math.isfinite(actual):
            return False

        expected = recover_calculation(question)

        if expected is None:
            return False

        return math.isclose(
            actual,
            float(expected),
            rel_tol=0,
            abs_tol=0.005
        )

    except (ValueError, TypeError):
        return False


def verify_tool_result(question, name, output):

    try:

        if name == "calculate_remaining_balance":

            return verify_calculation(
                question, output
            )

        if name == "search_financial_knowledge":

            return bool(
                re.findall(
                    r"\[(KB\d+)\]",
                    str(output)
                )
            )

        actual = (
            json.loads(output)
            if isinstance(output, str)
            else output
        )

        if isinstance(actual, dict) and "error" in actual:
            return False

        if name == "analyze_transactions":

            period = extract_period(question)

            expected = json.loads(
                analyze_transactions.invoke(period)
            )

        elif name == "detect_subscriptions":

            expected = json.loads(
                detect_subscriptions.invoke({})
            )

        elif name == "detect_recurring_payments":

            expected = json.loads(
                detect_recurring_payments.invoke({})
            )

        elif name == "identify_unusual_expenses":

            expected = json.loads(
                identify_unusual_expenses.invoke({})
            )

        elif name == "create_budget_plan":

            income = extract_monthly_income(question)

            if income is None or income <= 0:
                return False

            expected = json.loads(
                create_budget_plan.invoke({
                    "monthly_income": income
                })
            )

        else:
            return False

        if isinstance(expected, dict) and "error" in expected:
            return False

        return actual == expected

    except Exception:
        return False


def _run_agent(question, return_trace=False):

    required_tools = identify_required_tools(question)

    agent = create_finwise_agent()

    system_prompt = (
        "You are FinWise, an agentic personal finance assistant. "
        "Use tools for calculations and retrieval. "
        "Never invent financial data. "
        "Never assume income or expenses. "
        "Ask for missing financial information. "
        "Use the requested month and year for transaction analysis. "
        "Use month 0 and year 0 when no period is specified. "
        "Monthly budgets cover the latest dataset month. "
        "Distinguish subscriptions from general recurring expenses. "
        "Cite retrieved knowledge IDs. "
        "Provide educational budgeting guidance in INR. "
        "Never perform financial actions without human approval. "
        "Do not repeat successful tool calls. "
        "After receiving tool results, provide a final answer."
    )

    if required_tools:

        system_prompt += (
            "\nRequired tools: "
            + ", ".join(required_tools)
            + ". Execute every required tool before answering."
        )

    if "analyze_transactions" in required_tools:

        try:

            period = extract_period(question)

            system_prompt += (
                f"\nRequested analysis period: "
                f"month={period['month']}, "
                f"year={period['year']}."
            )

        except ValueError:
            pass

    result = agent.invoke({
        "messages": [
            ("system", system_prompt),
            ("user", question)
        ]
    })

    executed_tools = []
    recovered_tools = []
    rejected_tools = []
    knowledge_ids = set()
    tool_results = {}

    for message in result["messages"]:

        if message.type != "tool":
            continue

        name = message.name

        if getattr(message, "status", None) == "error":

            rejected_tools.append(name)
            continue

        if name in executed_tools:
            continue

        if name not in required_tools:

            rejected_tools.append(name)
            continue

        if not verify_tool_result(
            question, name, message.content
        ):

            rejected_tools.append(name)

            print("Rejected incorrect tool result:", name)

            continue

        executed_tools.append(name)

        tool_results[name] = message.content

        if name == "search_financial_knowledge":

            knowledge_ids.update(
                re.findall(
                    r"\[(KB\d+)\]",
                    str(message.content)
                )
            )

    missing_tools = [
        name for name in required_tools
        if name not in executed_tools
    ]

    if missing_tools:

        recovered = recover_missing_tools(
            question,
            missing_tools
        )

        for name, output in recovered.items():

            if not verify_tool_result(
                question, name, output
            ):
                continue

            recovered_tools.append(name)

            tool_results[name] = output

            if name == "search_financial_knowledge":

                knowledge_ids.update(
                    re.findall(
                        r"\[(KB\d+)\]",
                        str(output)
                    )
                )

    all_tools = list(dict.fromkeys(
        executed_tools + recovered_tools
    ))

    missing_tools = [
        name for name in required_tools
        if name not in all_tools
    ]

    validated = bool(required_tools) and not missing_tools

    answer = result["messages"][-1].content

    if missing_tools:

        answer = (
            "I could not complete the requested workflow. "
            "Please provide missing information or "
            "try a more specific request.\n\n"
            "Pending tools: "
            + ", ".join(missing_tools)
        )

    elif not required_tools:

        answer = (
            "I can analyze transactions, calculate balances, "
            "detect subscriptions and recurring payments, "
            "identify unusual expenses, retrieve financial "
            "knowledge and generate budget proposals. "
            "What would you like to explore?"
        )

    else:

        sections = []

        if "calculate_remaining_balance" in tool_results:

            balance = float(
                tool_results["calculate_remaining_balance"]
            )

            sections.append(
                f"Your remaining balance is ₹{balance:,.2f}."
            )

        labels = {
            "analyze_transactions": "Transaction Analysis",
            "detect_subscriptions": "Recurring Subscriptions",
            "detect_recurring_payments": "Recurring Expenses",
            "identify_unusual_expenses": "Unusual Expenses",
            "create_budget_plan": "Monthly Budget"
        }

        for name, label in labels.items():

            if name not in tool_results:
                continue

            raw = tool_results[name]

            try:

                data = (
                    json.loads(raw)
                    if isinstance(raw, str)
                    else raw
                )

                if name == "analyze_transactions":

                    label += (
                        " (" + data["period"] + ")"
                    )

                formatted = json.dumps(
                    data,
                    indent=2,
                    ensure_ascii=False
                )

            except (ValueError, TypeError, KeyError):

                formatted = str(raw)

            sections.append(
                label + ":\n" + formatted
            )

        if "search_financial_knowledge" in tool_results:

            sections.append(
                "Financial Knowledge:\n"
                + str(tool_results["search_financial_knowledge"])
            )

        if sections:

            answer = "\n\n".join(sections)

        if "create_budget_plan" in tool_results:

            answer += (
                "\n\nReview this budget proposal "
                "before approving it."
            )

        if knowledge_ids:

            answer += (
                "\n\nRetrieved knowledge sources: "
                + ", ".join(sorted(knowledge_ids))
            )

    print("\n--- Agent Execution Trace ---")
    print("Required tools:", required_tools)
    print("AI executed tools:", executed_tools)
    print("Rejected tools:", rejected_tools)
    print("Recovered tools:", recovered_tools)
    print("Missing tools:", missing_tools)
    print("Knowledge sources:", sorted(knowledge_ids))
    print(
        "Validation:",
        "PASSED" if validated else "INCOMPLETE"
    )
    print("-----------------------------")

    if return_trace:

        return {
            "answer": answer,
            "tools_used": all_tools if validated else [
                name for name in all_tools
                if name != "create_budget_plan"
            ],
            "required_tools": required_tools,
            "executed_tools": executed_tools,
            "rejected_tools": rejected_tools,
            "recovered_tools": recovered_tools,
            "missing_tools": missing_tools,
            "knowledge_sources": sorted(knowledge_ids),
            "validated": validated
        }

    return answer



def run_agent(
    question,
    return_trace=False,
    transactions=None
):
    with transaction_context(transactions):
        return _run_agent(
            question,
            return_trace=return_trace
        )
