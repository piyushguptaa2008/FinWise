import streamlit as st
from storage import save_data
import pandas as pd
from datetime import date
import math

CATEGORIES = {
    "Food": ["zomato", "swiggy", "lunch", "coffee", "food"],
    "Travel": ["uber", "ola", "cab", "metro", "bus"],
    "Shopping": ["amazon", "flipkart", "clothes"],
    "Education": ["book", "college", "course"],
    "Bills": ["wifi", "electricity", "recharge"],
    "Entertainment": ["movie", "netflix", "spotify"],
    "Other": []
}


def detect_category(name):
    for category, words in CATEGORIES.items():
        if any(word in name.lower() for word in words):
            return category
    return "Other"


def show_expenses():
    s = st.session_state
    s.setdefault("expenses", [])
    s.setdefault("monthly_budget", 5000.0)

    dark = s.get("dark_mode", False)
    ink = "#e1ebcd" if dark else "#384536"
    surface = "#242e28" if dark else "#fffdf8"
    gradient = "#344438,#41394e" if dark else "#e3ebce,#e8e0f2"
    colors = ["#494535", "#41394e", "#344b36"] if dark else ["#f6ebcb", "#e8e0f2", "#e1ebcd"]

    text_color = "#e1ebcd" if dark else "#171717"
    input_bg = "#303e32" if dark else "#f0f2e7"

    st.markdown(f"""
<style>

/* Expense page text */

[data-testid="stMain"] h1,
[data-testid="stMain"] h2,
[data-testid="stMain"] h3,
[data-testid="stMain"] p,
[data-testid="stMain"] label,
[data-testid="stMain"] small {{
    color: {text_color} !important;
}}

/* Input fields */

[data-testid="stMain"] input,
[data-testid="stMain"] [data-baseweb="select"] > div {{
    background: {input_bg} !important;
    color: {text_color} !important;
    border-radius: 12px !important;
}}

[data-testid="stMain"] input::placeholder {{
    color: #899481 !important;
}}

/* Premium expense buttons */

[data-testid="stMain"] .stButton button {{
    background: linear-gradient(
        135deg, #dce8c9, #a8c686
    ) !important;
    color: #171717 !important;
    border: none !important;
    border-radius: 16px !important;
    min-height: 55px;
    font-size: 17px !important;
    font-weight: 700 !important;
    transition: all 0.3s ease;
}}

[data-testid="stMain"] .stButton button p {{
    color: #171717 !important;
    font-weight: 700 !important;
}}

[data-testid="stMain"] .stButton button:hover {{
    background: #b8d29d !important;
    transform: translateY(-3px);
    box-shadow: 0 8px 20px #91b47550;
}}

</style>
""", unsafe_allow_html=True)

    st.markdown(f'''
<div style="background:linear-gradient(120deg,{gradient});color:{ink};padding:32px;border-radius:26px;margin-bottom:12px">
<small style="letter-spacing:3px">SPENDING STUDIO</small>
<div style="font-size:clamp(30px,4vw,50px);font-weight:800;letter-spacing:-2px">Make your money make sense.</div>
<div>Track, understand and manage your spending.</div>
</div>
''', unsafe_allow_html=True)

    def add_expense():
        name = s.studio_name.strip()
        amount = float(s.studio_amount)

        if not name or not math.isfinite(amount) or amount <= 0:
            s.studio_message = (False, "Enter a name and a positive amount.")
            return

        cat = detect_category(name) if s.studio_category == "Auto detect" else s.studio_category

        s.expenses.append({
            "Name": name,
            "Amount": round(amount, 2),
            "Category": cat,
            "Date": s.studio_date
        })

        save_data()
        s.studio_message = (True, f"Added to {cat}.")
       
        s.studio_name = ""
        s.studio_amount = 0.0

    summary = st.container()

    left, right = st.columns([1, 1], gap="medium")

    with left:
        st.subheader("✦ Quick capture")

        name = st.text_input(
            "Expense name",
            placeholder="Zomato, Uber, Amazon...",
            key="studio_name"
        )

        st.caption(f"Suggested category: {detect_category(name)}")

        st.number_input(
            "Amount (₹)",
            min_value=0.0,
            step=10.0,
            key="studio_amount"
        )

        st.selectbox(
            "Category",
            ["Auto detect"] + list(CATEGORIES),
            key="studio_category"
        )

        st.date_input(
            "Date",
            value=date.today(),
            max_value=date.today(),
            key="studio_date"
        )

        st.button(
            "＋ Add expense",
            on_click=add_expense,
            use_container_width=True,
            key="studio_add"
        )

        if "studio_message" in s:
            ok, msg = s.studio_message
            (st.success if ok else st.warning)(msg)

        st.subheader("Budget control")

        budget = st.number_input(
            "Monthly limit (₹)",
            min_value=1.0,
            value=max(1.0, float(s.monthly_budget)),
            step=500.0,
            key="studio_budget"
        )

    if s.monthly_budget != budget:
        s.monthly_budget = budget
        save_data()

    df = pd.DataFrame(
        s.expenses,
        columns=["Name", "Amount", "Category", "Date"]
    )

    dates = pd.to_datetime(df["Date"], errors="coerce")
    today = date.today()

    monthly = df[
        (dates.dt.month == today.month) &
        (dates.dt.year == today.year)
    ]

    total = float(monthly["Amount"].sum())
    remaining = budget - total

    with summary:
        for col, label, value, color in zip(
            st.columns(3),
            ["Monthly spending", "Budget remaining", "Transactions"],
            [f"₹{total:,.2f}", f"₹{remaining:,.2f}", str(len(monthly))],
            colors
        ):
            col.markdown(f'''
<div style="background:{color};color:{ink};padding:24px;border-radius:20px">
<small>{label}</small>
<div style="font-size:26px;font-weight:800">{value}</div>
</div>
''', unsafe_allow_html=True)

    with left:

        progress = min(total / budget * 100, 100)

        track = "#354438" if dark else "#e1e8d5"

        fill = "#c77d70" if total > budget else "#91b475"

        st.html(f"""
<div style="
    width:100%;
    height:14px;
    background:{track};
    border-radius:20px;
    overflow:hidden;
    margin:12px 0;
">
    <div style="
        width:{progress}%;
        height:100%;
        background:{fill};
        border-radius:20px;
        transition:width 0.6s ease;
    "></div>
</div>
""")
        st.caption(f"{total / budget:.0%} of monthly budget used")

        if remaining < 0:
            st.warning(f"Over budget by ₹{-remaining:,.2f}")

    with right:
        st.subheader("Where it goes")

        spending = monthly.groupby("Category")["Amount"].sum().sort_values(ascending=False)

        palette = [
            "#e9d7a4", "#a9c692", "#cbb9e2",
            "#a9ccc5", "#dfbfc5", "#c5c9a5", "#a8a4bc"
        ]

        stops = []
        start = 0.0

        if total > 0:
            for i, value in enumerate(spending):
                end = start + float(value) / total * 100
                stops.append(
                    f"{palette[i % len(palette)]} {start}% {end}%"
                )
                start = end

        ring = ",".join(stops) if stops else "#aab5a333 0% 100%"

        st.markdown(f'''
<div style="background:conic-gradient({ring});width:220px;max-width:100%;aspect-ratio:1;border-radius:50%;display:grid;place-items:center;margin:20px auto">
<div style="background:{surface};color:{ink};width:70%;height:70%;border-radius:50%;display:grid;place-content:center;text-align:center">
<b style="font-size:24px">₹{total:,.0f}</b>
<small>This month</small>
</div>
</div>
''', unsafe_allow_html=True)

        for category, value in spending.items():
            st.write(f"{category} — ₹{value:,.2f}")

        if not spending.empty:
            st.info(f"Smart insight: {spending.index[0]} is your biggest spending category.")
        else:
            st.caption("Add an expense to see your spending breakdown.")

    st.divider()

    st.subheader("Transaction activity")

    search = st.text_input(
        "Search transactions",
        key="studio_search"
    )

    category = st.selectbox(
        "Filter category",
        ["All"] + list(CATEGORIES),
        key="studio_filter"
    )

    visible = df[
        df["Name"].astype(str).str.contains(
            search, case=False, regex=False
        )
    ]

    if category != "All":
        visible = visible[visible["Category"] == category]

    
        st.html(
        '<div class="fw-transaction-table">'
        + visible.iloc[::-1].to_html(index=False, escape=True)
        + '</div>'
    )

    st.download_button(
        "Download expense report",
        df.to_csv(index=False),
        "FinWise_Expenses.csv",
        "text/csv"
    )

    if not visible.empty:
        selected = st.selectbox(
            "Expense to delete",
            list(visible.index),
            format_func=lambda i: str(df.loc[i, "Name"]) + f" — ₹{df.loc[i, 'Amount']:,.2f}"
        )

        if st.button("Delete selected expense"):
            s.expenses.pop(int(selected))
            if st.button("Delete selected expense"):
             s.expenses.pop(int(selected))
            save_data()
           
            st.rerun()
