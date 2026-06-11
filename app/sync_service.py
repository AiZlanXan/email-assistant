from app.gmail_client import get_recent_email_details
from app.database import (
    init_db,
    save_email,
    get_all_emails,
    update_email_classification
)
from app.classifier import classify_email
from app.reporter import generate_report


def sync_emails(max_results=10):
    print("开始同步邮件...")

    init_db()

    new_emails = get_recent_email_details(max_results=max_results)

    for email in new_emails:
        save_email(email)

    saved_emails = get_all_emails()

    categories = {}

    for email in saved_emails:
        category, importance = classify_email(email)
        update_email_classification(email.id, category, importance)

        if category not in categories:
            categories[category] = []

        categories[category].append(email)

    generate_report(categories)

    print("同步完成")