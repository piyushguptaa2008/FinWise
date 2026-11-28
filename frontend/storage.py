import streamlit as st


def initialize_database():

    st.session_state.setdefault("expenses", [])
    st.session_state.setdefault("monthly_budget", 5000.0)


def load_data():

    initialize_database()


def save_data():

    initialize_database()