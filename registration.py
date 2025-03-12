import streamlit as st
import bcrypt
from database import register_user

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