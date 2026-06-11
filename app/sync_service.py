from datetime import datetime

from app.gmail_client import get_recent_email_details, get_all_email_details
from app.database import (
    init_db,
    save_email,
    get_all_emails,
    get_emails_by_date,
    update_email_classification
)
from app.classifier import classify_email
from app.reporter import generate_report
from app.profile_service import generate_email_profile


def build_categories(emails):
    categories = {}

    for email in emails:
        category, importance = classify_email(email)
        update_email_classification(email.id, category, importance)

        if category not in categories:
            categories[category] = []

        categories[category].append(email)

    return categories


def save_emails(emails):
    for email in emails:
        save_email(email)


def full_sync(max_results=500):
    print("开始全量同步邮件...")

    init_db()

    emails = get_all_email_details(max_results=max_results)
    save_emails(emails)

    all_emails = get_all_emails()
    build_categories(all_emails)

    generate_email_profile(all_emails)

    today = datetime.now().strftime("%Y-%m-%d")
    today_emails = get_emails_by_date(today)
    today_categories = build_categories(today_emails)

    generate_report(today_categories)

    print("全量同步完成")


def sync_emails(max_results=20):
    print("开始增量同步邮件...")

    init_db()

    emails = get_recent_email_details(max_results=max_results)
    save_emails(emails)

    today = datetime.now().strftime("%Y-%m-%d")
    today_emails = get_emails_by_date(today)
    today_categories = build_categories(today_emails)

    generate_report(today_categories)

    print("增量同步完成")