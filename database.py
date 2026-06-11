import sqlite3

DB_NAME = "emails.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id TEXT PRIMARY KEY,
            sender TEXT,
            subject TEXT,
            date TEXT,
            snippet TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_email(email):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO emails (id, sender, subject, date, snippet)
        VALUES (?, ?, ?, ?, ?)
    """, (
        email.id,
        email.sender,
        email.subject,
        email.date,
        email.snippet
    ))

    conn.commit()
    conn.close()