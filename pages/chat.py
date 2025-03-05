import streamlit as st
import ollama
import time
import requests
from database import save_message, load_chat_history, delete_conversation

OLLAMA_URL = "ngrok http  https://296e-112-210-231-149.ngrok-free.app=harmless-definite-chimp.ngrok-free.app 80"  # Replace with your actual ngrok or Cloudflare URL

def get_response(prompt):
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={"model": "llama3", "messages": [{"role": "user", "content": prompt}]}
        )

        # Check if the request was successful
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get("message", {}).get("content", "No response received.")
        else:
            return f"Error: Received status code {response.status_code} from API."

    except requests.exceptions.RequestException as e:
        return f"Error: Unable to connect to the server. Details: {str(e)}"

# Ensure the user is authenticated
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.warning("You need to log in first.")
    st.button("Go to Login", on_click=lambda: st.session_state.update(authenticated=False, username=""))
    st.switch_page("app.py")
    st.stop()  # Prevents the rest of the page from being displayed

st.write(f"Welcome, {st.session_state['username']}!")

# Logout functionality
if st.button("Logout"):
    st.session_state["authenticated"] = False
    st.session_state["username"] = ""
    st.success("Logged out successfully!")
    st.switch_page("app.py")  # Switch to login page after logout

# Display chat history (only once)
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display previous chat history
for role, content in load_chat_history(st.session_state["username"]):
    st.session_state.messages.append({"role": role, "content": content})

    if role == "user":
        avatar = "😷"  # Emoji for the user
    else:
        avatar = "🧑‍⚕️"  # Emoji for the assistant

    with st.chat_message(role):
        st.write(content)

# Chat input and interaction
prompt = st.text_input("Describe your symptoms:")

def stream_data(text, delay: float = 0.02):
    """Streams the response word by word with a specified delay."""
    sentences = text.split('. ')
    for sentence in sentences:
        yield sentence + '. '
        time.sleep(delay)

if prompt:
    # Save user message
    save_message(st.session_state["username"], "user", prompt)

    # Show a spinner while the Symptom Checker AI processes the request
    with st.spinner("Checking symptoms... Please wait."):
        # Get assistant's response using Ollama

    # Save assistant's response
        save_message(st.session_state["username"], "assistant", response_text)

    # Display user message
    with st.chat_message("user", avatar="😷"):
        st.write(prompt)

    # Display assistant response
    with st.chat_message("assistant", avatar="🧑‍⚕️"):
        message_placeholder = st.empty()
        streamed_text = ""
        for chunk in stream_data(response_text):
            streamed_text += chunk
            message_placeholder.markdown(streamed_text)

# Option to delete conversation
if st.button("Delete Conversation"):
    delete_conversation(st.session_state["username"])
    st.success("Conversation deleted successfully!")
    st.session_state.messages = []