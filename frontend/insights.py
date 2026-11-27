
import streamlit as st
import pandas as pd
from datetime import date


def show_insights():

    s = st.session_state

    s.setdefault("expenses", [])
    s.setdefault("monthly_budget", 5000.0)

    dark = s.get("dark_mode", False)

    ink = "#e1ebcd" if dark else "#171717"
    surface = "#242e28" if dark else "#fffdf8"
    green = "#344b36" if dark else "#e1ebcd"
    purple = "#41394e" if dark else "#e8e0f2"
    yellow = "#494535" if dark else "#f6ebcb"

    # PREMIUM INTERFACE

    st.html(f"""
<style>
.insight-hero {{
    background: linear-gradient(
        135deg, {green}, {purple}
    );
    padding: 35px;
    border-radius: 26px;
    color: {ink};
}}

.insight-heading {{
    font-size: clamp(30px, 4vw, 48px);
    font-weight: 800;
    letter-spacing: -2px;
}}

.insight-card {{
    background: {surface};
    padding: 24px;
    border-radius: 20px;
    color: {ink};
    margin-bottom: 15px;
}}

[data-testid="stMain"] label p,
[data-testid="stMain"] h2,
[data-testid="stMain"] h3 {{
    color: {ink} !important;
}}

[data-testid="stMain"] input {{
    color: {ink} !important;
    background: {surface} !important;
}}
</style>

<div class="insight-hero">
    <small style="letter-spacing:3px">
        ✦ FINWISE INTELLIGENCE
    </small>

    <div class="insight-heading">
        Your money.<br>
        A smarter perspective.
    </div>

    <p style="color:{ink}">
        Understand your financial habits.
        Make informed decisions.
    </p>
</div>
""")

    # READ EXPENSE DATA

    df = pd.DataFrame(
        s.expenses,
        columns=["Name", "Amount", "Category", "Date"]
    )

    today = date.today()

    dates = pd.to_datetime(df["Date"], errors="coerce")

    monthly = df[
        (dates.dt.month == today.month) &
        (dates.dt.year == today.year)
    ]

    total = float(monthly["Amount"].sum())
    budget = max(1.0, float(s.monthly_budget))
    remaining = budget - total
    percentage = total / budget * 100

    spending = monthly.groupby(
        "Category"
    )["Amount"].sum().sort_values(ascending=False)

    top_category = (
        spending.index[0]
        if not spending.empty
        else "No expenses"
    )

    top_amount = (
        float(spending.iloc[0])
        if not spending.empty
        else 0.0
    )

    # BUDGET STATUS

    if percentage >= 100:
        status = "Limit reached"

    elif percentage >= 80:
        status = "Near limit"

    else:
        status = "Within budget"

    # SUMMARY CARDS

    st.write("")

    cards = [
        ("Budget Status", status, green),
        ("Monthly Spending", f"₹{total:,.0f}", yellow),
        ("Top Category", top_category, purple)
    ]

    for col, item in zip(st.columns(3), cards):

        label, value, color = item

        col.html(f"""
<div style="background:{color};
color:{ink};padding:22px;border-radius:22px">

<small>{label}</small>

<div style="font-size:25px;font-weight:800">
{value}
</div>

</div>
""")

    st.divider()

    # SMART RECOMMENDATIONS

    st.subheader("✦ Smart Recommendations")

    if monthly.empty:

        st.info("Add expenses to unlock financial insights.")

    else:

        share = top_amount / total * 100 if total else 0

        st.html(f"""
<div class="insight-card">
    <b>◎ Spending Pattern</b>
    <p>{top_category} accounts for
    {share:.1f}% of your monthly spending.</p>
</div>
""")

        st.html(f"""
<div class="insight-card">
    <b>◎ Budget Monitoring</b>
    <p>You have used {percentage:.1f}%
    of your monthly budget.</p>
</div>
""")

        if remaining > 0:

            st.html(f"""
<div class="insight-card">
    <b>◎ Budget Planning</b>
    <p>You have ₹{remaining:,.2f} remaining.
    Consider your upcoming expenses before
    allocating money to savings.</p>
</div>
""")

        elif remaining < 0:

            st.warning(
                f"You are ₹{-remaining:,.2f} over budget."
            )

    st.divider()

    # SMART ASSISTANT

    st.subheader("🤖 FinWise Assistant")

    def generate_answer(question):

        q = question.lower()

        if "category" in q or "most" in q:

            if spending.empty:
                return "You haven't recorded expenses this month."

            return (
                f"Your highest spending category is "
                f"{top_category}, with ₹{top_amount:,.2f} spent."
            )

        elif "budget" in q or "remaining" in q:

            return (
                f"Your monthly budget is ₹{budget:,.2f}. "
                f"Your remaining budget is ₹{remaining:,.2f}."
            )

        elif "save" in q or "saving" in q:

            if remaining <= 0:
                return "Review your budget and upcoming expenses first."

            return (
                f"You have ₹{remaining:,.2f} remaining "
                "in your budget. Consider essential expenses "
                "before deciding how much to save."
            )

        elif "spend" in q or "expense" in q or "summary" in q:

            return (
                f"You have spent ₹{total:,.2f} "
                f"across {len(monthly)} transactions this month."
            )

        else:

            return (
                "I can currently answer questions about "
                "your expenses, budget, spending categories "
                "and savings planning."
            )

    st.html(f"""
<div class="insight-card">
    <b>✦ FinWise Intelligence</b>
    <p>Hello! Ask me about your recorded
    spending, budget or financial habits.</p>
</div>
""")

    st.caption("Suggested questions")

    
    
    
    st.html(f"""
<style>

/* Suggested question buttons */

[data-testid="stMain"] .stButton button {{
    background: {green} !important;
    color: {ink} !important;
    border: 1px solid #a8b99b !important;
    border-radius: 16px !important;
    min-height: 55px;
    text-align: left;
    justify-content: flex-start;
    padding: 15px 22px;
    transition: all 0.3s ease;
}}

[data-testid="stMain"] .stButton button p {{
    color: {ink} !important;
    font-size: 16px !important;
    font-weight: 600 !important;
}}

[data-testid="stMain"] .stButton button:hover {{
    background: {purple} !important;
    transform: translateX(5px);
    box-shadow: 0 5px 20px #91b47530;
}}

/* Question input visibility */

[data-testid="stMain"] input::placeholder {{
    color: {ink} !important;
    opacity: 0.65;
}}

</style>
""")


    questions = [
        "Where am I spending the most?",
        "How much budget do I have left?",
        "How can I plan my savings?",
        "Show my spending summary."
    ]

    for i, question in enumerate(questions):

        if st.button(
            question,
            key=f"insight_question_{i}",
            use_container_width=True
        ):

            s.insight_question = question

    with st.form("assistant_form", clear_on_submit=True):

        question = st.text_input(
            "Ask FinWise",
            placeholder="Ask about your finances..."
        )

        submitted = st.form_submit_button(
            "Ask Assistant ↗",
            use_container_width=True
        )

        if submitted and question.strip():

            s.insight_question = question.strip()

    if "insight_question" in s:

        with st.chat_message("user"):
            st.write(s.insight_question)

        with st.chat_message("assistant"):
            st.write(
                generate_answer(s.insight_question)
            )

    st.caption("FinWise uses rule-based financial insights.")
