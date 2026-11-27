
import re
import json

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
    income: float, expenses: float
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
        identify_unusual_expenses,
        create_budget_plan
    ]

    return create_react_agent(model, tools=tools)


def run_agent(question, return_trace=False):

    required_tools = identify_required_tools(question)
    agent = create_finwise_agent()

    system_prompt = (
        "You are FinWise, an agentic personal finance assistant. "
        "Use tools for calculations and retrieval. "
        "Never invent financial data. "
        "Ask for missing financial information. "
        "Transaction analysis covers the entire dataset. "
        "Monthly budget covers the latest month in the dataset. "
        "Cite retrieved knowledge IDs. "
        "Provide educational budgeting guidance in INR. "
        "Never perform financial actions without human approval."
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

            executed_tools.append(message.name)
            tool_results[message.name] = message.content

            if message.name == "search_financial_knowledge":
                ids = re.findall(
                    r"\[(KB\d+)\]",
                    str(message.content)
                )
                knowledge_ids.update(ids)

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

                raw = tool_results[name]

                try:
                    data = json.loads(raw)
                    formatted = json.dumps(
                        data,
                        indent=2,
                        ensure_ascii=False
                    )
                except (ValueError, TypeError):
                    formatted = str(raw)

                sections.append(
                    label + ":\n" + formatted
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
