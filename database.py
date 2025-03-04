import sqlite3
import bcrypt

# Connect to SQLite database
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
        role TEXT,
        content TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS symptoms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        symptom TEXT,
        date_logged DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

# Register user (Create)
def register_user(username, name, password):
    conn = connect_db()
    cursor = conn.cursor()
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    try:
        cursor.execute("INSERT INTO users (username, name, password) VALUES (?, ?, ?)", (username, name, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Authenticate user (Read)
def authenticate_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode(), user[0].encode()):
        return True
    return False

# Update user details (Update)
def update_user(username, new_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = ? WHERE username = ?", (new_name, username))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success

# Delete user (Delete)
def delete_user(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success

# Reset password (Update)
def reset_password(username, new_password):
    conn = connect_db()
    cursor = conn.cursor()
    hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()

    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password, username))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success

# Save chat messages (Create)
def save_message(username, role, content):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (username, role, content) VALUES (?, ?, ?)", (username, role, content))
    conn.commit()
    conn.close()

# Load chat history (Read)
def load_chat_history(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, role, content, timestamp FROM chat_history WHERE username = ? ORDER BY timestamp", (username,))
    history = cursor.fetchall()
    conn.close()
    return history

# Delete a specific chat message (Delete)
def delete_message(message_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_history WHERE id = ?", (message_id,))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success

# Delete all chat messages for a user (Delete)
def delete_all_messages(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_history WHERE username = ?", (username,))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success

# Log a symptom (Create)
def log_symptom(username, symptom):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO symptoms (username, symptom) VALUES (?, ?)", (username, symptom))
    conn.commit()
    conn.close()

# Retrieve symptoms (Read)
def get_symptoms(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, symptom, date_logged FROM symptoms WHERE username = ? ORDER BY date_logged", (username,))
    symptoms = cursor.fetchall()
    conn.close()
    return symptoms

# Update a logged symptom (Update)
def update_symptom(symptom_id, new_symptom):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE symptoms SET symptom = ? WHERE id = ?", (new_symptom, symptom_id))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success

# Delete a symptom (Delete)
def delete_symptom(symptom_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM symptoms WHERE id = ?", (symptom_id,))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success

# Initialize database
create_tables()
