import re

# FinWise financial knowledge base
KNOWLEDGE_BASE = [
    {
        "id": "KB01",
        "topic": "Budgeting",
        "content": "Create a monthly budget based on income, essential expenses and savings goals."
    },
    {
        "id": "KB02",
        "topic": "Subscriptions",
        "content": "Review recurring subscriptions and identify services that are no longer needed."
    },
    {
        "id": "KB03",
        "topic": "Unusual Spending",
        "content": "Compare unusually large transactions with historical spending patterns before drawing conclusions."
    },
    {
        "id": "KB04",
        "topic": "Food Expenses",
        "content": "Track food delivery, restaurant and grocery expenses separately to understand spending habits."
    },
    {
        "id": "KB05",
        "topic": "Savings",
        "content": "Set realistic savings goals after accounting for essential monthly expenses."
    },
    {
        "id": "KB06",
        "topic": "Student Finance",
        "content": "Students can manage monthly allowances by tracking daily expenses and planning upcoming purchases."
    },
    {
        "id": "KB07",
        "topic": "Impulse Buying",
        "content": "Review optional purchases against the remaining budget before making spending decisions."
    },
    {
        "id": "KB08",
        "topic": "Transport",
        "content": "Track recurring transport expenses and compare available travel alternatives."
    }
]


def tokenize(text):
    return set(re.findall(r"\b\w+\b", text.lower()))


def retrieve_context(query, top_k=3):
    query_words = tokenize(query)
    results = []

    for document in KNOWLEDGE_BASE:
        text = document["topic"] + " " + document["content"]
        score = len(query_words & tokenize(text))

        if score > 0:
            results.append((score, document))

    results.sort(key=lambda item: item[0], reverse=True)

    return [document for score, document in results[:top_k]]


if __name__ == "__main__":
    query = "How can I reduce recurring subscriptions?"

    results = retrieve_context(query)

    print("FinWise RAG Retrieval")
    print("---------------------")

    for result in results:
        print(result["id"], result["topic"])
        print(result["content"])
        print()
