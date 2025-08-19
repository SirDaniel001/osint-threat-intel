import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from dotenv import load_dotenv

# Import PDF generator
from day24_pdf_report import generate_day24_report

# Load environment variables
load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

REPORT_PATH = "reports/day24_report.pdf"

def send_email_with_report():
    """Send the Day 24 PDF report via email with Gmail + App Password."""

    # Auto-generate PDF if missing
    if not os.path.exists(REPORT_PATH):
        print("⚠ Report missing, generating now...")
        generate_day24_report()

    # Double-check file exists
    if not os.path.exists(REPORT_PATH):
        raise FileNotFoundError(f"Report still not found: {REPORT_PATH}")

    # Build the email
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = "Day 24 Report — Bug Fixes & Performance Optimization"

    msg.attach(MIMEText("Attached is the Day 24 PDF report with performance improvements and bug fixes.", "plain"))

    # Attach PDF
    with open(REPORT_PATH, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(REPORT_PATH)}")
        msg.attach(part)

    # Send email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

    print(f"📧 Email sent successfully to {EMAIL_RECEIVER} with attachment {REPORT_PATH}")

if __name__ == "__main__":
    send_email_with_report()
