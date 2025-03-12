from random import randint
import streamlit as st
import sqlite3
from datetime import datetime, timedelta

# Streamlit UI Setup
st.set_page_config(page_title="Demographics", layout="wide")

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

# Connect to database
def connect_db():
    return sqlite3.connect("chatbot.db", check_same_thread=False)

# Logout button
if st.sidebar.button("🚪 Logout"):
    st.session_state["authenticated"] = False
    st.session_state["username"] = ""
    st.success("Logged out successfully!")
    st.switch_page("app.py")  # Keep navigation as requested


# Fetch user demographics
def get_user_demographics(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT first_name, last_name, date_of_birth, gender, marital_status, occupancy 
        FROM users WHERE username = ?
    """, (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# Fetch user allergies
def get_user_allergies(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT allergy FROM allergies WHERE username = ?
    """, (username,))
    allergies = cursor.fetchall()
    conn.close()
    return [allergy[0] for allergy in allergies]

# Fetch user past symptoms history
def get_user_symptoms_history(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, symptom FROM symptoms_history WHERE username = ?
    """, (username,))
    symptoms_history = cursor.fetchall()
    conn.close()
    return symptoms_history

# Fetch user biometrics
def get_user_biometrics(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT height, weight, blood_pressure, body_temperature, date_measured 
        FROM biometrics WHERE username = ? ORDER BY date_measured DESC LIMIT 1
    """, (username,))
    biometrics = cursor.fetchone()
    conn.close()
    return biometrics

# Add symptom
def add_symptom(username, date, symptom):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO symptoms_history (username, date, symptom) VALUES (?, ?, ?)
    """, (username, date, symptom))
    conn.commit()
    conn.close()
    reload_symptoms()
    st.rerun()

# Update symptom
def update_symptom(username, date, old_symptom, new_symptom):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE symptoms_history SET symptom = ? WHERE username = ? AND symptom = ? AND date = ?
    """, (new_symptom, username, old_symptom, date))
    conn.commit()
    conn.close()
    reload_symptoms()
    st.rerun()

# Delete symptom
def delete_symptom(username, date, symptom):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM symptoms_history WHERE username = ? AND symptom = ? AND date = ?
    """, (username, symptom, date))
    conn.commit()
    conn.close()
    reload_symptoms()
    st.rerun()

# Reload symptoms from session state
def reload_symptoms():
    global yesterday_symptoms, previous_7_days_symptoms, previous_30_days_symptoms
    st.session_state["symptoms_history"] = get_user_symptoms_history(username)
    symptoms_history = [(datetime.strptime(date, "%Y-%m-%d").date(), symptom) for date, symptom in st.session_state["symptoms_history"]]
    yesterday_symptoms = [symptom for date, symptom in symptoms_history if date == yesterday]
    previous_7_days_symptoms = [symptom for date, symptom in symptoms_history if previous_7_days <= date < yesterday]
    previous_30_days_symptoms = [symptom for date, symptom in symptoms_history if previous_30_days <= date < previous_7_days]

# Reload allergies from session state
def reload_allergies():
    st.session_state["allergies"] = get_user_allergies(username)

# Display Basic User Information
user = get_user_demographics(username)
if "allergies" not in st.session_state:
    st.session_state["allergies"] = get_user_allergies(username)
if "symptoms_history" not in st.session_state:
    st.session_state["symptoms_history"] = get_user_symptoms_history(username)
biometrics = get_user_biometrics(username)

# Organize symptoms history by date
yesterday = (datetime.now() - timedelta(days=1)).date()
previous_7_days = (datetime.now() - timedelta(days=7)).date()
previous_30_days = (datetime.now() - timedelta(days=30)).date()

# Initial load of symptoms
reload_symptoms()

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Patient Basic Information")
    with st.form("Basic Information"):
        first_name = st.text_input("First Name", value=user[0] if user else "")
        last_name = st.text_input("Last Name", value=user[1] if user else "")
        date_of_birth = st.date_input("Date of Birth", value=datetime.strptime(user[2], "%Y-%m-%d") if user and user[2] else None)
        gender = st.radio("Gender", options=["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(user[3]) if user and user[3] in ["Male", "Female", "Other"] else 0)
        marital_status = st.selectbox("Marital Status", options=["Single", "Married", "Divorced", "Widowed"], index=["Single", "Married", "Divorced", "Widowed"].index(user[4]) if user and user[4] in ["Single", "Married", "Divorced", "Widowed"] else 0)
        occupancy = st.text_input("Occupancy", value=user[5] if user else "")
        
        submitted = st.form_submit_button("Save")
        if submitted:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users 
                SET first_name = ?, last_name = ?, date_of_birth = ?, gender = ?, marital_status = ?, occupancy = ? 
                WHERE username = ?
            """, (first_name, last_name, date_of_birth, gender, marital_status, occupancy, username))
            conn.commit()
            conn.close()

            messageNum = randint(1, 3)
            if messageNum == 1:
                st.success("You have successfully updated your basic information.")
            elif messageNum == 2:
                st.success("Your basic information has been updated.")
            else:
                st.success("Your basic information has been successfully updated.")

    st.subheader("Biometrics Data")
    with st.form("Biometrics Data"):
        height = st.text_input("Height (in cm)", value=biometrics[0] if biometrics else "")
        weight = st.text_input("Weight (in kg)", value=biometrics[1] if biometrics else "")
        blood_pressure = st.text_input("Blood Pressure", value=biometrics[2] if biometrics else "")
        body_temperature = st.text_input("Body Temperature (in Celsius)", value=biometrics[3] if biometrics else "")
        date_measured = st.date_input("Date Measured", value=datetime.strptime(biometrics[4], "%Y-%m-%d") if biometrics and biometrics[4] else None)
        
        submitted_biometrics = st.form_submit_button("Save")
        if submitted_biometrics:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO biometrics (username, height, weight, blood_pressure, body_temperature, date_measured) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (username, height, weight, blood_pressure, body_temperature, date_measured))
            conn.commit()
            conn.close()
            st.success("Biometrics data has been successfully updated.")

with col2:
    def load_allergy_list():
        for i, allergy in enumerate(st.session_state["allergies"]):
            cols = st.columns([3, 1, 1])
            updated_allergy = cols[0].text_input("Allergy", value=allergy, key=f"allergy_{i}")
            delete_button = cols[1].button("Delete", key=f"delete_allergy_{i}")
            update_button = cols[2].button("Update", key=f"update_allergy_{i}")
            if delete_button:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("""
                    DELETE FROM allergies WHERE username = ? AND allergy = ?
                """, (username, allergy))
                conn.commit()
                conn.close()
                reload_allergies()
                st.rerun()
            if update_button:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE allergies SET allergy = ? WHERE username = ? AND allergy = ?
                """, (updated_allergy, username, allergy))
                conn.commit()
                conn.close()
                reload_allergies()
                st.rerun()
                st.success(f"Allergy {allergy} updated successfully.")

    st.subheader("Allergies")
    with st.form("Add Allergy"):
        new_allergy = st.text_input("Add Allergy")
        add_allergy_button = st.form_submit_button("Add Allergy")
        if add_allergy_button and new_allergy:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO allergies (username, allergy) VALUES (?, ?)
            """, (username, new_allergy))
            conn.commit()
            conn.close()
            st.success("Allergy added successfully.")
            reload_allergies()
            st.rerun()

    load_allergy_list()  # for initial load

    st.subheader("Patient Past Symptoms History")
    with st.form("Add Yesterday's Symptom"):
        yesterday_symptom = st.text_input("Symptom for Yesterday")
        add_yesterday_symptom_button = st.form_submit_button("Add Yesterday's Symptom")
        if add_yesterday_symptom_button and yesterday_symptom:
            add_symptom(username, yesterday, yesterday_symptom)
            st.success("Symptom for yesterday added successfully.")

    st.write("Yesterday's Symptoms:")
    for i, symptom in enumerate(yesterday_symptoms):
        cols = st.columns([3, 1, 1])
        updated_symptom = cols[0].text_input("Symptom", value=symptom, key=f"yesterday_symptom_{i}")
        delete_button = cols[1].button("Delete", key=f"delete_yesterday_symptom_{i}")
        update_button = cols[2].button("Update", key=f"update_yesterday_symptom_{i}")
        if delete_button:
            delete_symptom(username, yesterday, symptom)
            reload_symptoms()
            st.rerun()
        if update_button:
            update_symptom(username, yesterday, symptom, updated_symptom)
            reload_symptoms()
            st.rerun()

    with st.form("Add Previous 7 Days Symptom"):
        previous_7_days_symptom = st.text_input("Symptom for Previous 7 Days")
        add_previous_7_days_symptom_button = st.form_submit_button("Add Previous 7 Days Symptom")
        if add_previous_7_days_symptom_button and previous_7_days_symptom:
            add_symptom(username, previous_7_days, previous_7_days_symptom)
            st.success("Symptom for previous 7 days added successfully.")

    st.write("Previous 7 Days Symptoms:")
    for i, symptom in enumerate(previous_7_days_symptoms):
        cols = st.columns([3, 1, 1])
        updated_symptom = cols[0].text_input("Symptom", value=symptom, key=f"previous_7_days_symptom_{i}")
        delete_button = cols[1].button("Delete", key=f"delete_previous_7_days_symptom_{i}")
        update_button = cols[2].button("Update", key=f"update_previous_7_days_symptom_{i}")
        if delete_button:
            delete_symptom(username, previous_7_days, symptom)
            reload_symptoms()
            st.rerun()
        if update_button:
            update_symptom(username, previous_7_days, symptom, updated_symptom)
            reload_symptoms()
            st.rerun()

    with st.form("Add Previous 30 Days Symptom"):
        previous_30_days_symptom = st.text_input("Symptom for Previous 30 Days")
        add_previous_30_days_symptom_button = st.form_submit_button("Add Previous 30 Days Symptom")
        if add_previous_30_days_symptom_button and previous_30_days_symptom:
            add_symptom(username, previous_30_days, previous_30_days_symptom)
            st.success("Symptom for previous 30 days added successfully.")

    st.write("Previous 30 Days Symptoms:")
    for i, symptom in enumerate(previous_30_days_symptoms):
        cols = st.columns([3, 1, 1])
        updated_symptom = cols[0].text_input("Symptom", value=symptom, key=f"previous_30_days_symptom_{i}")
        delete_button = cols[1].button("Delete", key=f"delete_previous_30_days_symptom_{i}")
        update_button = cols[2].button("Update", key=f"update_previous_30_days_symptom_{i}")
        if delete_button:
            delete_symptom(username, previous_30_days, symptom)
            reload_symptoms()
            st.rerun()
        if update_button:
            update_symptom(username, previous_30_days, symptom, updated_symptom)
            reload_symptoms()
            st.rerun()