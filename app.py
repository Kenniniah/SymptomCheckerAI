import streamlit as st
import bcrypt
import sqlite3
import ollama

from database import register_user, reset_password, load_users, save_message, load_chat_history

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

# Function to verify user credentials
def verify_user(username, password):
    users = load_users()
    for user in users:
        if user["username"] == username and bcrypt.checkpw(password.encode(), user["password"].encode()):
            return True
    return False

# Function to handle login
def login():
    st.subheader("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        if verify_user(username, password):
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.rerun()  # Redirect to chat
        else:
            st.error("Invalid username or password")

# Function to handle registration
def register():
    st.subheader("Register")
    username = st.text_input("Username", key="register_username")
    name = st.text_input("Full Name")
    password = st.text_input("Password", type="password", key="register_password")
    if st.button("Register"):
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        if register_user(username, name, hashed_password):
            st.success("Registration successful! You can now log in.")
        else:
            st.error("Username already exists")

# Function to reset password
def reset():
    st.subheader("Reset Password")
    username = st.text_input("Enter your username")
    new_password = st.text_input("New Password", type="password")
    if st.button("Reset Password"):
        hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        if reset_password(username, hashed_password):
            st.success("Password reset successfully! Please login.")
        else:
            st.error("User not found")

# Function to display chat page
def chat():
    st.title("Chatbot")
    st.write(f"Welcome, {st.session_state['username']}!")

    if st.button("Logout"):
        st.session_state["authenticated"] = False
        st.session_state["username"] = ""
        st.rerun()

    prompt = st.chat_input("Enter your message")
    
    if prompt:
        save_message(st.session_state["username"], "user", prompt)

        result = ollama.chat(model="llama3.2:3b", messages=[{"role": "user", "content": prompt}])
        response = result["message"]["content"]

        save_message(st.session_state["username"], "assistant", response)
        
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            st.write(response)

    history = load_chat_history(st.session_state["username"])
    for role, content in history:
        with st.chat_message(role):
            st.write(content)

# **Main logic to determine which page to show**
if st.session_state["authenticated"]:
    chat()
else:
    st.title("Welcome to Symptom Checker")
    option = st.sidebar.radio("Select an option", ["Login", "Register", "Reset Password"])
    
    if option == "Login":
        login()
    elif option == "Register":
        register()
    elif option == "Reset Password":
        reset()
