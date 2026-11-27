def detect_anomalies(df):
    if len(df) < 3:
        return []

    mean_amount = df["amount"].mean()
    std_amount = df["amount"].std()

    threshold = mean_amount + (2 * std_amount)

    anomalies = df[df["amount"] > threshold]

    results = []

    for _, row in anomalies.iterrows():
        results.append({
            "date": str(row["date"].date()),
            "description": row["description"],
            "amount": float(row["amount"]),
            "category": row["category"],
            "reason": "Unusually high spending"
        })

    return results