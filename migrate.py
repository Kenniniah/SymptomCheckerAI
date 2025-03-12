import sqlite3

def connect_db():
    return sqlite3.connect("chatbot.db", check_same_thread=False)

def migrate():
    conn = connect_db()
    cursor = conn.cursor()
    
    # Create users table if it does not exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY
    );
    """)

    # Add new columns to the users table if they do not exist
    cursor.execute("ALTER TABLE users ADD COLUMN first_name TEXT")
    cursor.execute("ALTER TABLE users ADD COLUMN last_name TEXT")
    cursor.execute("ALTER TABLE users ADD COLUMN date_of_birth DATE")
    cursor.execute("ALTER TABLE users ADD COLUMN gender TEXT")
    cursor.execute("ALTER TABLE users ADD COLUMN marital_status TEXT")
    cursor.execute("ALTER TABLE users ADD COLUMN occupancy TEXT")

    # Create allergies table if it does not exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS allergies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        allergy TEXT,
        FOREIGN KEY (username) REFERENCES users (username)
    );
    """)

    # Create symptoms_history table if it does not exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS symptoms_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        date TEXT,
        symptom TEXT,
        FOREIGN KEY (username) REFERENCES users (username)
    );
    """)

    # Create biometrics table if it does not exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS biometrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        height TEXT,
        weight TEXT,
        blood_pressure TEXT,
        body_temperature TEXT,
        date_measured TEXT,
        FOREIGN KEY (username) REFERENCES users (username)
    );
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate()