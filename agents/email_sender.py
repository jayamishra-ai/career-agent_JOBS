import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email(subject, body, receiver):

    print("Preparing email...")

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = receiver

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:

            server.starttls()

            print("Logging in...")

            server.login(EMAIL, PASSWORD)

            print("Sending email...")

            server.send_message(msg)

        print("✅ Email Sent Successfully")

    except Exception as e:
        print("❌ Email Error:", e)