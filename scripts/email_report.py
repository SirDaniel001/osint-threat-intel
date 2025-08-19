import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("EMAIL_SENDER")
SMTP_PASS = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

REPORT_PATH = "reports/day24_report.pdf"


def send_email_with_report():
    """Send the Day 24 PDF report via email with Gmail + App Password."""
    if not os.path.exists(REPORT_PATH):
        raise FileNotFoundError(f"Report not found: {REPORT_PATH}")

    # Email setup
    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = "Day 24 Report — Bug Fixes & Performance Optimization"

    # Email body
    body = MIMEText("Hello,\n\nAttached is your Day 24 Threat Intel Report.\n\n✅ Completed in style!\n", "plain")
    msg.attach(body)

    # Attach PDF
    with open(REPORT_PATH, "rb") as f:
        pdf_attachment = MIMEApplication(f.read(), _subtype="pdf")
        pdf_attachment.add_header("Content-Disposition", "attachment", filename="day24_report.pdf")
        msg.attach(pdf_attachment)

    # Debug info (helps if login fails)
    print(f"SMTP_USER={SMTP_USER!r}")
    print(f"SMTP_PASS length={len(SMTP_PASS.strip())}")

    # Send email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(SMTP_USER, SMTP_PASS.strip())
        server.send_message(msg)

    print(f"📧 Email sent to {EMAIL_RECEIVER} with {REPORT_PATH} attached!")


if __name__ == "__main__":
    send_email_with_report()
