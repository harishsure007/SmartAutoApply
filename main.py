import streamlit as st
import spacy
import openai

# Import your page modules
from app_pages.login_page import login_user
from app_pages.logout_page import logout_page
from app_pages.compare_resume_page import compare_resume_page
from app_pages.dashboard_page import dashboard
from app_pages.welcome_page import main as welcome_page
from app_pages.cv_builder_page import cv_builder_page


# Streamlit config - must be first Streamlit command in main.py
st.set_page_config(page_title="Smart Auto-Apply", layout="wide")

openai.api_key = st.secrets["openai_api_key"]

try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello in a creative way."}
        ],
        max_tokens=10
    )
    print("✅ OpenAI API test passed:", response.choices[0].message.content.strip())
except Exception as e:
    print("❌ OpenAI API test failed:", e)

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    st.error("❌ Failed to load spaCy model: " + str(e))
    st.stop()

# Main router function
def main():
    # Initialize page state if missing
    if "page" not in st.session_state:
        st.session_state.page = "welcome"

    # If not logged in, force login page (except welcome)
    if not st.session_state.get("logged_in", False) and st.session_state.page != "welcome":
        st.session_state.page = "login"
        login_user()
        st.stop()

    # Route pages
    if st.session_state.page == "welcome":
        welcome_page()
    elif st.session_state.page == "login":
        login_user()
    elif st.session_state.page == "📈 Dashboard":
        dashboard()
    elif st.session_state.page == "📄 Compare Resume":
        compare_resume_page()
    elif st.session_state.page == "📄 Resume Optimizer":
        cv_builder_page()
    elif st.session_state.page == "🔓 Logout":
        logout_page()
    else:
        st.warning("⚠️ Unknown page. Redirecting to Dashboard...")
        st.session_state.page = "📈 Dashboard"
        st.experimental_rerun()

if __name__ == "__main__":
    main()
