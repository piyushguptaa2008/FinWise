import json
import streamlit as st
from streamlit_local_storage import LocalStorage


STORAGE_KEY = "finwise_user_data_v2"


def initialize_database():

    st.session_state.setdefault("expenses", [])
    st.session_state.setdefault("monthly_budget", 5000.0)
    st.session_state.setdefault("storage_loaded", False)
    st.session_state.setdefault("storage_dirty", False)


def load_data():

    initialize_database()

    storage = LocalStorage(key="finwise_storage_init")

    if not st.session_state.storage_loaded:

        saved = storage.getItem(STORAGE_KEY)

        if saved and not st.session_state.storage_dirty:

            try:
                data = json.loads(saved)

                st.session_state.expenses = data.get(
                    "expenses", []
                )

                st.session_state.monthly_budget = float(
                    data.get("monthly_budget", 5000.0)
                )

                st.session_state.storage_loaded = True

            except (ValueError, TypeError):
                st.warning("Unable to restore saved expenses.")

    if st.session_state.storage_dirty:

        data = {
            "expenses": st.session_state.expenses,
            "monthly_budget": st.session_state.monthly_budget
        }

        storage.setItem(
            STORAGE_KEY,
            json.dumps(data, default=str),
            key="finwise_browser_write"
        )

        st.session_state.storage_dirty = False
        st.session_state.storage_loaded = True


def save_data():

    initialize_database()

    st.session_state.storage_dirty = True