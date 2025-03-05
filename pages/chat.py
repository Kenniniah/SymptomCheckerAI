import streamlit as st
import requests
from database import get_conversations, save_message, load_chat_history, delete_conversation

# Use ngrok URL
OLLAMA_SERVER_URL = "https://f006-112-210-231-149.ngrok-free.app"

# Function to chat with Ollama
def chat_with_ollama(prompt):
    url = f"{OLLAMA_SERVER_URL}/api/chat"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "llama3",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json().get("message", {}).get("content", "Error: Unexpected response format.")
    except requests.exceptions.RequestException as e:
        return f"Error: Could not connect to Ollama ({str(e)})"

# Streamlit UI Setup
st.set_page_config(page_title="Chat", layout="wide")

st.title("Symptom Checker AI")

# Ensure the user is authenticated
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.warning("You need to log in first.")
    if st.button("Go to Login"):
        st.session_state["authenticated"] = False
        st.session_state["username"] = ""
        st.switch_page("app.py")  # Keep navigation as requested
    st.stop()

username = st.session_state["username"]
st.write(f"Welcome, {username}!")

# Sidebar for conversations
st.sidebar.title("Conversations")

# Load conversation list
conversations = get_conversations(username)
selected_convo = None

if conversations:
    selected_convo = st.sidebar.radio("Select a conversation:", conversations)

    # Ensure selected conversation is stored in session state
    if "selected_conversation" not in st.session_state or st.session_state["selected_conversation"] != selected_convo:
        st.session_state["selected_conversation"] = selected_convo
        st.session_state["messages"] = load_chat_history(username, selected_convo) if selected_convo else []

    # Delete conversation button
    if st.sidebar.button("🗑️ Delete Conversation") and selected_convo:
        delete_conversation(username, selected_convo)
        st.session_state["selected_conversation"] = None  # Reset selection
        st.session_state["messages"] = []  # Clear chat messages
        st.rerun()  # Refresh the UI after deletion
else:
    st.sidebar.write("No conversations found.")

# Logout button
if st.sidebar.button("🚪 Logout"):
    st.session_state["authenticated"] = False
    st.session_state["username"] = ""
    st.success("Logged out successfully!")
    st.switch_page("app.py")  # Keep navigation as requested

# Ensure messages exist in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for role, content in st.session_state["messages"]:
    avatar = "😷" if role == "user" else "🧑‍⚕️"
    with st.chat_message(role, avatar=avatar):
        st.write(content)

# Chat input with a Submit button
with st.form(key="chat_form"):
    prompt = st.text_input("Describe your symptoms:", key="user_input")
    submit_button = st.form_submit_button("Submit")

if submit_button and prompt and st.session_state.get("selected_conversation"):
    # Save user message
    save_message(username, "user", prompt, st.session_state["selected_conversation"])

    with st.spinner("Checking symptoms... Please wait."):  # **Added spinner here**
        response = chat_with_ollama(prompt)  # Use ngrok-based function

    # Save AI response
    save_message(username, "assistant", response, st.session_state["selected_conversation"])

    # Display chat messages
    with st.chat_message("user", avatar="😷"):
        st.write(prompt)
    with st.chat_message("assistant", avatar="🧑‍⚕️"):
        st.write(response)

    # Add response to session state to maintain chat history
    st.session_state["messages"].append(("user", prompt))
    st.session_state["messages"].append(("assistant", response))
