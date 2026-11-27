def analyze_spending(df):
    expenses = df[df["amount"] < 0].copy()
    income = df[df["amount"] > 0].copy()

    expenses["amount"] = expenses["amount"].abs()

    total_spending = expenses["amount"].sum()
    total_income = income["amount"].sum()

    category_spending = (
        expenses.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    average_spending = (
        expenses["amount"].mean()
        if not expenses.empty else 0
    )

    highest_category = (
        category_spending.idxmax()
        if not category_spending.empty
        else "None"
    )

    return {
        "total_spending": float(total_spending),
        "total_income": float(total_income),
        "net_balance": float(total_income - total_spending),
        "average_spending": float(average_spending),
        "total_transactions": len(df),
        "expense_transactions": len(expenses),
        "income_transactions": len(income),
        "category_spending": category_spending.to_dict(),
        "highest_category": highest_category
    }