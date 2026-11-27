import pandas as pd
from datetime import date
import streamlit as st


def show_dashboard():

    s = st.session_state

    s.setdefault("expenses", [])
    s.setdefault("monthly_budget", 5000.0)

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

    budget = float(s.monthly_budget)
    expenses = float(monthly["Amount"].sum())
    remaining = budget - expenses



    dashboard_html = """<style>

/* MAIN BACKGROUND */

.stApp {
    background: #faf4ee;
    color: #3d4738;
}

.block-container {
    padding-top: 2rem;
    max-width: 1450px;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background: #faf5ef;
    border-right: 1px solid #ece6dc;
}

[data-testid="stSidebar"] label {
    color: #3d4738;
}

/* LOGO */

.fw-brand {
    font-size: 32px;
    font-weight: 900;
    letter-spacing: -2px;
    margin-bottom: 22px;
    color: #3d4738;
}

.fw-brand span {
    background: #72a95a;
    color: white;
    border-radius: 8px;
    padding: 0 6px;
    margin-left: 4px;
}

/* HERO SECTION */

.fw-hero {
    position: relative;
    min-height: 350px;
    padding: 40px;
    border-radius: 28px;
    overflow: hidden;
    background: linear-gradient(
        135deg,
        #f6ebcb,
        #e3ebce,
        #e8e0f2
    );
    display: flex;
    align-items: center;
    margin-bottom: 16px;
}

.fw-hero-text {
    position: relative;
    z-index: 2;
    width: 60%;
}

.fw-eyebrow {
    font-size: 13px;
    letter-spacing: 5px;
    color: #525b49;
    margin-bottom: 20px;
}

.fw-heading {
    font-size: clamp(36px, 5vw, 68px);
    line-height: 1.08;
    font-weight: 900;
    letter-spacing: -3px;
    color: #3d4738;
}

.fw-description {
    font-size: 18px;
    color: #59634e;
    margin-top: 18px;
    margin-bottom: 25px;
}

/* EXPLORE BUTTON */

.fw-explore {
    display: inline-block;
    text-decoration: none !important;
    background: #3d4738;
    color: white !important;
    border-radius: 50px;
    padding: 16px 30px;
    font-size: 16px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.fw-explore:hover {
    background: #667b55;
    transform: translateY(-4px);
    box-shadow: 0 12px 25px #3d473830;
}

/* MONEY ILLUSTRATION */

.fw-art {
    position: absolute;
    right: 2%;
    top: 50%;
    width: 38%;
    height: 300px;
    transform: translateY(-50%);
}

.fw-glow {
    position: absolute;
    inset: 0;
    border-radius: 50%;
    background: #ffffff30;
}

.fw-orbit {
    position: absolute;
    width: 96%;
    height: 70%;
    top: 15%;
    border: 3px solid #ffffffcc;
    border-radius: 50%;
    transform: rotate(-40deg);
}

/* FLOATING BANK CARD */

.fw-bank-card {
    position: absolute;
    width: 68%;
    height: 48%;
    top: 26%;
    left: 15%;
    border: 2px solid white;
    border-radius: 24px;
    background: linear-gradient(
        135deg,
        #ffffffb0,
        #d1dcc8a0,
        #eae4f4
    );
    backdrop-filter: blur(15px);
    box-shadow: 8px 12px 0 #8a96833b,
                0 20px 35px #65765d22;
    animation: fwCardFloat 4s ease-in-out infinite;
}

.fw-chip {
    position: absolute;
    left: 20px;
    top: 20px;
    width: 43px;
    height: 30px;
    border-radius: 8px;
    background: linear-gradient(
        125deg, #ffffff, #becdc7, #ffffff
    );
}

.fw-card-brand {
    position: absolute;
    bottom: 20px;
    left: 20px;
    font-size: 25px;
    color: #3d4738;
    font-weight: 900;
}

/* FLOATING RUPEE COINS */

.fw-coin {
    position: absolute;
    z-index: 3;
    width: 76px;
    height: 76px;
    border-radius: 50%;
    background: linear-gradient(
        145deg, #ffffff, #c8d9d4
    );
    border: 5px solid #f8fff9;
    outline: 2px solid #a2bab2;
    box-shadow: 5px 8px 0 #8da9a0;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #52786d;
    font-size: 38px;
    font-weight: 800;
    animation: fwCoinFloat 3s ease-in-out infinite;
}

.fw-coin-one {
    top: 4%;
    right: 13%;
}

.fw-coin-two {
    bottom: 5%;
    left: 5%;
    width: 88px;
    height: 88px;
    animation-delay: 0.6s;
}

.fw-coin-three {
    bottom: 12%;
    right: 0;
    width: 60px;
    height: 60px;
    font-size: 29px;
    animation-delay: 1s;
}

/* FINANCIAL CARDS */

.fw-metrics {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 16px;
}

.fw-metric {
    padding: 22px;
    border-radius: 22px;
    border: 1px solid #ffffff80;
    transition: all 0.3s ease;
}

.fw-metric:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 30px #3d473815;
}

.fw-balance {
    background: #f6ebcb;
}

.fw-expenses {
    background: #e8e0f2;
}

.fw-savings {
    background: #e1ebcd;
}

.fw-metric-icon {
    font-size: 23px;
    margin-bottom: 8px;
}

.fw-metric-label {
    font-size: 15px;
    color: #5a6352;
}

.fw-amount {
    font-size: clamp(24px, 3vw, 34px);
    font-weight: 800;
    color: #3d4738;
    margin-top: 6px;
}

/* ANALYTICS SECTION */

.fw-analytics {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
}

.fw-chart {
    min-height: 330px;
    padding: 24px;
    border-radius: 25px;
    background: #fffdfb;
}

.fw-chart-title {
    font-size: 20px;
    font-weight: 800;
    color: #3d4738;
    margin-bottom: 25px;
}

/* DONUT CHART */

.fw-donut {
    position: relative;
    width: 235px;
    height: 235px;
    max-width: 100%;
    margin: 10px auto;
    border-radius: 50%;
    background: conic-gradient(
        #f4e7bf 0% 39%,
        #fffdfb 39% 40%,
        #dce8c5 40% 72%,
        #fffdfb 72% 74%,
        #e4d9f1 74% 98%,
        #fffdfb 98% 100%
    );
    display: flex;
    justify-content: center;
    align-items: center;
    animation: fwChartEnter 1s ease-out both;
}

.fw-donut-center {
    background: #fffdfb;
    width: 68%;
    height: 68%;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
}

.fw-donut-amount {
    font-size: 32px;
    font-weight: 900;
    color: #3d4738;
}

.fw-donut-label {
    font-size: 14px;
    color: #65705c;
}

/* FINANCIAL GROWTH CHART */

.fw-growth {
    background: #f6ebcb;
}

.fw-bars {
    height: 235px;
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 8px;
}

.fw-bar {
    flex: 1;
    border-radius: 30px;
    background: linear-gradient(
        #92977a, #757e61
    );
    height: var(--height);
    transform-origin: bottom;
    animation: fwBarGrow 1.3s ease-out both;
}

.fw-light-bar {
    background: #fffdf5;
}

.fw-months {
    display: flex;
    justify-content: space-between;
    margin-top: 15px;
    color: #6a725f;
    font-size: 12px;
}

/* FOOTER */

.fw-footer {
    text-align: center;
    color: #858c79;
    font-size: 12px;
    letter-spacing: 2px;
    margin-top: 30px;
}

/* ANIMATIONS */

@keyframes fwCardFloat {
    0%, 100% {
        transform: rotate(-20deg) translateY(0);
    }
    50% {
        transform: rotate(-16deg) translateY(-12px);
    }
}

@keyframes fwCoinFloat {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-12px);
    }
}

@keyframes fwBarGrow {
    from {
        transform: scaleY(0);
    }
    to {
        transform: scaleY(1);
    }
}

@keyframes fwChartEnter {
    from {
        opacity: 0;
        transform: scale(0.7);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

/* MOBILE RESPONSIVE DESIGN */

@media (max-width: 850px) {
    .fw-hero {
        display: block;
        padding: 26px;
    }

    .fw-hero-text {
        width: 100%;
    }

    .fw-art {
        position: relative;
        right: auto;
        top: auto;
        width: 90%;
        margin: 25px auto 0;
        transform: none;
    }

    .fw-analytics {
        grid-template-columns: 1fr;
    }

    .fw-metrics {
        grid-template-columns: 1fr;
    }
}

@media (prefers-reduced-motion: reduce) {
    .fw-bank-card,
    .fw-coin,
    .fw-bar,
    .fw-donut {
        animation: none;
    }
}

</style>



<div class="fw-hero">
    <div class="fw-hero-text">
        <div class="fw-eyebrow">YOUR MONEY. YOUR FUTURE.</div>
        <div class="fw-heading">Money moves.<br>Made smarter.</div>
        <div class="fw-description">The next generation of personal finance.</div>
        <a class="fw-explore" href="#fw-analytics" target="_self">Explore FinWise ↗</a>
    </div>
    <div class="fw-art">
        <div class="fw-glow"></div>
        <div class="fw-orbit"></div>
        <div class="fw-bank-card">
            <div class="fw-chip"></div>
            <div class="fw-card-brand">finwise.</div>
        </div>
        <div class="fw-coin fw-coin-one">₹</div>
        <div class="fw-coin fw-coin-two">₹</div>
        <div class="fw-coin fw-coin-three">₹</div>
    </div>
</div>

<div class="fw-metrics">
    <div class="fw-metric fw-balance">
        <div class="fw-metric-icon">▣</div>
        <div class="fw-metric-label">Balance</div>
        <div class="fw-amount">₹24,850</div>
    </div>
    <div class="fw-metric fw-expenses">
        <div class="fw-metric-icon">↗</div>
        <div class="fw-metric-label">Expenses</div>
        <div class="fw-amount">₹8,420</div>
    </div>
    <div class="fw-metric fw-savings">
        <div class="fw-metric-icon">◎</div>
        <div class="fw-metric-label">Savings</div>
        <div class="fw-amount">₹6,580</div>
    </div>
</div>

<div class="fw-analytics" id="fw-analytics">
    <div class="fw-chart">
        <div class="fw-chart-title">Spending analytics</div>
        <div class="fw-donut">
            <div class="fw-donut-center">
                <div class="fw-donut-amount">₹8,420</div>
                <div class="fw-donut-label">Total expenses</div>
            </div>
        </div>
    </div>
    <div class="fw-chart fw-growth">
        <div class="fw-chart-title">Financial growth</div>
        <div class="fw-bars">
            <div class="fw-bar" style="--height:25%"></div>
            <div class="fw-bar fw-light-bar" style="--height:12%"></div>
            <div class="fw-bar" style="--height:50%"></div>
            <div class="fw-bar fw-light-bar" style="--height:30%"></div>
            <div class="fw-bar" style="--height:38%"></div>
            <div class="fw-bar fw-light-bar" style="--height:22%"></div>
            <div class="fw-bar" style="--height:72%"></div>
            <div class="fw-bar fw-light-bar" style="--height:45%"></div>
            <div class="fw-bar" style="--height:60%"></div>
            <div class="fw-bar fw-light-bar" style="--height:36%"></div>
            <div class="fw-bar" style="--height:100%"></div>
            <div class="fw-bar fw-light-bar" style="--height:58%"></div>
        </div>
        <div class="fw-months">
            <span>Jan</span>
            <span>Feb</span>
            <span>Mar</span>
            <span>Apr</span>
            <span>May</span>
            <span>Jun</span>
        </div>
    </div>
</div>

<div class="fw-footer">
    FINWISE — MAKE EVERY RUPEE COUNT.
</div>


"""

    dashboard_html = dashboard_html.replace(
        "₹24,850", f"₹{budget:,.0f}"
    ).replace(
        "₹8,420", f"₹{expenses:,.0f}"
    ).replace(
        "₹6,580", f"₹{remaining:,.0f}"
    ).replace(
        ">Balance<", ">Monthly Budget<"
    ).replace(
        ">Savings<", ">Budget Remaining<"
    ).replace(
        "Financial growth", "Financial growth (Demo)"
    ).replace(
        "Spending analytics", "Spending analytics (Demo)"
    )


    # LIVE DASHBOARD CHARTS

    from html import escape

    dark = s.get("dark_mode", False)

    ink = "#e1ebcd" if dark else "#171717"

    palette = [
        "#eeddb1",
        "#bed2a4",
        "#d8c9e9",
        "#a8cbc3",
        "#dfbfc5",
        "#b8bca0",
        "#a8a4bc"
    ]

    # SPENDING DONUT CHART

    spending = monthly.groupby(
        "Category"
    )["Amount"].sum().sort_values(ascending=False)

    stops = []
    legend = ""
    start = 0.0

    if expenses > 0:

        for i, (category, amount) in enumerate(spending.items()):

            color = palette[i % len(palette)]

            end = start + float(amount) / expenses * 100

            stops.append(
                f"{color} {start}% {end}%"
            )

            start = end

            legend += f"""
<div style="display:flex;align-items:center;
gap:10px;margin:12px 0;color:{ink}">
<span style="background:{color};width:12px;
height:12px;border-radius:50%"></span>
<span>{escape(str(category))}</span>
<b style="margin-left:auto">₹{amount:,.2f}</b>
</div>
"""

    ring = ",".join(stops) if stops else "#aab5a344"

    if not legend:
        legend = "<p>No expenses recorded this month.</p>"

    # SIX-MONTH SPENDING HISTORY

    months = pd.period_range(
        end=pd.Period(today, freq="M"),
        periods=6,
        freq="M"
    )

    history = []

    for month in months:

        month_total = df.loc[
            dates.dt.to_period("M") == month,
            "Amount"
        ].sum()

        history.append(float(month_total))

    maximum = max(history + [1.0])

    bars = ""

    for month, amount in zip(months, history):

        height = amount / maximum * 100

        bars += f"""
<div style="flex:1;min-width:0;text-align:center;
color:{ink}">

<div style="height:220px;display:flex;
flex-direction:column;justify-content:flex-end">

<div style="font-size:11px;margin-bottom:7px">
₹{amount:,.0f}
</div>

<div class="fw-bar" style="--height:{height}%;
flex:none;width:80%;margin:0 auto;
height:{height}%;min-height:0">
</div>

</div>

<div style="font-size:12px;margin-top:12px">
{month.strftime('%b')}
</div>

</div>
"""

    # NEW ANALYTICS INTERFACE

    analytics_html = f"""
<div class="fw-analytics" id="fw-analytics">

<div class="fw-chart">

<div class="fw-chart-title">
Spending analytics
</div>

<div class="fw-donut"
style="background:conic-gradient({ring}) !important">

<div class="fw-donut-center">

<div class="fw-donut-amount">
₹{expenses:,.0f}
</div>

<div class="fw-donut-label">
Total expenses
</div>

</div>
</div>

{legend}

</div>

<div class="fw-chart fw-growth">

<div class="fw-chart-title">
Monthly spending trends
</div>

<div style="display:flex;gap:10px;
align-items:flex-end;margin-top:25px">

{bars}

</div>

<div style="margin-top:25px;color:{ink}">
Last six months of recorded expenses
</div>

</div>

</div>
"""

    # REPLACE THE OLD DEMO GRAPHS

    start_index = dashboard_html.find(
        '<div class="fw-analytics"'
    )

    end_index = dashboard_html.find(
        '<div class="fw-footer"'
    )

    if start_index >= 0 and end_index > start_index:

        dashboard_html = (
            dashboard_html[:start_index]
            + analytics_html
            + dashboard_html[end_index:]
        )

    else:

        st.warning("Could not locate the old analytics section.")

    st.html(dashboard_html)
