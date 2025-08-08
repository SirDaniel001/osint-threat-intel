from fpdf import FPDF
from fpdf.enums import XPos, YPos
from datetime import datetime
import smtplib
from email.message import EmailMessage
import os

# === Email Configuration ===
EMAIL_SENDER = "danielmuteti590@gmail.com"
EMAIL_PASSWORD = "mmprpqvniofzfjvu"  # Gmail App Password
EMAIL_RECEIVER = "danielmuteti590@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# === File Output Path ===
PDF_OUTPUT = "../data/day15_report.pdf"

# === PDF Generation ===
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(200, 10, "Day 15 - Telegram Alert Bot Report", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    pdf.set_font("Helvetica", '', 12)
    pdf.cell(200, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    pdf.ln(5)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "Summary:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font("Helvetica", '', 12)
    summary = [
        "- Connected Telegram Bot (@PhishingAlertBot) to the threat intelligence database.",
        "- Developed 'telegram_alert.py' to monitor and send new threat alerts.",
        "- Successfully tested Telegram bot integration with SQLite.",
        "- Each alert includes: Source, Type, Indicator, Detection Date, and Confidence Score.",
        "- Verified live alerts delivered to Telegram app in real time.",
    ]
    for line in summary:
        pdf.cell(0, 10, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(5)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "Sample Telegram Alerts", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font("Helvetica", '', 11)
    messages = [
        "[ALERT] New Threat Detected!",
        "Source: OpenPhish",
        "Type: phishing",
        "Indicator: http://malicious-site1.com",
        "Detected: 2025-08-07 10:00:00",
        "Confidence: N/A",
        "",
        "[ALERT] New Threat Detected!",
        "Source: URLhaus",
        "Type: malware",
        "Indicator: http://badstuff.biz",
        "Detected: 2025-08-07 10:15:00",
        "Confidence: N/A",
        "",
        "[ALERT] New Threat Detected!",
        "Source: PhishTank",
        "Type: phishing",
        "Indicator: http://phishy-login.co",
        "Detected: 2025-08-07 11:00:00",
        "Confidence: N/A"
    ]
    for msg in messages:
        pdf.cell(0, 8, msg, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.output(PDF_OUTPUT)
    print(f"[+] PDF Report Generated: {PDF_OUTPUT}")
    return PDF_OUTPUT

# === Email Sending ===
def send_email(pdf_path):
    msg = EmailMessage()
    msg['Subject'] = 'Day 15 - Telegram Alert Bot Report'
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg.set_content('Attached is the Day 15 OSINT project report on Telegram alert bot integration.')

    with open(pdf_path, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=os.path.basename(pdf_path))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print(f"[+] Email sent to {EMAIL_RECEIVER}")

# === Main ===
if __name__ == "__main__":
    pdf_path = generate_pdf()
    send_email(pdf_path)
