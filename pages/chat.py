import streamlit as st
import ollama
from database import save_message, load_chat_history

st.title("Chatbot")

if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.switch_page("app.py")  # Redirect to login if not authenticated

st.write(f"Welcome, {st.session_state['username']}!")

if st.button("Logout"):
    st.session_state["authenticated"] = False
    st.session_state["username"] = ""
    st.switch_page("app.py")  # Redirect to login

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
