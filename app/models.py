from dataclasses import dataclass


@dataclass
class Email:
    id: str
    sender: str
    subject: str
    date: str
    snippet: str
    received_at: str = ""