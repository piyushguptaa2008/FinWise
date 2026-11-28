
import streamlit as st
import pandas as pd
from datetime import date
from agent_bridge import ask_finwise
from approval import ApprovalManager


def show_insights():

    s = st.session_state

    if "approval_manager" not in s:
        s.approval_manager = ApprovalManager()

    manager = s.approval_manager

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

[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] * {{
    color: {ink} !important;
}}

[data-testid="stChatMessage"] {{
    background: {surface} !important;
    border-radius: 18px !important;
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

    # AI-POWERED SMART ASSISTANT

    st.subheader("🤖 FinWise Assistant")

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

    pending_question = None

    # SUGGESTED QUESTION BUTTONS

    for i, question in enumerate(questions):

        if st.button(
            question,
            key=f"insight_question_{i}",
            use_container_width=True
        ):

            pending_question = question

    # CUSTOM QUESTION INPUT

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

            pending_question = question.strip()

    # CONNECT TO ACTUAL AI AGENT

    if pending_question:

        s.insight_question = pending_question

        s.pop("insight_result", None)
        s.pop("insight_error", None)

        with st.spinner("FinWise is thinking..."):

            try:

                s.insight_result = ask_finwise(
                    s.insight_question
                )

                result = s.insight_result

                if (
                    result.get("validated") is True
                    and "create_budget_plan"
                    in result.get("tools_used", [])
                ):

                    manager.create_proposal(
                        "Save budget plan",
                        {
                            "request": s.insight_question,
                            "recommendation": result["answer"]
                        }
                    )

            except Exception as e:

                s.insight_error = str(e)

                print("FinWise Agent Error:", str(e))

    # DISPLAY AI RESPONSE

    if "insight_question" in s:

        with st.chat_message("user"):

            st.write(s.insight_question)

        with st.chat_message("assistant"):

            if "insight_result" in s:

                result = s.insight_result

                st.markdown(result["answer"])

                tools_used = result.get("tools_used", [])

                if tools_used:

                    with st.expander("Agent Activity"):

                        for tool_name in tools_used:

                            st.write(
                                "✓ " + tool_name.replace("_", " ").title()
                            )

                if result.get("validated") is False:

                    st.warning(
                        "Some required agent checks could not be completed."
                    )

            elif "insight_error" in s:

                st.error(
                    "Unable to generate a response. Please try again."
                )

    # HUMAN APPROVAL

    pending = manager.get_pending()

    if pending:

        st.divider()
        st.subheader("Human Approval Required")

        st.info(
            "Review the proposed budget before saving it."
        )

        for proposal in pending:

            proposal_id = proposal["id"]

            with st.container(border=True):

                st.markdown(
                    "**Status: Pending approval**"
                )

                st.markdown(
                    proposal["details"]["recommendation"]
                )

                approve_col, reject_col = st.columns(2)

                if approve_col.button(
                    "Approve Plan",
                    key=f"approve_{proposal_id}",
                    use_container_width=True
                ):

                    try:

                        response = manager.approve(proposal_id)

                        if "error" in response:
                            st.error(response["error"])

                        else:
                            s.approval_notice = "Budget plan approved and saved."
                            st.rerun()

                    except Exception as e:
                        st.error(f"Approval failed: {e}")

                if reject_col.button(
                    "Reject Plan",
                    key=f"reject_{proposal_id}",
                    use_container_width=True
                ):

                    response = manager.reject(proposal_id)

                    if "error" in response:
                        st.error(response["error"])

                    else:
                        s.approval_notice = "Budget proposal rejected."
                        st.rerun()

    if "approval_notice" in s:
        st.info(s.pop("approval_notice"))

    # APPROVAL HISTORY

    history = manager.get_history()

    if history:

        with st.expander("Approval History"):

            for item in reversed(history):

                status = item["status"].title()

                if item["status"] == "approved":
                    st.success(f"Approved: {item['action']}")

                else:
                    st.warning(f"{status}: {item['action']}")

                st.caption(item.get("reviewed_at", ""))

    st.caption(
        "FinWise uses AI-powered financial insights and RAG."
    )
