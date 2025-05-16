import streamlit as st
from login import login

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
else:
    st.success(f"✅ Welcome, {st.session_state.username}!")
