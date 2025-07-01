import streamlit as st
from login import clear_session

def logout_page():
    st.title("🔒 Logging out...")

    # Clear session file (persistent login data)
    clear_session()

    # Clear session state but keep page so app knows to show login page
    keys_to_keep = ["page"]  # You can add others you want to preserve
    for key in list(st.session_state.keys()):
        if key not in keys_to_keep:
            del st.session_state[key]

    # Set page to login and logged_in to False
    st.session_state["logged_in"] = False
    st.session_state["page"] = "login"

    st.success("✅ You have been logged out. Please log in again.")

    # Use rerun to refresh UI
    st.experimental_rerun()
