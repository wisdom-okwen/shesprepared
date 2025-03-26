import sqlite3

DB_FILE = "chat_history.db"

def init_db():
    """Initialize database and create table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            bot TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_history(user, bot):
    """Save chat history in the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (user, bot) VALUES (?, ?)", (user, bot))
    conn.commit()
    conn.close()

def load_history(limit=12):
    """Load the last N messages from chat history."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT user, bot FROM chat_history ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [{"user": row[0], "bot": row[1]} for row in reversed(rows)]


def get_last_bot_response():
    """Fetch the last bot response from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT bot FROM chat_history ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else "No previous response available."


def clear_history():
    """Clear all chat history from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_history")
    conn.commit()
    conn.close()

def get_all():
    """Get all chat history."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chat_history")
    responses = cursor.fetchall()
    return responses
    

if __name__ == '__main__':
    # init_db()
    print(get_all())