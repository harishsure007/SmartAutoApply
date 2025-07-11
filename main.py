import streamlit as st
import pandas as pd
import os
import json
import re
import spacy

# --- Local imports ---
from app_pages.login_page import login_user
from app_pages.logout_page import logout_page
from app_pages.compare_resume_page import compare_resume_page
from app_pages.dashboard_page import dashboard
from utils import load_last_page, save_current_page  # removed load_session here
from streamlit_extras.switch_page_button import switch_page
from app_pages.welcome_page import main as welcome_page

# --- OpenAI API Key ---
from config.config import OPENAI_API_KEY
import openai
openai.api_key = OPENAI_API_KEY

# --- NLP Setup ---
nlp = spacy.load("en_core_web_sm")

# --- Streamlit Config ---
st.set_page_config(page_title="Smart Auto-Apply", layout="wide")

# --- File Paths ---
SAVED_JOBS_FILE = "saved_jobs.csv"

# ----------- Removed load_session usage -----------
# username = load_session()
# if username and "logged_in" not in st.session_state:
#     st.session_state.logged_in = True
#     st.session_state.username = username
# --------------------------------------------------

# --- Main App Router ---
def main():
    # Initialize page state if missing
    if "page" not in st.session_state:
        st.session_state.page = "welcome"

    # Show login page if not logged in (except allow welcome page)
    if not st.session_state.get("logged_in", False) and st.session_state.page != "welcome":
        st.session_state.page = "login"
        login_user()
        st.stop()



    # Route based on current page
    if st.session_state.page == "📈 Dashboard":
        dashboard()

    elif st.session_state.page == "📄 Compare Resume":
        compare_resume_page()

    elif st.session_state.page == "📄 Resume Optimizer":
        from app_pages.cv_builder_page import cv_builder_page
        cv_builder_page()

    elif st.session_state.page == "🔓 Logout":
        logout_page()

    elif st.session_state.page == "welcome":
        welcome_page()

    else:
        st.warning("⚠️ Unknown page. Redirecting to Dashboard...")
        st.session_state.page = "📈 Dashboard"
        st.rerun()  # Use st.rerun() to refresh UI

# Run the app
if __name__ == "__main__":
    main()
