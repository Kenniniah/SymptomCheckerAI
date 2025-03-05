import sqlite3
import bcrypt

# Connect to database
def connect_db():
    return sqlite3.connect("chatbot.db", check_same_thread=False)

# Create tables
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        name TEXT,
        password TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        conversation TEXT,  -- Add conversation name
        role TEXT,
        content TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()

# Register user
def register_user(username, name, password):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, name, password) VALUES (?, ?, ?)", (username, name, password))
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
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode(), user[0].encode()):
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

# Initialize database
create_tables()
