import streamlit as st
import ollama
from database import save_message, load_chat_history

st.title("Chatbot")

# Ensure the user is authenticated
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.warning("You need to log in first.")
    st.button("Go to Login", on_click=lambda: st.session_state.update(authenticated=False, username=""))
    st.stop()  # Prevents the rest of the page from being displayed

st.write(f"Welcome, {st.session_state['username']}!")

# Logout functionality
if st.button("Logout"):
    st.session_state["authenticated"] = False
    st.session_state["username"] = ""
    st.success("Logged out successfully!")
    st.rerun()  # Redirect to login page

# Display chat history (only once)
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display previous chat history
for role, content in load_chat_history(st.session_state["username"]):
    st.session_state.messages.append({"role": role, "content": content})
    with st.chat_message(role):
        st.write(content)

# Chat input and interaction
prompt = st.text_input("Enter your message:")

if prompt:
    # Save user message
    save_message(st.session_state["username"], "user", prompt)

    # Get assistant's response using Ollama
    result = ollama.chat(model="llama3.2:3b", messages=[{"role": "user", "content": prompt}])
    response = result["message"]["content"]

    # Save assistant's response
    save_message(st.session_state["username"], "assistant", response)

    # Display the new messages
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        st.write(response)
