from gmail_client import get_recent_email_details
from database import init_db, save_email


def main():
    init_db()

    emails = get_recent_email_details(max_results=5)

    for email in emails:
        save_email(email)

        print("=" * 40)
        print("From:", email.sender)
        print("Subject:", email.subject)
        print("Date:", email.date)
        print("Snippet:", email.snippet)

    print("保存完成")


if __name__ == "__main__":
    main()