import streamlit as st
import bcrypt
from database import register_user, verify_user

st.title("Welcome to Symptom Checker")

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
            st.switch_page("pages/chat.py")  # Redirect to chat
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
            st.success("Registration successful! Redirecting to login...")
            st.switch_page("pages/chat.py")  # Redirect to chat
        else:
            st.error("Username already exists")

# Choose between Login & Register
option = st.sidebar.radio("Select an option", ["Login", "Register"])
if option == "Login":
    login()
else:
    register()