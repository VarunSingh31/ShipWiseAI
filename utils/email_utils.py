import os
import smtplib
import datetime
from email.message import EmailMessage

EMAIL_HISTORY_FILE = "email_history_log.csv"

def send_plaintext_email(subject, body, recipient_email):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.getenv("SENDER_EMAIL")
    msg['To'] = recipient_email
    msg.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASSWORD"))
        smtp.send_message(msg)

    log_email_history(subject, recipient_email)

def log_email_history(subject, recipient_email):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"{timestamp},{recipient_email},{subject}\n"
    with open(EMAIL_HISTORY_FILE, "a") as f:
        f.write(entry)
