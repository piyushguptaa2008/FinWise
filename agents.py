
import re
import json
import math

from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from model_config import get_model
from rag import retrieve_context
from intent_router import identify_required_tools
from tool_recovery import recover_missing_tools

from agent_tools import (
    analyze_transactions,
    detect_subscriptions,
    identify_unusual_expenses,
    create_budget_plan,
    calculate_remaining_budget
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
    income: float, expenses: float
) -> float:
    """Calculate remaining balance in Indian rupees."""

    return round(income - expenses, 2)



def format_financial_data(data, parent_key=""):

    if isinstance(data, list):

        if not data:
            return "No records found."

        return "\n\n".join(
            format_financial_data(item, parent_key)
            for item in data
        )

    if isinstance(data, dict):

        if not data:
            return "No records found."

        lines = []

        for key, value in data.items():

            label = key.replace("_", " ").title()

            if isinstance(value, (dict, list)):

                lines.append(
                    f"\\n**{label}**\\n".replace("\\n", "\n")
                )

                lines.append(
                    format_financial_data(value, key)
                )

            elif isinstance(value, bool):

                lines.append(f"- **{label}:** {value}")

            elif isinstance(value, (int, float)):

                money_words = (
                    "amount", "income", "budget",
                    "spending", "balance", "saving",
                    "expense", "cost", "price"
                )

                count_words = (
                    "count", "transactions", "frequency",
                    "percentage", "days", "months"
                )

                is_money = (
                    any(word in key.lower() for word in money_words)
                    or parent_key == "category_spending"
                )

                is_count = any(
                    word in key.lower()
                    for word in count_words
                )

                if is_money and not is_count:
                    value = f"₹{value:,.2f}"

                lines.append(f"- **{label}:** {value}")

            else:

                lines.append(f"- **{label}:** {value}")

        return "\n".join(lines)

    return str(data)


def format_financial_result(name, raw):

    try:
        data = json.loads(raw) if isinstance(raw, str) else raw

    except (ValueError, TypeError):
        return str(raw)

    if name == "detect_subscriptions" and not data:
        return "No recurring expenses were detected."

    if name == "identify_unusual_expenses" and not data:
        return "No unusual expenses were detected."

    return format_financial_data(data)


def create_finwise_agent(required_tools=None):

    model = get_model()

    tools = [
        search_financial_knowledge,
        calculate_remaining_balance,
        calculate_remaining_budget,
        analyze_transactions,
        detect_subscriptions,
        identify_unusual_expenses,
        create_budget_plan
    ]

    if set(required_tools or []) == {"search_financial_knowledge"}:
        tools = [search_financial_knowledge]

    return create_react_agent(model, tools=tools)


def run_agent(question, return_trace=False):

    required_tools = identify_required_tools(question)
    agent = create_finwise_agent(required_tools)

    system_prompt = (
        "You are FinWise, an agentic personal finance assistant. "
        "Use tools for calculations and retrieval. "
        "Never invent financial data. "
        "Ask for missing financial information. "
        "Transaction analysis covers the entire dataset. "
        "Monthly budget covers the latest month in the dataset. "
        "Cite retrieved knowledge IDs. "
        "Provide educational budgeting guidance in INR. "
        "Never perform financial actions without human approval. "
        "Do not repeat successful tool calls. "
        "Use only relevant tools. "
        "For remaining monthly budget questions, use calculate_remaining_budget. "
        "Remaining budget covers the current calendar month. "
        "Never confuse monthly budget with monthly income. "
        "After receiving tool results, provide a final answer."
    )

    if required_tools:
        system_prompt += (
            "\nRequired tools: "
            + ", ".join(required_tools)
            + ". Execute every required tool before answering."
        )

    result = agent.invoke({
        "messages": [
            ("system", system_prompt),
            ("user", question)
        ]
    })

    executed_tools = []
    recovered_tools = []
    knowledge_ids = set()
    tool_results = {}

    for message in result["messages"]:

        if message.type == "tool":

            if getattr(message, "status", None) == "error":
                continue

            if message.name == "calculate_remaining_budget":
                try:
                    data = json.loads(message.content)
                    if not isinstance(data, dict) or "error" in data:
                        continue
                    if not all(
                        key in data for key in (
                            "monthly_budget",
                            "monthly_spending",
                            "remaining_budget",
                            "status"
                        )
                    ):
                        continue
                except (ValueError, TypeError):
                    continue

            if message.name == "calculate_remaining_balance":

                try:
                    balance = float(message.content)

                    if not math.isfinite(balance):
                        continue

                except (ValueError, TypeError):
                    continue

            if message.name == "search_financial_knowledge":

                ids = re.findall(
                    r"\[(KB\d+)\]",
                    str(message.content)
                )

                if not ids:
                    continue

                knowledge_ids.update(ids)

            executed_tools.append(message.name)
            tool_results[message.name] = message.content

    missing_tools = [
        name for name in required_tools
        if name not in executed_tools
    ]

    # Automatic recovery
    if missing_tools:

        recovered = recover_missing_tools(
            question,
            missing_tools
        )

        for name, output in recovered.items():

            # Track recovered RAG citations
            if name == "search_financial_knowledge":

                ids = re.findall(
                    r"\[(KB\d+)\]",
                    str(output)
                )

                if not ids:
                    continue

                knowledge_ids.update(ids)

            recovered_tools.append(name)
            tool_results[name] = output

    all_tools = list(dict.fromkeys(
        executed_tools + recovered_tools
    ))

    missing_tools = [
        name for name in required_tools
        if name not in all_tools
    ]

    validated = not missing_tools

    answer = result["messages"][-1].content

    if not validated:

        answer = (
            "I could not complete the requested workflow. "
            "Please provide any missing information "
            "or try a more specific request."
            "\n\nPending tools: "
            + ", ".join(missing_tools)
        )

    else:

        sections = []

        # Grounded calculation result
        if "calculate_remaining_balance" in tool_results:

            balance = float(
                tool_results["calculate_remaining_balance"]
            )

            sections.append(
                f"Your remaining balance is ₹{balance:,.2f}."
            )

        if "calculate_remaining_budget" in tool_results:

            raw = tool_results["calculate_remaining_budget"]
            data = json.loads(raw) if isinstance(raw, str) else raw

            sections.append(
                "### Remaining Monthly Budget\n\n"
                f"- **Monthly budget:** ₹{data['monthly_budget']:,.2f}\n"
                f"- **Monthly spending:** ₹{data['monthly_spending']:,.2f}\n"
                f"- **Remaining budget:** ₹{data['remaining_budget']:,.2f}\n"
                f"- **Status:** {data['status']}"
            )

        # Grounded backend results
        labels = {
            "analyze_transactions":
                "Transaction Analysis (Entire Dataset)",
            "detect_subscriptions":
                "Recurring Expenses",
            "identify_unusual_expenses":
                "Unusual Expenses",
            "create_budget_plan":
                "Monthly Budget (Latest Dataset Month)"
        }

        for name, label in labels.items():

            if name in tool_results:

                formatted = format_financial_result(
                    name,
                    tool_results[name]
                )

                sections.append(
                    f"### {label}\n\n{formatted}"
                )

        # Grounded RAG results
        if "search_financial_knowledge" in tool_results:

            knowledge = str(
                tool_results["search_financial_knowledge"]
            )

            sections.append(
                "Financial Knowledge:\n" + knowledge
            )

        if sections:

            answer = "\n\n".join(sections)

        if "create_budget_plan" in tool_results:

            answer += (
                "\n\nReview this budget proposal "
                "before approving it."
            )

        if knowledge_ids:

            answer = str(answer) + (
                "\n\nRetrieved knowledge sources: "
                + ", ".join(sorted(knowledge_ids))
            )

    print("\n--- Agent Execution Trace ---")
    print("Required tools:", required_tools)
    print("AI executed tools:", executed_tools)
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
            "recovered_tools": recovered_tools,
            "missing_tools": missing_tools,
            "knowledge_sources": sorted(knowledge_ids),
            "validated": validated
        }

    return answer
