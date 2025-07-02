import streamlit as st
import base64

# Function to set background image
def set_background(image_path):
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
        background-color: rgba(255, 255, 255, 0.90);
        border-radius: 12px;
        padding: 2rem;
        margin-top: 3rem;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }}
    .hero-text h1 {{
        font-size: 3rem;
        color: #1f3b4d;
        text-align: center;
    }}
    .hero-sub {{
        font-size: 1.5rem;
        color: #444;
        text-align: center;
        margin-bottom: 2rem;
    }}
    .feature-box {{
        background-color: #f2f2f2;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Main welcome page
def main():
    st.set_page_config(page_title="Smart Auto-Apply", layout="centered")
    set_background("image dashboard.png")  # Replace with your actual image file name

    # Hero Section
    st.markdown("<div class='hero-text'><h1>Smart Auto-Apply</h1></div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-sub'>Automate your job search with AI. Match. Apply. Track.</div>", unsafe_allow_html=True)

    # CTA Button
    if st.button("\ud83d\ude80 Get Started"):
        st.switch_page("login.py")  # Or "pages/login.py" if you use multi-page structure

    # Feature Highlights
    st.markdown("### \ud83d\udd0d Features")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='feature-box'>\ud83e\udde0 AI Resume Parser<br><small>Extracts and analyzes your resume instantly.</small></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='feature-box'>🤖 Smart Matching<br><small>Matches jobs using NLP & TF-IDF.</small></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='feature-box'>📄 Auto Apply<br><small>Fills job applications automatically.</small></div>", unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown("<div class='feature-box'>📊 Dashboard<br><small>Tracks applied jobs & match score.</small></div>", unsafe_allow_html=True)
    with col5:
        st.empty()
    with col6:
        st.empty()

    # Footer
    st.markdown("---")
    st.markdown("Made with ❤️ by Harish Kumar Sure")

# Run
if __name__ == "__main__":
    main()
