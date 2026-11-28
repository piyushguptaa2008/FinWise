
import re
import calendar


def extract_period(question):

    question = question.lower()

    months = [
        number for number in range(1, 13)
        if re.search(
            rf"\b{calendar.month_name[number].lower()}\b",
            question
        )
    ]

    years = list(set(
        re.findall(r"\b20\d{2}\b", question)
    ))

    if len(months) > 1 or len(years) > 1:
        raise ValueError(
            "Please specify a single month and year."
        )

    return {
        "month": months[0] if months else 0,
        "year": int(years[0]) if years else 0
    }


def identify_required_tools(question):

    question = question.lower()
    required_tools = []

    patterns = {

        "analyze_transactions": [
            r"\banaly[sz]e\b.*\btransactions?\b",
            r"\bspending patterns?\b",
            r"\btransaction analysis\b",
            r"\btotal income\b",
            r"\btotal spending\b",
            r"\btotal expenses?\b",
            r"\bhow much.*\b(spent|spend|earned)\b",
            r"\bmonthly spending\b",
            r"\bfinancial summary\b",

            # Category-wise spending analysis
            r"\bwhich category\b.*\b(most|highest|largest|costs?|spending|spend)\b",
            r"\bwhich categories\b",
            r"\b(category|categories)\b.*\b(highest|most|top|largest)\b",
            r"\btop spending categor(?:y|ies)\b",
            r"\bwhere\b.*\b(spend|spending)\b",
            r"\bmost\b.*\b(spending|spent|expenses?)\b",
            r"\bhighest spending\b",
            r"\bbreakdown\b.*\bexpenses?\b",
            r"\bexpenses?\b.*\bby category\b",
            r"\bcategory[- ]wise spending\b",
            r"\bshow.*\bmy expenses\b"
        ],

        "detect_subscriptions": [
            r"\bsubscriptions?\b"
        ],

        "detect_recurring_payments": [
            r"\brecurring expenses?\b",
            r"\brecurring payments?\b",
            r"\brecurring transactions?\b"
        ],

        "identify_unusual_expenses": [
            r"\banomalies\b",
            r"\bunusual (expenses|spending|transactions)\b",
            r"\bsuspicious transactions?\b"
        ],

        "create_budget_plan": [
            r"\b(create|generate|prepare|make)\b.*\bbudget\b",
            r"\bbudget plan\b"
        ],

        "calculate_remaining_balance": [
            r"\bremaining balance\b",
            r"\bcalculate\b.*\bbalance\b",
            r"\bmoney left\b",
            r"\bnet balance\b",
            r"\bmy balance\b",
            r"\bhow much.*\bleft\b"
        ],

        "search_financial_knowledge": [
            r"\bknowledge base\b",
            r"\bfinancial knowledge\b",
            r"\bbudgeting rule\b",
            r"\bfinancial advice\b",
            r"\b50\s*/\s*30\s*/\s*20\b"
        ]
    }

    for tool_name, expressions in patterns.items():

        if any(
            re.search(pattern, question)
            for pattern in expressions
        ):
            required_tools.append(tool_name)

    has_month = any(
        re.search(
            rf"\b{calendar.month_name[number].lower()}\b",
            question
        )
        for number in range(1, 13)
    )

    has_year = bool(
        re.search(r"\b20\d{2}\b", question)
    )

    if (has_month or has_year) and re.search(
        r"\b(spending|expenses?|income|spent|spend|earned)\b",
        question
    ):

        if "analyze_transactions" not in required_tools:
            required_tools.append("analyze_transactions")

    return required_tools


if __name__ == "__main__":

    questions = [
        "What is my November spending?",
        "Show October 2026 expenses",
        "Show my total income and spending",
        "Show my recurring subscriptions",
        "Show all recurring expenses",
        "Calculate my remaining balance",
        "Explain the 50/30/20 budgeting rule",
        "Which category accounts for the most spending?",
        "Where am I spending the most?",
        "Show my expenses by category",
        "Which category costs me the most?"
    ]

    for question in questions:

        print("\nQuestion:", question)
        print("Tools:", identify_required_tools(question))
        print("Period:", extract_period(question))
