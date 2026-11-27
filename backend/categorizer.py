CATEGORY_RULES = {
    "Food": ["swiggy", "zomato", "restaurant", "cafe", "food"],
    "Transport": ["uber", "ola", "rapido", "fuel", "metro"],
    "Shopping": ["amazon", "flipkart", "myntra"],
    "Entertainment": ["cinema", "movie", "gaming"],
    "Subscriptions": ["netflix", "spotify", "prime"],
    "Education": ["college", "course", "books", "fees"],
    "Groceries": ["blinkit", "zepto", "bigbasket"],
    "Health": ["hospital", "pharmacy", "medicine"],
    "Utilities": ["electricity", "wifi", "recharge"],
    "Rent": ["rent"]
}


def categorize_transaction(description):
    description = str(description).lower()

    for category, keywords in CATEGORY_RULES.items():
        if any(word in description for word in keywords):
            return category

    return "Other"


def categorize_transactions(df):
    df = df.copy()
    df["category"] = df["description"].apply(
        categorize_transaction
    )
    return df