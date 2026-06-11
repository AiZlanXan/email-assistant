import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# 只读 Gmail，不会删除/发送邮件
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_gmail_service():
    creds = None

    # token.json 是第一次授权成功后自动生成的
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # 如果还没有登录，或者登录失效，就重新授权
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

    service = build("gmail", "v1", credentials=creds)
    return service


def get_recent_emails(service, max_results=5):
    result = service.users().messages().list(
        userId="me",
        labelIds=["INBOX"],
        maxResults=max_results
    ).execute()

    messages = result.get("messages", [])

    if not messages:
        print("没有读取到邮件")
        return

    for message in messages:
        email_data = service.users().messages().get(
            userId="me",
            id=message["id"],
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

        print("--------------")
        print("From:", info["From"])
        print("Subject:", info["Subject"])
        print("Date:", info["Date"])


def main():
    service = get_gmail_service()
    get_recent_emails(service, max_results=5)


if __name__ == "__main__":
    main()