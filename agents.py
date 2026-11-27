
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from rag import retrieve_context

from agent_tools import (
    analyze_transactions,
    detect_subscriptions,
    identify_unusual_expenses,
    create_budget_plan
)


@tool
def search_financial_knowledge(query: str) -> str:
    """Retrieve relevant financial knowledge for a user's question."""

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
    model = ChatOllama(
        model="qwen2.5:7b",
        base_url="http://localhost:11434",
        temperature=0
    )

    tools = [
        search_financial_knowledge,
        calculate_remaining_balance,
        analyze_transactions,
        detect_subscriptions,
        identify_unusual_expenses,
        create_budget_plan
    ]

    agent = create_react_agent(
        model,
        tools=tools
    )

    return agent


def run_agent(question, return_trace=False):
    agent = create_finwise_agent()

    result = agent.invoke({
        "messages": [
            (
                "system",
                "You are FinWise, a personal finance assistant. "
                "Use available tools for calculations and retrieval. "
                "Use backend tools when analyzing transaction data. "
                "Ask for monthly income if required and not provided. "
                "Cite retrieved knowledge IDs. "
                "Never invent financial data. "
                "Provide educational budgeting guidance in INR. "
                "Do not perform financial actions without user approval."
            ),
            ("user", question)
        ]
    })

    executed_tools = []

    for message in result["messages"]:
        if message.type == "tool":
            executed_tools.append(message.name)

    answer = result["messages"][-1].content

    print("\n--- Agent Execution Trace ---")

    if executed_tools:
        for name in executed_tools:
            print(f"Executed tool: {name}")
    else:
        print("No tools executed.")

    print("-----------------------------")

    if return_trace:
        return {
            "answer": answer,
            "tools_used": executed_tools
        }

    return answer


if __name__ == "__main__":
    print("Testing FinWise tools...")

    print(calculate_remaining_balance.invoke({
        "income": 10000,
        "expenses": 6750
    }))

    print(search_financial_knowledge.invoke({
        "query": "recurring subscriptions"
    }))
