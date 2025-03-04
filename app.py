import streamlit as st
import ollama
import database  # Import your database functions

OLLAMA_SERVER = "ngrok http --url=harmless-definite-chimp.ngrok-free.app 80"

# Streamlit app title
st.title('Symptom Checker')

# Navigation: Login / Register / Chat / Reset Password
menu = st.sidebar.radio("Navigation", ["Login", "Register", "Chat", "Reset Password"])

# Session state to track logged-in user
if "user" not in st.session_state:
    st.session_state.user = None

# 🟢 Register Page
if menu == "Register":
    st.subheader("Create an Account")
    username = st.text_input("Username")
    name = st.text_input("Full Name")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if username and name and password:
            success = database.register_user(username, name, password)
            if success:
                st.success("Account created successfully! Please login.")
            else:
                st.error("Username already exists. Try a different one.")
        else:
            st.error("All fields are required.")

# 🔵 Login Page
elif menu == "Login":
    st.subheader("Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if database.authenticate_user(username, password):
            st.session_state.user = username
            st.success("Login successful!")
            st.rerun()  # Refresh the page
        else:
            st.error("Invalid username or password.")

# 🟠 Password Reset Page
elif menu == "Reset Password":
    st.subheader("Reset Your Password")
    username = st.text_input("Enter your username")
    new_password = st.text_input("New Password", type="password")

    if st.button("Reset Password"):
        if username and new_password:
            success = database.reset_password(username, new_password)
            if success:
                st.success("Password reset successful! You can now log in with your new password.")
            else:
                st.error("Username not found. Please check your username.")
        else:
            st.error("Both fields are required.")

# 🟡 Chat Page (Only if logged in)
elif menu == "Chat":
    if st.session_state.user is None:
        st.warning("Please login first.")
        st.stop()

    st.subheader(f"Welcome, {st.session_state.user}!")
    st.write("Describe your symptoms, and I'll try to assist.")

    # Logout button
    if st.sidebar.button("Log Out"):
        st.session_state.user = None
        st.success("Logged out successfully!")
        st.rerun()  # Refresh the page

    # Load chat history
    chat_history = database.load_chat_history(st.session_state.user)
    for role, content in chat_history:
        with st.chat_message(role):
            st.write(content)

    # User input
    prompt = st.chat_input("What are your symptoms?")
    
    if prompt:
        with st.chat_message("user"):
            st.write(prompt)
        
        # Save user message to history
        database.save_message(st.session_state.user, "user", prompt)

        # Process AI response
        with st.spinner("Finding your symptoms..."):
            result = ollama.chat(model='llama3.2:3b', messages=[{"role": "user", "content": prompt}])
            response = result["message"]["content"]
        
        # Display AI response
        with st.chat_message("assistant"):
            st.write(response)

        # Save AI response to history
        database.save_message(st.session_state.user, "assistant", response)
