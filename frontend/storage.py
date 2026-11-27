
import sqlite3
import json
import streamlit as st
from pathlib import Path

DB_PATH = Path.home() / ".finwise" / "finwise.db"


def initialize_database():

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS finance_data (
                id INTEGER PRIMARY KEY,
                expenses TEXT NOT NULL,
                budget REAL NOT NULL
            )
        """)


def load_data():

    if st.session_state.get("database_loaded", False):
        return

    initialize_database()

    with sqlite3.connect(DB_PATH) as conn:

        row = conn.execute("""
            SELECT expenses, budget
            FROM finance_data
            WHERE id = 1
        """).fetchone()

    if row:

        st.session_state.expenses = json.loads(row[0])
        st.session_state.monthly_budget = row[1]

    else:

        st.session_state.setdefault("expenses", [])
        st.session_state.setdefault("monthly_budget", 5000.0)

    st.session_state.database_loaded = True


def save_data():

    initialize_database()

    expenses = json.dumps(
        st.session_state.expenses,
        default=str
    )

    budget = st.session_state.monthly_budget

    with sqlite3.connect(DB_PATH) as conn:

        conn.execute("""
            INSERT OR REPLACE INTO finance_data
            (id, expenses, budget)
            VALUES (1, ?, ?)
        """, (expenses, budget))
