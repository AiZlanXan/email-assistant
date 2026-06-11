import os
import sqlite3

from app.models import Email

DB_NAME = os.path.join("data", "emails.db")


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


def init_db():
    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id TEXT PRIMARY KEY,
            sender TEXT,
            subject TEXT,
            date TEXT,
            snippet TEXT,
            received_at TEXT,
            category TEXT DEFAULT '未分类',
            importance INTEGER DEFAULT 0
        )
    """)

    add_column_if_not_exists(cursor, "emails", "received_at", "TEXT")
    add_column_if_not_exists(cursor, "emails", "category", "TEXT DEFAULT '未分类'")
    add_column_if_not_exists(cursor, "emails", "importance", "INTEGER DEFAULT 0")

    conn.commit()
    conn.close()


def save_email(email):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO emails
        (id, sender, subject, date, snippet, received_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        email.id,
        email.sender,
        email.subject,
        email.date,
        email.snippet,
        email.received_at
    ))

    conn.commit()
    conn.close()


def get_emails_by_date(date_text):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    start_time = f"{date_text} 00:00:00"
    end_time = f"{date_text} 23:59:59"

    cursor.execute("""
        SELECT id, sender, subject, date, snippet, received_at
        FROM emails
        WHERE received_at >= ? AND received_at <= ?
        ORDER BY received_at DESC
    """, (start_time, end_time))

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
                snippet=row[4],
                received_at=row[5]
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


def get_emails_by_month(year, month):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    start_date = f"{year}-{month:02d}-01 00:00:00"

    if month == 12:
        end_date = f"{year + 1}-01-01 00:00:00"
    else:
        end_date = f"{year}-{month + 1:02d}-01 00:00:00"

    cursor.execute("""
        SELECT id, sender, subject, date, snippet, received_at
        FROM emails
        WHERE received_at >= ? AND received_at < ?
        ORDER BY received_at DESC
    """, (start_date, end_date))

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
                snippet=row[4],
                received_at=row[5]
            )
        )

    return emails


def has_emails():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM emails")
    count = cursor.fetchone()[0]

    conn.close()

    return count > 0

def get_all_emails():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, sender, subject, date, snippet, received_at
        FROM emails
        ORDER BY received_at DESC
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
                snippet=row[4],
                received_at=row[5]
            )
        )

    return emails