import streamlit as st
from database import register_user, authenticate_user, update_user, reset_password, delete_user

# Session state initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Function to handle login
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful!")
            st.switch_page("chat.py")  # Redirect to chat after login
        else:
            st.error("Invalid credentials")

# Function to handle registration
def register():
    st.title("Register")
    username = st.text_input("Username")
    name = st.text_input("Full Name")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if register_user(username, name, password):
            st.success("Registration successful! Please login.")
        else:
            st.error("Username already exists!")

# Function to update user details
def update_profile():
    st.title("Update Profile")
    new_name = st.text_input("New Name", value="")
    if st.button("Update Name"):
        if update_user(st.session_state.username, new_name):
            st.success("Profile updated successfully!")
        else:
            st.error("Update failed!")

# Function to reset password
def reset_password_ui():
    st.title("Reset Password")
    new_password = st.text_input("New Password", type="password")
    if st.button("Reset Password"):
        if reset_password(st.session_state.username, new_password):
            st.success("Password updated successfully!")
        else:
            st.error("Reset failed!")

# Function to delete account
def delete_account():
    st.title("Delete Account")
    if st.button("Delete My Account"):
        if delete_user(st.session_state.username):
            st.session_state.logged_in = False
            st.success("Account deleted successfully!")
            st.switch_page("app.py")
        else:
            st.error("Account deletion failed!")

# Main app logic
def main():
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Go to", ["Login", "Register"])

    if choice == "Login":
        login()
    elif choice == "Register":
        register()

if __name__ == "__main__":
    main()
