import streamlit as st
import bcrypt
from database import register_user, verify_user

st.title("Welcome to Symptom Checker AI")

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

# Login Page
def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if verify_user(username, password):
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.success(f"Welcome {username}!")
            st.switch_page("pages/chat.py")  # Refresh the page after login
        else:
            st.error("Invalid username or password")

# Register Page
def register():
    st.subheader("Register")
    username = st.text_input("Username")
    name = st.text_input("Full Name")
    password = st.text_input("Password", type="password")
    
    if st.button("Register"):
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        if register_user(username, name, hashed_password):
            st.success("Registration successful! Please log in.")
            st.switch_page("pages/chat.py")  # Refresh to show login page
        else:
            st.error("Username already exists")

# Reset Password
def reset():
    st.subheader("Reset Password")
    username = st.text_input("Username")
    new_password = st.text_input("New Password", type="password")
    
    if st.button("Reset Password"):
        if reset_password(username, new_password):
            st.success("Password reset successful!")
            st.switch_page("app.py")  # Switch back to login page after password reset
        else:
            st.error("Failed to reset password. Please check the username.")

# Choose between Login, Register, or Reset Password
option = st.sidebar.radio("Select an option", ["Login", "Register", "Reset Password"])
if option == "Login":
    login()
elif option == "Register":
    register()
else:
    reset()
