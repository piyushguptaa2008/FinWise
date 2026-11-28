
import streamlit as st
import sqlite3
import json
import hashlib
from pathlib import Path

def get_db_path():
    if "_profile_db" not in st.session_state:
        st.title("FinWise — Your Personal Profile")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Open Profile"):
            if username.strip() and len(password) >= 8:
                key = hashlib.sha256(
                    (username.strip() + ":" + password).encode()
                ).hexdigest()

                folder = Path.home() / ".finwise_profiles"
                folder.mkdir(mode=0o700, exist_ok=True)

                st.session_state["_profile_db"] = str(
                    folder / (key + ".db")
                )
                st.rerun()
            else:
                st.error("Enter a username and at least 8 password characters.")

        st.stop()

    return st.session_state["_profile_db"]


def initialize_database():
    with sqlite3.connect(get_db_path()) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS finance_data (
                id INTEGER PRIMARY KEY,
                expenses TEXT,
                budget REAL
            )
        """)

    st.session_state.setdefault("expenses", [])
    st.session_state.setdefault("monthly_budget", 5000.0)


def load_data():
    initialize_database()

    if st.session_state.get("_data_loaded"):
        return

    with sqlite3.connect(get_db_path()) as conn:
        row = conn.execute(
            "SELECT expenses, budget FROM finance_data WHERE id=1"
        ).fetchone()

    if row:
        st.session_state.expenses = json.loads(row[0])
        st.session_state.monthly_budget = row[1]

    st.session_state["_data_loaded"] = True


def save_data():
    initialize_database()

    with sqlite3.connect(get_db_path()) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO finance_data VALUES (1, ?, ?)",
            (
                json.dumps(st.session_state.expenses, default=str),
                float(st.session_state.monthly_budget)
            )
        )
