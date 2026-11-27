def analyze_spending(df):
    total_spending = df["amount"].sum()

    category_spending = (
        df.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    average_spending = (
        df["amount"].mean() if not df.empty else 0
    )

    highest_category = (
        category_spending.idxmax()
        if not category_spending.empty
        else "None"
    )

    return {
        "total_spending": float(total_spending),
        "average_spending": float(average_spending),
        "total_transactions": len(df),
        "category_spending": category_spending.to_dict(),
        "highest_category": highest_category
    }