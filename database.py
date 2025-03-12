import sqlite3
import bcrypt

# Connect to database
def connect_db():
    return sqlite3.connect("chatbot.db", check_same_thread=False)

# Create tables
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    
    # Create users table if it does not exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        date_of_birth TEXT,
        gender TEXT,
        marital_status TEXT,
        occupancy TEXT,
        password TEXT
    );
    """)
    
    conn.commit()
    conn.close()

# Register user
def register_user(username, first_name, last_name, date_of_birth, gender, marital_status, occupancy, password):
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
        INSERT INTO users (username, first_name, last_name, date_of_birth, gender, marital_status, occupancy, password)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (username, first_name, last_name, date_of_birth, gender, marital_status, occupancy, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Verify user credentials
def verify_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT password FROM users WHERE username = ?
    """, (username,))
    result = cursor.fetchone()
    
    conn.close()
    
    if result and bcrypt.checkpw(password.encode(), result[0].encode()):
        return True
    return False

# Save chat messages with a conversation name
def save_message(username, conversation, role, content):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chat_history (username, conversation, role, content) VALUES (?, ?, ?, ?)", 
        (username, conversation, role, content)
    )
    conn.commit()
    conn.close()

# Load chat history for a specific conversation
def load_chat_history(username, conversation):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, content FROM chat_history WHERE username = ? AND conversation = ? ORDER BY timestamp",
        (username, conversation)
    )
    history = cursor.fetchall()
    conn.close()
    return history

# Get a list of all conversations for a user
def get_conversations(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT DISTINCT conversation FROM chat_history WHERE username = ?",
        (username,)
    )
    conversations = [row[0] for row in cursor.fetchall()]
    conn.close()
    return conversations

# Delete a specific conversation
def delete_conversation(username, conversation):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM chat_history WHERE username = ? AND conversation = ?",
        (username, conversation)
    )
    conn.commit()
    conn.close()

# Save biometric data
def save_biometrics(username, height, weight, blood_pressure, body_temperature, date_measured):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO biometrics (username, height, weight, blood_pressure, body_temperature, date_measured) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, (username, height, weight, blood_pressure, body_temperature, date_measured))
    conn.commit()
    conn.close()

# Initialize database
create_tables()