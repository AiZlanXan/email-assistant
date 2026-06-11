from gmail_client import get_recent_email_details
from database import init_db, save_email, get_all_emails
from classifier import classify_email


def main():
    init_db()

    new_emails = get_recent_email_details(max_results=5)

    for email in new_emails:
        save_email(email)

    saved_emails = get_all_emails()

    categories = {}

    for email in saved_emails:
        category = classify_email(email)

        if category not in categories:
            categories[category] = []

        categories[category].append(email)

    print("\n📬 邮件分类结果\n")

    for category, emails in categories.items():
        print("=" * 40)
        print(f"【{category}】共 {len(emails)} 封")

        for email in emails:
            print("-", email.subject)


if __name__ == "__main__":
    main()