def detect_recurring_expenses(df):
    df = df[df["amount"] < 0].copy()
    df["amount"] = df["amount"].abs()

    df["merchant"] = (
        df["description"].astype(str).str.lower().str.strip()
    )

    recurring = []

    for merchant, group in df.groupby("merchant"):
        group = group.sort_values("date")

        if len(group) < 2:
            continue

        gaps = group["date"].diff().dt.days.dropna()
        average_gap = gaps.mean()

        if 25 <= average_gap <= 35:
            recurring.append({
                "description": merchant,
                "frequency": "Monthly",
                "occurrences": len(group),
                "average_amount": round(
                    float(group["amount"].mean()), 2
                ),
                "total_amount": float(group["amount"].sum())
            })

    return recurring