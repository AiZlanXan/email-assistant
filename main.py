from gmail_client import get_recent_email_details
from database import init_db, save_email, get_all_emails
from classifier import classify_email
from reporter import generate_report


def main():
    init_db()

    new_emails = get_recent_email_details(max_results=10)

    for email in new_emails:
        save_email(email)

    saved_emails = get_all_emails()

    categories = {}

    for email in saved_emails:
        category = classify_email(email)

        if category not in categories:
            categories[category] = []

        categories[category].append(email)

    generate_report(categories)


if __name__ == "__main__":
    main()