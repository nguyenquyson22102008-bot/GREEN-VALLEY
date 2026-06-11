import os

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))


def _mail_accounts_from_env():
    accounts = []
    raw_accounts = os.getenv("MAIL_ACCOUNTS", "")

    for raw_account in raw_accounts.split(";"):
        if not raw_account.strip() or ":" not in raw_account:
            continue
        email, password = raw_account.split(":", 1)
        if email.strip() and password.strip():
            accounts.append({"email": email.strip(), "password": password.strip()})

    sender_email = os.getenv("SENDER_EMAIL", "").strip()
    sender_password = os.getenv("SENDER_PASSWORD", "").strip()
    if sender_email and sender_password:
        accounts.append({"email": sender_email, "password": sender_password})

    return accounts


MAIL_ACCOUNTS = _mail_accounts_from_env()
