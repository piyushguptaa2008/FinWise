
import re

# FinWise financial knowledge base
KNOWLEDGE_BASE = [
    {
        "id": "KB01",
        "topic": "Budgeting",
        "keywords": "monthly budget income expenses planning",
        "content": "Create a monthly budget based on income, essential expenses and savings goals."
    },
    {
        "id": "KB02",
        "topic": "Subscriptions",
        "keywords": "recurring subscriptions netflix spotify membership cancellation",
        "content": "Review recurring subscriptions and identify services that are no longer needed."
    },
    {
        "id": "KB03",
        "topic": "Unusual Spending",
        "keywords": "anomaly anomalies unusual suspicious large transactions",
        "content": "Compare unusually large transactions with historical spending patterns before drawing conclusions."
    },
    {
        "id": "KB04",
        "topic": "Food Expenses",
        "keywords": "food delivery restaurant grocery dining",
        "content": "Track food delivery, restaurant and grocery expenses separately to understand spending habits."
    },
    {
        "id": "KB05",
        "topic": "Savings",
        "keywords": "saving savings goals financial planning",
        "content": "Set realistic savings goals after accounting for essential monthly expenses."
    },
    {
        "id": "KB06",
        "topic": "Student Finance",
        "keywords": "student college university allowance pocket money",
        "content": "Students can manage monthly allowances by tracking daily expenses and planning upcoming purchases."
    },
    {
        "id": "KB07",
        "topic": "Impulse Buying",
        "keywords": "shopping impulse buying unnecessary purchases",
        "content": "Review optional purchases against the remaining budget before making spending decisions."
    },
    {
        "id": "KB08",
        "topic": "Transport",
        "keywords": "transport travel commute fuel transportation",
        "content": "Track recurring transport expenses and compare available travel alternatives."
    },
    {
        "id": "KB09",
        "topic": "50/30/20 Budgeting Rule",
        "keywords": "50 30 20 budgeting rule needs wants savings percentage allocation",
        "content": (
            "The 50/30/20 budgeting rule is a flexible guideline "
            "that allocates 50% of take-home income to essential "
            "needs, 30% to discretionary wants, and 20% to savings "
            "and additional debt repayment. These percentages "
            "can be adjusted according to individual circumstances."
        )
    },
    {
        "id": "KB10",
        "topic": "Emergency Fund",
        "keywords": "emergency fund unexpected expenses financial safety",
        "content": (
            "An emergency fund helps cover unexpected expenses. "
            "Build it gradually according to your income, "
            "essential expenses and personal circumstances."
        )
    },
    {
        "id": "KB11",
        "topic": "Expense Tracking",
        "keywords": "expense tracking categories transactions spending analysis",
        "content": (
            "Categorize transactions and review spending regularly "
            "to identify patterns and understand where money goes."
        )
    },
    {
        "id": "KB12",
        "topic": "Needs vs Wants",
        "keywords": "needs wants essential discretionary expenses",
        "content": (
            "Needs are essential expenses such as housing, food "
            "and necessary transportation. Wants are optional "
            "expenses such as entertainment and non-essential shopping."
        )
    },
    {
        "id": "KB13",
        "topic": "Budget Overspending",
        "keywords": "overspending overbudget reduce spending budget deficit",
        "content": (
            "When expenses exceed the available budget, review "
            "optional spending first while protecting essential needs."
        )
    },
    {
        "id": "KB14",
        "topic": "Cash Flow",
        "keywords": "cash flow income expenses balance surplus deficit",
        "content": (
            "Cash flow measures money received and money spent "
            "during a period. Positive cash flow means income "
            "exceeds expenses."
        )
    }
]


STOP_WORDS = {
    "a", "an", "the", "is", "are", "was",
    "were", "and", "or", "of", "to", "in",
    "on", "for", "with", "my", "me", "i",
    "you", "your", "how", "what", "can",
    "should", "please", "explain", "search",
    "using", "use", "knowledge", "base",
    "financial", "about", "tell", "from",
    "do", "does", "it", "be", "this", "that"
}


def tokenize(text):

    words = set(
        re.findall(r"\b\w+\b", text.lower())
    )

    return words - STOP_WORDS


def retrieve_context(query, top_k=3):

    query_words = tokenize(query)

    if not query_words:
        return []

    results = []

    for document in KNOWLEDGE_BASE:

        topic_words = tokenize(document["topic"])

        keyword_words = tokenize(
            document.get("keywords", "")
        )

        content_words = tokenize(
            document["content"]
        )

        # Give more importance to topics and keywords
        score = (
            4 * len(query_words & topic_words)
            + 3 * len(query_words & keyword_words)
            + len(query_words & content_words)
        )

        if score > 0:
            results.append((score, document))

    results.sort(
        key=lambda item: item[0],
        reverse=True
    )

    if not results:
        return []

    # Remove weakly related documents
    best_score = results[0][0]

    filtered = [
        document
        for score, document in results
        if score >= max(2, best_score * 0.35)
    ]

    return filtered[:top_k]


if __name__ == "__main__":

    queries = [
        "Explain the 50/30/20 budgeting rule.",
        "How can I reduce recurring subscriptions?",
        "What is an emergency fund?",
        "How can students manage their allowance?"
    ]

    for query in queries:

        print("\nQuery:", query)
        print("-" * 45)

        results = retrieve_context(query)

        for result in results:

            print(result["id"], result["topic"])
            print(result["content"])
            print()
