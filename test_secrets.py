import streamlit as st

# Load and show API Key (use lowercase key from secrets.toml)
openai_key = st.secrets["openai_api_key"]

st.success("✅ OpenAI API Key loaded:")
st.code(openai_key)

# Add rerun button
if st.button("Rerun App"):
    st.rerun()
