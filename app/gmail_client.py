import os
from email.utils import parsedate_to_datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


from config import SCOPES
from app.models import Email



def get_service():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def get_email_detail(service, message_id):
    email_data = service.users().messages().get(
        userId="me",
        id=message_id,
        format="metadata",
        metadataHeaders=["From", "Subject", "Date"]
    ).execute()

    headers = email_data["payload"]["headers"]

    info = {
        "From": "",
        "Subject": "",
        "Date": ""
    }

    for header in headers:
        name = header["name"]
        value = header["value"]

        if name in info:
            info[name] = value

    return Email(
        id=message_id,
        sender=info["From"],
        subject=info["Subject"],
        date=info["Date"],
        snippet=email_data.get("snippet", ""),
        received_at=parse_email_date(info["Date"])
    )


def get_recent_email_details(max_results=5):
    service = get_service()

    result = service.users().messages().list(
        userId="me",
        labelIds=["INBOX"],
        maxResults=max_results
    ).execute()

    messages = result.get("messages", [])

    emails = []

    for message in messages:
        email = get_email_detail(service, message["id"])
        emails.append(email)

    return emails

def get_all_email_details(max_results=500):
    service = get_service()

    emails = []
    page_token = None

    while True:
        result = service.users().messages().list(
            userId="me",
            labelIds=["INBOX"],
            maxResults=100,
            pageToken=page_token
        ).execute()

        messages = result.get("messages", [])

        for message in messages:
            email = get_email_detail(service, message["id"])
            emails.append(email)

            if len(emails) >= max_results:
                return emails

        page_token = result.get("nextPageToken")

        if not page_token:
            break

    return emails

def parse_email_date(date_text):
    if not date_text:
        return ""

    try:
        dt = parsedate_to_datetime(date_text)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return ""