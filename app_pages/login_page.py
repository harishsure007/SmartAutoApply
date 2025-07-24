import streamlit as st
import json
import os
import base64

SESSION_FILE = "user_profile.json"
USERS_FILE = "users.json"  # File to store registered users

# Load users from JSON file
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

# Save users to JSON file
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

# Save session
def save_session(username):
    with open(SESSION_FILE, "w") as f:
        json.dump({"username": username}, f)

# Clear session
def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

# Set background image with base64 encoding
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
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed;
    }}
    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.85);
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Login/Register UI
def login_user():

    # Set background image (adjust path if needed)
    set_background("image dashboard.png")

    st.title("🚀 Smart Auto-Apply")

    users = load_users()
    option = st.radio("Choose an option", ["Login", "Register"], horizontal=True)

    if option == "Login":
        st.subheader("🔐 Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            if username in users and users[username] == password:
                # Set session state flags on successful login
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.page = "📈 Dashboard"
                save_session(username)  # Optional: save session for persistent login
                st.success(f"✅ Welcome, {username}!")
                st.experimental_rerun()  # Refresh app to go to dashboard
            else:
                st.error("🚫 Invalid username or password")

    else:
        st.subheader("🆕 Register")
        new_user = st.text_input("New Username", key="register_username")
        new_pass = st.text_input("New Password", type="password", key="register_password")
        confirm_pass = st.text_input("Confirm Password", type="password", key="confirm_password")

        if st.button("Register"):
            if not new_user or not new_pass:
                st.warning("⚠️ Please fill in all fields.")
            elif new_user in users:
                st.warning("⚠️ Username already exists.")
            elif new_pass != confirm_pass:
                st.warning("⚠️ Passwords do not match.")
            else:
                users[new_user] = new_pass
                save_users(users)
                st.success("✅ Account created. You can now login.")

# Run login only if this file is executed directly
if __name__ == "__main__":
    login_user()
