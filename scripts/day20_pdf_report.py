#!/usr/bin/env python3
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# -------------------------
# Load environment variables
# -------------------------
load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

SMTP_USER = os.getenv("SMTP_USER") or os.getenv("EMAIL_SENDER")
SMTP_PASS = os.getenv("SMTP_PASS") or os.getenv("EMAIL_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM") or os.getenv("EMAIL_SENDER")
EMAIL_TO = os.getenv("EMAIL_TO") or os.getenv("EMAIL_RECEIVER")

if not all([SMTP_USER, SMTP_PASS, EMAIL_FROM, EMAIL_TO]):
    raise ValueError("❌ Missing email credentials in .env")

# -------------------------
# Database config
# -------------------------
DB_PATH = Path(__file__).resolve().parents[1] / "osint_threats.db"

# -------------------------
# PDF Report Class
# -------------------------
class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, "OSINT Threat Intelligence Report", ln=True, align="C")
        self.ln(5)
        self.set_font('Helvetica', '', 12)
        self.set_text_color(80, 80, 80)
        self.cell(0, 10, f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}", ln=True, align="C")
        self.ln(10)

    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, title, ln=True)
        self.ln(4)

    def chapter_body(self, body, color=(0, 0, 0)):
        self.set_font('Helvetica', '', 12)
        self.set_text_color(*color)
        self.multi_cell(0, 8, body)
        self.ln()

# -------------------------
# Fetch Data
# -------------------------
def fetch_data():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM threats")
    total = c.fetchone()[0]

    c.execute("SELECT source, COUNT(*) FROM threats GROUP BY source ORDER BY COUNT(*) DESC LIMIT 5")
    top_sources = c.fetchall()

    c.execute("SELECT type, COUNT(*) FROM threats GROUP BY type ORDER BY COUNT(*) DESC LIMIT 5")
    top_types = c.fetchall()

    c.execute("SELECT id, source, type, keyword, domain, date_detected FROM threats ORDER BY date_detected DESC LIMIT 10")
    recent = c.fetchall()

    conn.close()
    return total, top_sources, top_types, recent

# -------------------------
# Create PDF
# -------------------------
def create_pdf(filepath):
    total, top_sources, top_types, recent = fetch_data()
    pdf = PDF()
    pdf.add_page()

    pdf.chapter_title("Summary")
    pdf.chapter_body(f"Total Threats: {total}", color=(220, 50, 50))

    pdf.chapter_title("Top Sources")
    for src, count in top_sources:
        pdf.chapter_body(f"{src} - {count}", color=(0, 102, 204))

    pdf.chapter_title("Top Types")
    for typ, count in top_types:
        pdf.chapter_body(f"{typ} - {count}", color=(0, 153, 76))

    pdf.chapter_title("Recent Threats")
    for tid, src, typ, kw, dom, date in recent:
        pdf.chapter_body(
            f"ID: {tid} | Source: {src} | Type: {typ} | Keyword: {kw} | Domain: {dom} | Date: {date}",
            color=(102, 0, 204)
        )

    pdf.output(filepath)
    print(f"✅ PDF report generated: {filepath}")

# -------------------------
# Email Sending
# -------------------------
def send_email(filepath):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg['Subject'] = f"Day 20 OSINT Threat Report - {datetime.now(timezone.utc).strftime('%Y-%m-%d')}"

    with open(filepath, "rb") as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{Path(filepath).name}"')
    msg.attach(part)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())

    print("📧 Email sent successfully.")

# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    report_path = Path(__file__).parent / "day20_report.pdf"
    create_pdf(report_path)
    send_email(report_path)
