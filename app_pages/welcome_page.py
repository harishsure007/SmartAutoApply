import streamlit as st
import base64
import os

# Set background and custom styles
def set_background(image_path):
    if not os.path.exists(image_path):
        st.error(f"⚠️ Background image '{image_path}' not found.")
        return

    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        padding: 2rem 3rem;
        margin-top: 1rem;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }}

    div.stButton > button:first-child {{
        background-color: transparent;
        color: #ffffff;
        padding: 0.5rem 1.2rem;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 500;
        cursor: pointer;
        border: 2px solid #ffffff;
        transition: background-color 0.3s ease, color 0.3s ease;
        width: 100%;
        max-width: 100px;
    }}

    div.stButton > button:first-child:hover {{
        background-color: #ffffff;
        color: #1f3b4d;
    }}

    .features-container {{
        display: flex;
        justify-content: center;
        max-width: 1200px;
        margin: 0 auto 3rem auto;
        gap: 1rem;
        flex-wrap: wrap;
    }}

    .feature-box {{
        background-color: #f8f9fa;
        border-radius: 12px;
        padding: 1.5rem 1rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05);
        flex: 1 1 200px;
        max-width: 180px;
        height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        transition: transform 0.2s ease;
        cursor: default;
    }}

    .feature-box:hover {{
        transform: translateY(-6px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.15);
    }}

    .feature-box b {{
        font-size: 1.1rem;
        color: #1f3b4d;
        margin-bottom: 0.5rem;
    }}

    .feature-box small {{
        font-size: 0.9rem;
        color: #555;
    }}

    .footer {{
        text-align: center;
        font-size: 0.9rem;
        color: gray;
        margin-top: 4rem;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Render Header
def render_header():
    col1, col2, col3, col4, col5 = st.columns([5, 1, 0.3, 1, 0.2])
    with col2:
        if st.button("Help"):
            st.info("📘 Need assistance? Contact: support@smartautoapply.com")
    with col4:
        if st.button("Login", key="header_login"):
            st.session_state.page = "login"
            st.rerun()

# Main content
def main():
    st.set_page_config(page_title="Smart Auto-Apply", layout="centered")
    set_background("image dashboard.png")

    render_header()

    st.markdown("<h1 style='color: white; text-align: center;'>Welcome to Smart Auto-Apply</h1>", unsafe_allow_html=True)
    st.markdown(
        "<div style='text-align: center; font-size: 1.2rem; color: #fff;'>"
        "Your intelligent assistant to simplify job searching. Automate resume matching, job scraping, and applications with one click."
        "</div><br>",
        unsafe_allow_html=True
    )

    # Feature Boxes
    features_html = """
    <div class="features-container">
        <div class="feature-box"><b>🧠 AI Resume Parsing</b><small>Extract key info using NLP.</small></div>
        <div class="feature-box"><b>🤖 Smart Matching</b><small>Match jobs using TF-IDF & semantic similarity.</small></div>
        <div class="feature-box"><b>📄 One-Click Apply</b><small>Auto-fill job applications instantly.</small></div>
        <div class="feature-box"><b>📊 Dashboard</b><small>Track match scores & application status.</small></div>
        <div class="feature-box"><b>🗂️ Resume Comparisons</b><small>Optimize resumes for every job.</small></div>
        <div class="feature-box"><b>☁️ Cloud Support</b><small>Run securely on AWS or GCP.</small></div>
    </div>
    """
    st.markdown(features_html, unsafe_allow_html=True)

    # Footer
    st.markdown(
        "<div class='footer'>🚀 Your AI assistant to find and apply for jobs — quickly, easily, and intelligently.</div>",
        unsafe_allow_html=True
    )

# Run
if __name__ == "__main__":
    main()
