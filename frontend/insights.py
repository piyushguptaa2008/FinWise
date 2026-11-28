import streamlit as st
import pandas as pd
from datetime import date
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from frontend.ai_adapter import get_ai_answer
from approval import ApprovalManager


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

    st.html(f"""
    <div class="insight-card">
        <b>✦ FinWise Intelligence</b>
        <p>Ask me about spending, subscriptions,
        budgeting and financial knowledge.</p>
    </div>

    <style>
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

    [data-testid="stMain"] input::placeholder {{
        color: {ink} !important;
        opacity: 0.65;
    }}
    </style>
    """)

    st.info(
    "AI analyses your recorded expenses "
    "to provide personalised financial insights."
)

    s.setdefault("insight_result", None)
    s.setdefault("insight_question", "")

    new_question = None

    st.caption("Suggested questions")

    questions = [
        "What is my November spending?",
        "Show my subscriptions.",
        "Calculate my remaining balance.",
        "Explain the 50/30/20 budgeting rule.",
        "Create a monthly budget plan with income 15000."
    ]

    for i, question in enumerate(questions):

        if st.button(
            question,
            key=f"insight_question_{i}",
            use_container_width=True
        ):
            new_question = question

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
            new_question = question.strip()

    # RUN AI ONLY ON SUBMISSION

    if new_question:

        s.insight_question = new_question
        s.insight_result = None

        with st.spinner("FinWise AI is analysing your request..."):

            try:
                s.insight_result = get_ai_answer(
    new_question,
    s.expenses
)
            except Exception as error:
                st.error(
                    f"AI request failed: {type(error).__name__}"
                )

    # DISPLAY AI RESPONSE

    if s.insight_result is not None:

        result = s.insight_result

        with st.chat_message("user"):
            st.write(s.insight_question)

        with st.chat_message("assistant"):
            st.markdown(result.get("answer", ""))

        # VALIDATION STATUS

        if result.get("validated", False):
            st.success("Validation Passed")

        else:
            st.warning("Validation Incomplete")

        # AI EXECUTION TRACE

        with st.expander("View AI Execution Trace"):

            st.write("Executed Tools:")
            st.write(result.get("executed_tools", []))

            st.write("Recovered Tools:")
            st.write(result.get("recovered_tools", []))

            st.write("Rejected Tools:")
            st.write(result.get("rejected_tools", []))

            st.write("Missing Tools:")
            st.write(result.get("missing_tools", []))

            st.write("Knowledge Sources:")
            st.write(result.get("knowledge_sources", []))


    # HUMAN APPROVAL SYSTEM

    if "approval_manager" not in s:
        s.approval_manager = ApprovalManager()

    manager = s.approval_manager

    result = s.insight_result or {}

    can_approve = (
        result.get("validated", False)
        and "create_budget_plan" in
        result.get("tools_used", [])
    )

    # CREATE PROPOSAL ONLY ON SUBMISSION

    if new_question:
        s.insight_proposal_id = None

        if can_approve:

            proposal = manager.create_proposal(
                action="create_budget_plan",
                details={
                    "question": s.insight_question,
                    "answer": result["answer"],
                    "dataset": "User Recorded Expenses"
                }
            )

            s.insight_proposal_id = proposal["id"]

    # APPROVAL AND REJECTION BUTTONS

    if can_approve and s.get("insight_proposal_id"):

        proposal = manager.get_proposal(
            s.insight_proposal_id
        )

        if proposal:

            st.subheader("🛡️ Human Approval")

            if proposal["status"] == "pending":

                st.info(
                    "Review this budget proposal "
                    "before approving it."
                )

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "✓ Approve",
                        key="approve_budget",
                        use_container_width=True
                    ):
                        manager.approve(proposal["id"])
                        st.rerun()

                with col2:

                    if st.button(
                        "✕ Reject",
                        key="reject_budget",
                        use_container_width=True
                    ):
                        manager.reject(proposal["id"])
                        st.rerun()

            elif proposal["status"] == "approved":

                st.success("Budget proposal approved!")

            elif proposal["status"] == "rejected":

                st.warning("Budget proposal rejected.")

    # REVIEWED PROPOSAL HISTORY

    st.divider()

    with st.expander("📜 Reviewed Proposal History"):

        history = manager.get_history()

        if not history:

            st.info("No reviewed proposals yet.")

        else:

            for proposal in history:

                st.write(
                    proposal["details"]["question"]
                )

                st.write(
                    "Status:",
                    proposal["status"].upper()
                )

                st.caption(
                    proposal.get("reviewed_at", "")
                )

                st.write(proposal["details"]["answer"])

                st.divider()
    st.caption(
        "Powered by FinWise Agentic AI"
    )