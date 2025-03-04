import streamlit as st
from database import save_message, load_chat_history, delete_message, delete_all_messages
from database import log_symptom, get_symptoms, update_symptom, delete_symptom

# Ensure user is logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.switch_page("app.py")

st.title("Chat & Symptom Tracker")
username = st.session_state.username

# --- Chat Interface ---
st.subheader("Chat History")
chat_history = load_chat_history(username)

# Display chat messages
for msg in chat_history:
    message_id, role, content, timestamp = msg
    st.write(f"**{role.capitalize()}**: {content}  ⏳ {timestamp}")
    if st.button(f"Delete Message {message_id}", key=f"delete_{message_id}"):
        delete_message(message_id)
        st.rerun()

# Input new message
new_message = st.text_area("Enter your message:")
if st.button("Send Message"):
    save_message(username, "user", new_message)
    st.rerun()

# Clear chat
if st.button("Delete All Messages"):
    delete_all_messages(username)
    st.rerun()

# --- Symptom Tracker ---
st.subheader("Log Symptoms")
new_symptom = st.text_input("Enter your symptom")
if st.button("Log Symptom"):
    log_symptom(username, new_symptom)
    st.success("Symptom logged successfully!")
    st.rerun()

# Display symptoms
st.subheader("Your Symptoms")
symptoms = get_symptoms(username)

for symptom in symptoms:
    symptom_id, symptom_text, date_logged = symptom
    st.write(f"**{symptom_text}** (Logged: {date_logged})")

    # Update symptom
    updated_text = st.text_input(f"Update Symptom {symptom_id}", value=symptom_text, key=f"update_{symptom_id}")
    if st.button(f"Update {symptom_id}", key=f"update_button_{symptom_id}"):
        update_symptom(symptom_id, updated_text)
        st.rerun()

    # Delete symptom
    if st.button(f"Delete {symptom_id}", key=f"delete_symptom_{symptom_id}"):
        delete_symptom(symptom_id)
        st.rerun()

# Logout button
if st.button("Logout"):
    st.session_state.logged_in = False
    st.switch_page("app.py")
