import streamlit as st
import bcrypt
from database import register_user, verify_user

st.set_page_config(page_title="Login", layout="centered")

st.title("Login to Symptom Checker AI")

# Check authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""

# User Login
with st.form("login_form"):
    st.subheader("Login")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    submitted = st.form_submit_button("Login")

    if submitted:
        if verify_user(username, password):
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.success("Login successful! Redirecting...")
            st.rerun()  # Rerun app to process login

# If authenticated, redirect to chat.py
if st.session_state["authenticated"]:
    st.switch_page("pages/chat.py")

# User Registration
with st.form("register_form"):
    st.subheader("Register")
    new_username = st.text_input("New Username", key="register_user")
    new_name = st.text_input("Full Name", key="register_name")
    new_password = st.text_input("New Password", type="password", key="register_pass")
    register_submit = st.form_submit_button("Register")

    if register_submit:
        hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        if register_user(new_username, new_name, hashed_password):
            st.success("Registration successful! You can now log in.")
        else:
            st.error("Username already exists. Try another one.")
