import streamlit as st
from pathlib import Path
from splash import show_splash
from dashboard import show_dashboard
from expenses import show_expenses
from budget import show_budget
from insights import show_insights
from savings import show_savings
from storage import load_data

st.set_page_config(
    page_title="FinWise",
    page_icon="💰",
    layout="wide"
)

show_splash()
load_data()



css_file = Path(__file__).parent / "style.css"

st.markdown(
    f"<style>{css_file.read_text()}</style>",
    unsafe_allow_html=True
)

st.markdown("""
<div class="top-brand-wrap">
    <div class="top-brand">💰 FinWise</div>
    <div class="top-brand-sub">
        Your Personal Finance Assistant
    </div>
    <div class="top-brand-text">
        Understand. Plan. Spend smarter.
    </div>
</div>
""", unsafe_allow_html=True)








  
if "nav_page" not in st.session_state:
    st.session_state.nav_page = "Dashboard"


def change_page(name):
    st.session_state.nav_page = name


with st.sidebar:

    st.markdown("""
    <div class="nav-brand">💰 FinWise</div>
    <div class="nav-tagline">PERSONAL FINANCE</div>
    <div class="nav-section">WORKSPACE</div>
    """, unsafe_allow_html=True)

    menu = {
        "Dashboard": "⌂",
        "Expenses": "₹",
        "Budget": "◉",
        "Savings Goals": "◎",
        "AI Insights": "✦"
    }       

    for name, icon in menu.items():

        st.button(
            f"{icon}    {name}",
            key="nav_" + name,
            use_container_width=True,
            type="primary" if st.session_state.nav_page == name else "secondary",
            on_click=change_page,
            args=(name,)
        )
    st.divider()

    dark_mode = st.toggle(
        "🌙 Dark Mode",
        value=False,
        key="dark_mode"
    )
    st.markdown("""
    <div class="nav-premium">
        <div class="nav-star">✦</div>
        <h3>Money, but smarter.</h3>
        <p>Small habits.<br>Big possibilities.</p>
    </div>

    <div class="nav-account">
        <div class="nav-avatar">♙</div>
        <div>
            <b>Your Account</b><br>
            <small>Personal workspace</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

page = st.session_state.nav_page


if page == "Dashboard":
    show_dashboard()

elif page == "Expenses":
    show_expenses()

elif page == "Budget":
    show_budget()
elif page == "AI Insights":
    show_insights()
elif page == "Savings Goals":
    show_savings()



if dark_mode:
    st.markdown("""
<style>

:root {
    --fw-bg: #171e1b;
    --fw-surface: #242e28;
    --fw-text: #e1ebcd;
    --fw-input: #303e32;
    --fw-border: #435541;
}
/* Main background */

.stApp {
    background: #171e1b !important;
    color: #e1ebcd !important;
}

[data-testid="stHeader"] {
    background: #171e1b !important;
}

/* Sidebar */

[data-testid="stSidebar"] {
    background: #222b25 !important;
    border-right: 1px solid #354438 !important;
}

.nav-brand,
.top-brand,
.top-brand-sub {
    color: #e1ebcd !important;
}

.nav-tagline,
.nav-section,
.top-brand-text {
    color: #a7b6a2 !important;
}

/* Navigation buttons */

[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    color: #e1ebcd !important;
    border-color: transparent !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: #354438 !important;
}

[data-testid="stSidebar"] .stButton > button[kind="primary"],
[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"] {
    background: #40563b !important;
    color: #e1ebcd !important;
}

/* Sidebar cards */

.nav-premium {
    background: linear-gradient(
        135deg, #41394e, #303e32
    ) !important;
}

.nav-premium h3,
.nav-premium p {
    color: #e2d9ec !important;
}

.nav-account {
    background: #303b32 !important;
    color: #e1ebcd !important;
}

.nav-account small {
    color: #a7b6a2 !important;
}

.nav-avatar {
    background: #496044 !important;
}

/* Hero section */

.fw-hero {
    background: linear-gradient(
        135deg,
        #3e4532,
        #293c31,
        #393344
    ) !important;
}

.fw-heading {
    color: #e5eedb !important;
}

.fw-eyebrow,
.fw-description {
    color: #b9c9b1 !important;
}

.fw-explore {
    background: #c5d9b2 !important;
    color: #263321 !important;
}

/* Floating bank card */

.fw-bank-card {
    background: linear-gradient(
        135deg, #899f80, #536c53, #6e687d
    ) !important;

    border-color: #b7cbb0 !important;
}

.fw-card-brand {
    color: #edf3e6 !important;
}

.fw-orbit {
    border-color: #b5c9ae80 !important;
}

/* Financial cards */

.fw-balance {
    background: #494535 !important;
}

.fw-expenses {
    background: #41394e !important;
}

.fw-savings {
    background: #344b36 !important;
}

.fw-metric {
    border-color: #ffffff15 !important;
}

.fw-amount,
.fw-metric-icon,
.fw-metric-label {
    color: #e1ebcd !important;
}

/* Analytics cards */

.fw-chart {
    background: #242e28 !important;
}

.fw-growth {
    background: #353b2d !important;
}

.fw-chart-title,
.fw-donut-amount {
    color: #e1ebcd !important;
}

/* Donut chart */

.fw-donut {
    background: conic-gradient(
        #b7aa79 0% 39%,
        #242e28 39% 40%,
        #8faa78 40% 72%,
        #242e28 72% 74%,
        #a795bb 74% 98%,
        #242e28 98% 100%
    ) !important;
}

.fw-donut-center {
    background: #242e28 !important;
}

.fw-donut-label,
.fw-months,
.fw-footer {
    color: #aabca3 !important;
}

/* Growth chart */

.fw-bar {
    background: linear-gradient(
        #b8cea0, #819b70
    ) !important;
}

.fw-light-bar {
    background: #606b53 !important;
}

/* Text visibility */

h1, h2, h3, h4 {
    color: #e1ebcd !important;
}

[data-testid="stSidebar"] label p {
    color: #e1ebcd !important;
}

</style>
""", unsafe_allow_html=True)

