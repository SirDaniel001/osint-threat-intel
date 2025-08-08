import os
from fpdf import FPDF
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from dotenv import load_dotenv

# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# ----------------------------
# Paths
# ----------------------------
REPORT_FILE = "../data/day13_report.pdf"
LOGO_PATH = "../data/logo.png"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# ----------------------------
# PDF Generator
# ----------------------------
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Logo
    if os.path.exists(LOGO_PATH):
        pdf.image(LOGO_PATH, x=80, y=10, w=50)
        pdf.ln(40)

    # Header
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(200, 10, "Day 13 - Phishing Data Ingestion Report", ln=True, align='C')
    pdf.set_font("Helvetica", '', 12)
    pdf.cell(200, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
    pdf.ln(10)

    # Summary Table
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "Summary:", ln=True)
    pdf.set_font("Helvetica", '', 12)

    summary = [
        ("Database Path", "database/osint_threats.db"),
        ("Table Name", "threats"),
        ("New Records Inserted", "3"),
        ("Source Files", "sample_phishing_feed.csv"),
        ("Feed Sources", "OpenPhish, URLhaus, PhishTank"),
        ("Insertion Method", "CSV Reader -> SQLite"),
    ]

    for label, value in summary:
        pdf.cell(70, 10, label, 1)
        pdf.cell(120, 10, value, 1, ln=True)

    pdf.output(REPORT_FILE)
    print(f"[+] PDF Report Generated: {REPORT_FILE}")

# ----------------------------
# Email Sender
# ----------------------------
def send_email():
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = "Day 13 - OSINT Threat Intelligence Report"
        msg.attach(MIMEText("Attached is the Day 13 PDF Report.\n\nRegards,\nKaliGPT", 'plain'))

        if os.path.exists(REPORT_FILE):
            with open(REPORT_FILE, "rb") as file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(REPORT_FILE)}')
                msg.attach(part)

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        print(f"[+] Email sent to {EMAIL_RECEIVER}")
    except Exception as e:
        print(f"[-] Email sending failed: {e}")

# ----------------------------
# Run
# ----------------------------
if __name__ == "__main__":
    generate_pdf()
    send_email()
