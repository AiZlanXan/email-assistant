from app.gmail_client import get_recent_email_details, get_all_email_details
from app.database import (
    init_db,
    save_email,
    get_all_emails,
    update_email_classification
)
from app.classifier import classify_email
from app.reporter import generate_report
from app.profile_service import generate_email_profile


def process_emails(emails):
    for email in emails:
        save_email(email)

    saved_emails = get_all_emails()

    categories = {}

    for email in saved_emails:
        category, importance = classify_email(email)
        update_email_classification(email.id, category, importance)

        if category not in categories:
            categories[category] = []

        categories[category].append(email)

    return saved_emails, categories


def full_sync(max_results=500):
    print("开始全量同步邮件...")

    init_db()

    emails = get_all_email_details(max_results=max_results)

    saved_emails, categories = process_emails(emails)

    generate_email_profile(saved_emails)
    generate_report(categories)

    print("全量同步完成")


def sync_emails(max_results=10):
    print("开始增量同步邮件...")

    init_db()

    emails = get_recent_email_details(max_results=max_results)

    saved_emails, categories = process_emails(emails)

    generate_report(categories)

    print("增量同步完成")