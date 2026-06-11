import sqlite3

from app.models import Email

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

    add_column_if_not_exists(
        cursor,
        "emails",
        "category",
        "TEXT DEFAULT '未分类'"
    )

    add_column_if_not_exists(
        cursor,
        "emails",
        "importance",
        "INTEGER DEFAULT 0"
    )

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
        CREATE TABLE IF NOT EXISTS emails (
            id TEXT PRIMARY KEY,
            sender TEXT,
            subject TEXT,
            date TEXT,
            snippet TEXT,
            category TEXT DEFAULT '未分类',
            importance INTEGER DEFAULT 0
        )
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

def update_email_classification(email_id, category, importance):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE emails
        SET category = ?, importance = ?
        WHERE id = ?
    """, (
        category,
        importance,
        email_id
    ))

    conn.commit()
    conn.close()

def add_column_if_not_exists(cursor, table_name, column_name, column_definition):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()

    existing_columns = []

    for column in columns:
        existing_columns.append(column[1])

    if column_name not in existing_columns:
        cursor.execute(
            f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}"
        )