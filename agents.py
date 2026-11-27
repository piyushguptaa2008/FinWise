
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from rag import retrieve_context


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
        calculate_remaining_balance
    ]

    agent = create_react_agent(
        model,
        tools=tools
    )

    return agent


def run_agent(question):
    agent = create_finwise_agent()

    result = agent.invoke({
        "messages": [
            (
                "system",
                "You are FinWise, a personal finance assistant. "
                "Use available tools for calculations and retrieval. "
                "Cite retrieved knowledge IDs. "
                "Never invent financial data. "
                "Provide educational budgeting guidance in INR."
            ),
            ("user", question)
        ]
    })

    return result["messages"][-1].content


if __name__ == "__main__":
    print("Testing FinWise tools...")

    print(calculate_remaining_balance.invoke({
        "income": 10000,
        "expenses": 6750
    }))

    print(search_financial_knowledge.invoke({
        "query": "recurring subscriptions"
    }))

