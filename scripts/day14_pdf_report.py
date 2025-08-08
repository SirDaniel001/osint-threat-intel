import pandas as pd
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from datetime import datetime
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# Config
CSV_FILE = "../results/search_results_day14.csv"
PDF_FILE = "../data/day14_report.pdf"
LOGO_PATH = "../data/logo.png"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Generate PDF
def generate_pdf(df):
    pdf = FPDF()
    pdf.add_page()

    if os.path.exists(LOGO_PATH):
        pdf.image(LOGO_PATH, x=80, y=10, w=50)
    pdf.set_font("Helvetica", 'B', 16)
    pdf.ln(40)
    pdf.cell(200, 10, "Day 14 - Threat Search & Export Report", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.set_font("Helvetica", '', 12)
    pdf.cell(200, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    # Normalize columns to lowercase
    df.columns = df.columns.str.strip().str.lower()

    # Summary
    pdf.ln(10)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "Summary:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", '', 12)

    total = len(df)
    unique_sources = df['source'].nunique() if 'source' in df.columns else 0
    unique_threats = df['threat type'].nunique() if 'threat type' in df.columns else 0
    unique_iocs = df['indicator'].nunique() if 'indicator' in df.columns else 0

    rows = [
        ("Total Records", total),
        ("Unique Sources", unique_sources),
        ("Threat Types", unique_threats),
        ("Unique IOCs", unique_iocs),
    ]

    for label, value in rows:
        pdf.cell(60, 10, str(label), 1)
        pdf.cell(40, 10, str(value), 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Preview Data
    pdf.ln(10)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "Sample Records (Top 5):", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", '', 9)

    headers = df.columns.tolist()
    for header in headers:
        pdf.cell(40, 8, header[:15], 1)
    pdf.ln()

    for _, row in df.head(5).iterrows():
        for value in row:
            pdf.cell(40, 8, str(value)[:15], 1)
        pdf.ln()

    pdf.output(PDF_FILE)
    print(f"[+] PDF Report Generated: {PDF_FILE}")
    return PDF_FILE

# Send Email
def send_email(attachment_path):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = "Day 14 - OSINT Threat Search Report"

    msg.attach(MIMEText("Attached is the Day 14 report summarizing threat search and export actions.", 'plain'))

    with open(attachment_path, "rb") as file:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
        msg.attach(part)

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()
    print(f"[+] Email sent to {EMAIL_RECEIVER}")

# Main
if __name__ == "__main__":
    if not os.path.exists(CSV_FILE):
        print(f"[-] Missing file: {CSV_FILE}")
        exit(1)

    df = pd.read_csv(CSV_FILE)
    pdf_path = generate_pdf(df)
    send_email(pdf_path)
