
import re


def identify_required_tools(question):
    question = question.lower()
    required_tools = []

    patterns = {
        "analyze_transactions": [
            r"\banaly[sz]e\b.*\btransactions?\b",
            r"\bspending patterns?\b",
            r"\btransaction analysis\b"
        ],
        "detect_subscriptions": [
            r"\bdetect subscriptions?\b",
            r"\bidentify recurring expenses\b",
            r"\bfind subscriptions?\b"
        ],
        "identify_unusual_expenses": [
            r"\banomalies\b",
            r"\bunusual (expenses|spending)\b",
            r"\bsuspicious transactions?\b"
        ],
        "create_budget_plan": [
            r"\b(create|generate|prepare|make)\b.*\bbudget\b",
            r"\bbudget plan\b"
        ],
        "calculate_remaining_balance": [
            r"\bremaining balance\b",
            r"\bcalculate\b.*\bbalance\b",
            r"\bmoney left\b"
        ],
        "search_financial_knowledge": [
            r"\bknowledge base\b",
            r"\bfinancial knowledge\b",
            r"\bbudgeting rule\b",
            r"\bfinancial advice\b"
        ]
    }

    for tool_name, expressions in patterns.items():
        if any(re.search(pattern, question)
               for pattern in expressions):
            required_tools.append(tool_name)

    return required_tools


if __name__ == "__main__":
    test_questions = [
        "Analyze transactions and create a budget plan",
        "Find subscriptions",
        "Identify unusual expenses",
        "Calculate my remaining balance",
        "Search the financial knowledge base",
        "Hello"
    ]

    for question in test_questions:
        print("\nQuestion:", question)
        print("Required tools:",
              identify_required_tools(question))
