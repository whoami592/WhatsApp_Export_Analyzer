import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime


PATTERNS = [
    re.compile(r"^\[?(\d{1,2}/\d{1,2}/\d{2,4}),?\s+(\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM|am|pm)?)\]?\s+-?\s*([^:]+):\s?(.*)$"),
    re.compile(r"^\[?(\d{1,2}[-.]\d{1,2}[-.]\d{2,4}),?\s+(\d{1,2}:\d{2}(?::\d{2})?)\]?\s+-?\s*([^:]+):\s?(.*)$"),
]


@dataclass
class Message:
    date: str
    time: str
    sender: str
    text: str


def parse_export(text):
    messages = []
    for raw in text.replace("\ufeff", "").splitlines():
        match = next((p.match(raw) for p in PATTERNS if p.match(raw)), None)
        if match:
            messages.append(Message(*(part.strip() for part in match.groups())))
        elif messages and raw.strip():
            messages[-1].text += "\n" + raw.strip()
    return messages


def statistics(messages):
    senders = Counter(m.sender for m in messages)
    words = Counter()
    for message in messages:
        words.update(re.findall(r"[A-Za-z0-9_']{3,}", message.text.lower()))
    return {
        "messages": len(messages),
        "participants": len(senders),
        "senders": senders,
        "top_words": words.most_common(15),
    }
