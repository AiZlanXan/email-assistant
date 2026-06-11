from gmail_client import get_recent_email_details


def main():
    emails = get_recent_email_details(max_results=5)

    for email in emails:
        print("=" * 40)
        print("From:", email.sender)
        print("Subject:", email.subject)
        print("Date:", email.date)
        print("Snippet:", email.snippet)


if __name__ == "__main__":
    main()