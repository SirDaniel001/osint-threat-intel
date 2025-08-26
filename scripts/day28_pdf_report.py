#!/usr/bin/env python3
"""
Day 28 – Final Project Report Generator + Email Sender
Final corrected version (aligned with your .env variables).
Author: SirDaniel
"""

import os
import smtplib
import sqlite3
from fpdf import FPDF, XPos, YPos
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from dotenv import load_dotenv
from pathlib import Path

# ---------- CONFIG ----------
# detect project root (parent of scripts/)
BASE_DIR = Path(__file__).resolve().parent.parent

# load .env from project root
load_dotenv(BASE_DIR / ".env")

DB_PATH = BASE_DIR / "database" / "osint_threats.db"
REPORT_PATH = BASE_DIR / "reports" / "day28_final_report.pdf"
ARCHITECTURE_IMG = BASE_DIR / "reports" / "day28_architecture.png"

# match your .env keys
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("EMAIL_SENDER")
SENDER_PASS = os.getenv("EMAIL_PASSWORD")
RECIPIENT_EMAIL = os.getenv("EMAIL_RECEIVER", "danielmuteti590@gmail.com")


# ---------- PDF GENERATOR ----------
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()

    # register fonts (regular + bold)
    pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    pdf.add_font("DejaVu", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")

    # title
    pdf.set_font("DejaVu", "", 16)
    pdf.cell(200, 10, "Day 28 Final Project Report",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    # body
    pdf.set_font("DejaVu", "", 12)
    pdf.ln(10)
    pdf.multi_cell(0, 10,
        "OSINT Threat Intelligence Platform\n\n"
        "✔ Project completed successfully on Day 28 (24/08/2025).\n"
        "✔ Features: phishing detection, dark web monitoring, WHOIS checks, alerts, dashboard, reports.\n"
        "✔ All diagrams, presentation slides, and documentation finalized.\n"
    )

    # add DB stats if DB exists
    if DB_PATH.exists():
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM threats;")
            threats_count = cur.fetchone()[0]
        except Exception:
            threats_count = 0

        try:
            cur.execute("SELECT COUNT(*) FROM alerts;")
            alerts_count = cur.fetchone()[0]
        except Exception:
            alerts_count = 0

        conn.close()

        pdf.ln(5)
        pdf.cell(0, 10, "Database Statistics:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(0, 10, f" - Total Threats: {threats_count}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(0, 10, f" - Total Alerts: {alerts_count}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # embed architecture diagram if exists
    if ARCHITECTURE_IMG.exists():
        pdf.ln(10)
        pdf.set_font("DejaVu", "B", 12)
        pdf.cell(0, 10, "System Architecture Diagram:",
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.image(str(ARCHITECTURE_IMG), w=170)

    pdf.ln(10)
    pdf.set_font("DejaVu", "", 10)
    pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.output(str(REPORT_PATH))
    print(f"[+] PDF report generated: {REPORT_PATH}")


# ---------- EMAIL SENDER ----------
def send_email():
    if not SENDER_EMAIL or not SENDER_PASS:
        print("[!] Skipping email: EMAIL_SENDER or EMAIL_PASSWORD not set in .env")
        return

    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECIPIENT_EMAIL
        msg["Subject"] = "Day 28 Final Project Report"

        body = (
            "Hello SirDaniel,\n\n"
            "Attached is your Day 28 Final Project Report PDF.\n\n"
            "✔ Completed & delivered!\n"
        )
        msg.attach(MIMEText(body, "plain"))

        with open(REPORT_PATH, "rb") as f:
            attach = MIMEApplication(f.read(), _subtype="pdf")
            attach.add_header("Content-Disposition", "attachment", filename=REPORT_PATH.name)
            msg.attach(attach)

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASS)
        server.send_message(msg)
        server.quit()

        print(f"[+] Email sent to {RECIPIENT_EMAIL}")

    except Exception as e:
        print(f"[!] Email sending failed: {e}")


# ---------- MAIN ----------
if __name__ == "__main__":
    generate_pdf()
    send_email()
