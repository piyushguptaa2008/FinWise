import re


def identify_required_tools(question):

    # Route only the actual user question, not frontend instructions
    question = question.rsplit("User question: ", 1)[-1]
    question = question.lower().strip()

    required_tools = []

    patterns = {

        "analyze_transactions": [
            r"\banaly[sz]e\b.*\btransactions?\b",
            r"\bspending patterns?\b",
            r"\btransaction analysis\b",
            r"\bspending summary\b",
            r"\bwhere am i spending\b",
            r"\bhighest spending\b"
        ],

        "detect_subscriptions": [
            r"\bdetect subscriptions?\b",
            r"\bidentify recurring expenses\b",
            r"\bfind subscriptions?\b",
            r"\brecurring payments?\b"
        ],

        "identify_unusual_expenses": [
            r"\banomalies\b",
            r"\bunusual (expenses|spending)\b",
            r"\bsuspicious transactions?\b"
        ],

        "create_budget_plan": [
            r"\b(create|generate|prepare|make)\b.*\bbudget\b",
            r"\bbudget plan\b",
            r"\bbudget recommendation\b"
        ],

        "calculate_remaining_balance": [
            r"\bremaining balance\b",
            r"\bcalculate\b.*\bbalance\b",
            r"\bmoney left\b"
        ],

        "calculate_remaining_budget": [
            r"\bbudget.*\bleft\b",
            r"\bremaining\b.*\bbudget\b",
            r"\bbudget remaining\b",
            r"\bbudget balance\b",
            r"\bbudget.*\bremaining\b",
            r"\bbudget.*\bleftover\b",
            r"\bhow much.*\bbudget\b.*\bavailable\b",
            r"\bam i over budget\b",
            r"\bam i within budget\b"
        ],

        "search_financial_knowledge": [
            r"\bknowledge base\b",
            r"\bfinancial knowledge\b",
            r"\bbudgeting rule\b",
            r"\bfinancial advice\b",
            r"\b50.?30.?20\b"
        ]
    }

    for tool_name, expressions in patterns.items():

        if any(
            re.search(pattern, question)
            for pattern in expressions
        ):
            required_tools.append(tool_name)

    # Prefer the dedicated budget calculator
    # when the question explicitly concerns a budget.
    if "calculate_remaining_budget" in required_tools:

        if "calculate_remaining_balance" in required_tools:
            required_tools.remove(
                "calculate_remaining_balance"
            )

    return required_tools


if __name__ == "__main__":

    test_questions = [
        "Analyze transactions and create a budget plan",
        "Find subscriptions",
        "Identify unusual expenses",
        "Calculate my remaining balance",
        "Search the financial knowledge base",
        "How much budget do I have left?",
        "What is my remaining budget?",
        "Show my spending summary",
        "What is the 50/30/20 budgeting rule?",
        "Am I over budget?",
        "What is my budget balance?",
        "Hello",
        "Use calculate_remaining_budget tool.\nUser question: Find subscriptions"
    ]

    for question in test_questions:

        print("\nQuestion:", question)

        print(
            "Required tools:",
            identify_required_tools(question)
        )