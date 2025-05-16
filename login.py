import streamlit as st
import pandas as pd
import os
import base64

# Dummy credentials file (extend or replace with secure DB in production)
USERS = {
    "admin": "admin123",
    "user": "user123"
}

# Centered layout with optional background styling
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f5f8fa;
    padding-top: 3rem;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
h1 {
    text-align: center;
    font-size: 2.2rem;
}
.login-box {
    max-width: 400px;
    margin: 0 auto;
    background-color: #ffffff;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0px 0px 8px rgba(0,0,0,0.1);
}
input[type="password"]::-ms-reveal,
input[type="password"]::-ms-clear {
    display: none;
}
</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)


def login():
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.markdown("<h1>Smart Auto-Apply Login</h1>", unsafe_allow_html=True)

    username = st.text_input("Username")

    # Password input with eye toggle using Streamlit components
    pw_col1, pw_col2 = st.columns([9, 1])
    with pw_col1:
        password = st.text_input("Password", type="password", key="password")
    with pw_col2:
        show_icon = st.checkbox("👁", label_visibility="collapsed", key="toggle_pw")

    if show_icon:
        st.session_state["password"] = st.text_input("Re-enter Password", type="default", label_visibility="collapsed", value=st.session_state.get("password", ""), key="visible_pw")
        password = st.session_state["password"]

    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome, {username}!")
        else:
            st.error("❌ Invalid username or password")

    # Reset password placeholder
    with st.expander("🔁 Forgot Password?"):
        st.info("Password reset feature is under development.")
        st.text_input("Enter your email")
        st.button("Send Reset Link")

    # Sign-up form (demo)
    st.markdown("---")
    st.subheader("🆕 New Here? Create an Account")
    new_user = st.text_input("New Username", key="signup_user")
    new_pw = st.text_input("New Password", type="password", key="signup_pw")
    if st.button("Sign Up"):
        if new_user and new_pw:
            st.success("✅ Account created successfully (demo-only)")
        else:
            st.warning("Please fill both fields to sign up.")

    st.markdown("</div>", unsafe_allow_html=True)
