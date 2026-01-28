import re

REDACTED = "[REDACTED_PII]"

def redact_pii(text: str) -> str:
    # Email regex
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    # Phone regex: matches (555) 123-4567, 555-123-4567, 5551234567, +1 555 123 4567, etc.
    phone_pattern = r"(\+?\d{1,2}[\s-]?)?(\(\d{3}\)|\d{3})[\s-]?\d{3}[\s-]?\d{4}"
    # Redact emails
    text = re.sub(email_pattern, REDACTED, text)
    # Redact phone numbers
    text = re.sub(phone_pattern, REDACTED, text)
    return text
