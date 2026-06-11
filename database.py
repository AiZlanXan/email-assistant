import sqlite3

from models import Email

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
        INSERT OR IGNORE INTO emails
        (id, sender, subject, date, snippet)
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


def get_all_emails():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, sender, subject, date, snippet
        FROM emails
        ORDER BY rowid DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    emails = []

    for row in rows:
        emails.append(
            Email(
                id=row[0],
                sender=row[1],
                subject=row[2],
                date=row[3],
                snippet=row[4]
            )
        )

    return emails