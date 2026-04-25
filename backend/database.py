import sqlite3

def get_connection():
    conn = sqlite3.connect("task.db")
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(""" 
     CREATE TABLE IF NOT EXISTS tasks(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      title TEXT NOT NULL,
      description TEXT,
      date TEXT
     )
    """)

    conn.commit()
    conn.close()