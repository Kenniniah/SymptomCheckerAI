import streamlit as st
import ollama
from database import get_conversations, save_message, load_chat_history, delete_conversation

st.set_page_config(page_title="Chat", layout="wide")

st.title("Symptom Checker AI")

# Ensure the user is authenticated
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.warning("You need to log in first.")
    if st.button("Go to Login"):
        st.session_state["authenticated"] = False
        st.session_state["username"] = ""
        st.switch_page("app.py")  # Redirect to login
    st.stop()  # Prevents unauthorized users from seeing the chat page

username = st.session_state["username"]
st.write(f"Welcome, {username}!")

# Sidebar for saved conversations
st.sidebar.title("Conversations")

# Load conversation list
conversations = get_conversations(username)

if conversations:
    selected_convo = st.sidebar.radio("Select a conversation:", conversations)

    # Delete conversation button
    if st.sidebar.button("🗑️ Delete Conversation"):
        delete_conversation(username, selected_convo)
        st.rerun()  # Refresh sidebar after deletion

    # Load selected conversation
    if "selected_conversation" not in st.session_state or st.session_state["selected_conversation"] != selected_convo:
        st.session_state["selected_conversation"] = selected_convo
        st.session_state.messages = load_chat_history(username, selected_convo)
else:
    st.sidebar.write("No conversations found.")

# Logout button
if st.sidebar.button("🚪 Logout"):
    st.session_state["authenticated"] = False
    st.session_state["username"] = ""
    st.success("Logged out successfully!")
    st.switch_page("app.py")  # Redirect to login

# Display chat history
for role, content in st.session_state.get("messages", []):
    avatar = "😷" if role == "user" else "🧑‍⚕️"
    with st.chat_message(role, avatar=avatar):
        st.write(content)

# Chat input
prompt = st.text_input("Describe your symptoms:")

if prompt:
    save_message(username, "user", prompt, st.session_state["selected_conversation"])

    with st.spinner("Checking symptoms... Please wait."):
        result = ollama.chat(model="llama3.2:3b", messages=[{"role": "user", "content": prompt}])
        response = result["message"]["content"]

    save_message(username, "assistant", response, st.session_state["selected_conversation"])

    with st.chat_message("user", avatar="😷"):
        st.write(prompt)
    with st.chat_message("assistant", avatar="🧑‍⚕️"):
        st.write(response)
