import math
from numbers import Real


def generate_budget(monthly_income, total_spending):

    if (
        isinstance(monthly_income, bool)
        or not isinstance(monthly_income, Real)
        or not math.isfinite(monthly_income)
    ):
        raise ValueError("Income must be a valid number")

    if (
        isinstance(total_spending, bool)
        or not isinstance(total_spending, Real)
        or not math.isfinite(total_spending)
    ):
        raise ValueError("Total spending must be a valid number")

    if monthly_income <= 0:
        raise ValueError("Income must be greater than zero")

    if total_spending < 0:
        raise ValueError("Total spending cannot be negative")

    needs = monthly_income * 0.50
    wants = monthly_income * 0.30
    savings = monthly_income * 0.20

    remaining = monthly_income - total_spending

    return {
        "monthly_income": round(monthly_income, 2),
        "needs_budget": round(needs, 2),
        "wants_budget": round(wants, 2),
        "savings_goal": round(savings, 2),
        "total_spending": round(total_spending, 2),
        "remaining_balance": round(remaining, 2),
        "budget_status": (
            "Over Budget"
            if total_spending > needs + wants
            else "Within Budget"
        )
    }
