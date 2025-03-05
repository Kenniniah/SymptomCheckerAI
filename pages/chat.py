import streamlit as st
import requests
from database import get_conversations, save_message, load_chat_history, delete_conversation

# Use ngrok URL
#OLLAMA_SERVER_URL =  " https://ab12-112-210-231-149.ngrok-free.app"

# Function to chat with Ollama
def chat_with_ollama(prompt):
    OLLAMA_SERVER_URL = "https://ab12-112-210-231-149.ngrok-free.app"  # Ensure the URL is defined
    url = f"{OLLAMA_SERVER_URL}/api/chat"  # Define the API endpoint

    headers = {"Content-Type": "application/json"}
    data = {
        "model": "llama3.2:3b",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        response.raise_for_status()  # Raise an error if the request failed

        print("Raw response text:", response.text)  # Debugging line

        json_response = response.json()  # Attempt to parse JSON
        return json_response["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error: Could not connect to Ollama ({str(e)})"
    except ValueError as e:  # Handles JSON decoding issues
        return f"Error: Invalid JSON response from Ollama ({str(e)})"


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
    if "selected_conversation" not in st.session_state:
        st.session_state["selected_conversation"] = None  # Ensure it's always initialized

if selected_convo and st.session_state["selected_conversation"] != selected_convo:

        st.session_state["selected_conversation"] = selected_convo
        st.session_state["messages"] = load_chat_history(username, selected_convo)

    # Delete conversation button
    if st.sidebar.button("🗑️ Delete Conversation"):
        delete_conversation(username, selected_convo)
        st.session_state["selected_conversation"] = None  # Reset selection
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

# Chat input
prompt = st.text_input("Describe your symptoms:")

if prompt:
    # Save user message
    save_message(username, "user", prompt, st.session_state["selected_conversation"])

    with st.spinner("Checking symptoms... Please wait."):
        response = chat_with_ollama(prompt)  # Use ngrok-based function

    # Save AI response
    save_message(username, "assistant", response, st.session_state["selected_conversation"])

    # Display chat messages
    with st.chat_message("user", avatar="😷"):
        st.write(prompt)
    with st.chat_message("assistant", avatar="🧑‍⚕️"):
        st.write(response)
