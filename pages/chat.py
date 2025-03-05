import streamlit as st
import ollama
import time
from database import save_message, load_chat_history, delete_conversation

OLLAMA_SERVER = "ngrok http --url=harmless-definite-chimp.ngrok-free.app 80"

st.title("Symptom Checker AI")

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
        result = ollama.chat(model="llama3.2:3b", messages=[{"role": "user", "content": prompt}])
        response = result["message"]["content"]

    # Save assistant's response
    save_message(st.session_state["username"], "assistant", response)

    # Display the response
    with st.chat_message("user", avatar="😷"):  # User's emoji
        st.write(prompt)

    # Display usr message
    with st.chat_message("assistant", avatar="🧑‍⚕️"):  # Assistant's emoji
        response_text = ""  # Define response_text before use
        message_placeholder = st.empty()  # Placeholder for the message
        for chunk in stream_data(response):
            response_text += chunk  # Accumulate words into a complete response
            message_placeholder.markdown(response_text)  # Display accumulated response
            

# Option to delete entire conversation history
if st.button("Delete Conversation"):
    delete_conversation(st.session_state["username"])
    st.success("Conversation deleted successfully!")
    st.session_state.messages = []  # Clear chat history
    # Display the new messages
    #with st.chat_message("user"):
    #    st.write(prompt)
    #with st.chat_message("assistant"):
    #    st.write(response)