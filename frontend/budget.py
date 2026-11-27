from storage import save_data
import streamlit as st
import pandas as pd
from datetime import date


def show_budget():

    s = st.session_state

    s.setdefault("expenses", [])
    s.setdefault("monthly_budget", 5000.0)

    dark = s.get("dark_mode", False)

    ink = "#e1ebcd" if dark else "#171717"
    surface = "#242e28" if dark else "#fffdf8"

    gradient = (
        "#344438, #41394e" if dark
        else "#e3ebce, #e8e0f2"
    )

    colors = (
        ["#494535", "#41394e", "#344b36"] if dark
        else ["#f6ebcb", "#e8e0f2", "#e1ebcd"]
    )

    # PREMIUM HEADER

    st.markdown(f"""
<div style="background:linear-gradient(135deg,{gradient});
padding:35px;border-radius:25px;color:{ink}">

<div style="font-size:12px;letter-spacing:3px">
FINANCIAL PLANNING
</div>

<div style="font-size:clamp(30px,4vw,50px);
font-weight:800;letter-spacing:-2px">
Plan smarter. Spend wiser.
</div>

<div style="font-size:16px">
Give every rupee a purpose.
</div>

</div>
""", unsafe_allow_html=True)

    # CALCULATE MONTHLY EXPENSES

    df = pd.DataFrame(
        s.expenses,
        columns=["Name", "Amount", "Category", "Date"]
    )

    today = date.today()

    dates = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    monthly = df[
        (dates.dt.month == today.month) &
        (dates.dt.year == today.year)
    ]

    spent = float(monthly["Amount"].sum())

    summary = st.container()

    left, right = st.columns(2)

    # SET MONTHLY BUDGET

    with left:

        st.subheader("🎯 Budget Control")

        with st.form("budget_planner_form"):

            new_budget = st.number_input(
                "Monthly Budget (₹)",
                min_value=1.0,
                value=max(1.0, float(s.monthly_budget)),
                step=500.0
            )

            save = st.form_submit_button(
                "Update Budget",
                use_container_width=True
            )

            if save:

                s.monthly_budget = new_budget
            save_data()

        st.success("Budget updated successfully!")

    budget = float(s.monthly_budget)
    remaining = budget - spent
    percentage = (spent / budget) * 100

    # FINANCIAL SUMMARY CARDS

    with summary:

        st.write("")

        labels = [
            "Monthly Budget",
            "Total Spent",
            "Budget Remaining"
        ]

        values = [budget, spent, remaining]

        for col, label, value, color in zip(
            st.columns(3), labels, values, colors
        ):

            col.markdown(f"""
<div style="background:{color};color:{ink};
padding:25px;border-radius:22px">

<div style="font-size:14px">
{label}
</div>

<div style="font-size:30px;font-weight:800">
₹{value:,.2f}
</div>

</div>
""", unsafe_allow_html=True)

    # CIRCULAR BUDGET INDICATOR

    with right:

        st.subheader("Budget Overview")

        ring_color = (
            "#c77d70" if spent > budget
            else "#91b475"
        )

        used = min(percentage, 100)

        st.markdown(f"""
<div style="background:conic-gradient(
{ring_color} 0% {used}%,
#aab5a333 {used}% 100%);
width:230px;max-width:100%;aspect-ratio:1;
border-radius:50%;display:grid;
place-items:center;margin:25px auto">

<div style="background:{surface};
width:78%;height:78%;border-radius:50%;
display:grid;place-content:center;
text-align:center;color:{ink}">

<div style="font-size:40px;font-weight:800">
{percentage:.0f}%
</div>

<div>Budget Used</div>

</div>
</div>
""", unsafe_allow_html=True)

        if percentage >= 100:

            st.warning("You have reached your budget limit.")

        elif percentage >= 80:

            st.warning("You are approaching your budget limit.")

        else:

            st.success(
                f"₹{remaining:,.2f} available in your budget."
            )

    st.divider()

    # CATEGORY-WISE SPENDING

    st.subheader("Category Spending Analysis")

    if not monthly.empty:

        spending = monthly.groupby(
            "Category"
        )["Amount"].sum().sort_values(ascending=False)

        for category, amount in spending.items():

            st.write(f"**{category}** — ₹{amount:,.2f}")

            st.progress(min(float(amount / budget), 1.0))

        highest = spending.idxmax()

        st.info(
            f"✦ Smart Insight: {highest} is your "
            "highest spending category this month."
        )

    else:

        st.info("Add expenses to unlock spending analytics.")

    st.divider()

    # SMART FINANCIAL INSIGHTS

    st.subheader("✦ FinWise Insights")

    if remaining > 0:

        st.write(
            f"You have ₹{remaining:,.2f} remaining "
            "in your monthly budget."
        )

    elif remaining < 0:

        st.write(
            f"You have exceeded your budget by "
            f"₹{abs(remaining):,.2f}."
        )

    else:

        st.write("Your monthly budget is fully used.")
