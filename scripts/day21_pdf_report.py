#!/usr/bin/env python3
import sqlite3
import os
from datetime import datetime, date, timedelta, timezone
from fpdf import FPDF, XPos, YPos
import matplotlib.pyplot as plt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

# ========= CONFIG =========
DB_PATH = os.path.abspath("../osint_threats.db")
EMAIL_SENDER = "danielmuteti590@gmail.com"
EMAIL_PASSWORD = "mmprpqvniofzfjvu"  # Gmail App Password
EMAIL_RECEIVER = "danielmuteti590@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
# ==========================

def fetch_data():
    since_date = (date.today() - timedelta(days=13)).isoformat()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM threats WHERE type LIKE '%phishing%' AND date_detected >= ?", (since_date,))
    phishing_count = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM threats WHERE source LIKE '%darkweb%' AND date_detected >= ?", (since_date,))
    darkweb_hits = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM threats WHERE type LIKE '%whois%' AND date_detected >= ?", (since_date,))
    whois_suspicious = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT date_detected, COUNT(*) 
        FROM threats 
        WHERE date_detected >= ? 
        GROUP BY date_detected
        ORDER BY date_detected
    """, (since_date,))
    trend_data = cursor.fetchall()

    cursor.execute("""
        SELECT domain, source, date_detected
        FROM threats
        WHERE date_detected >= ?
        ORDER BY date_detected DESC
        LIMIT 10
    """, (since_date,))
    recent = cursor.fetchall()

    conn.close()
    return phishing_count, darkweb_hits, whois_suspicious, trend_data, recent

def generate_chart(trend_data):
    dates = [row[0] for row in trend_data]
    counts = [row[1] for row in trend_data]

    plt.figure(figsize=(6, 3))
    plt.plot(dates, counts, marker="o", color="blue")
    plt.title("Threat Trends (Last 14 Days)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    chart_path = "trend_chart.png"
    plt.savefig(chart_path)
    plt.close()
    return chart_path

def generate_pdf(phishing_count, darkweb_hits, whois_suspicious, chart_path, recent):
    pdf = FPDF()
    pdf.add_page()

    # ✅ Unicode font loading
    pdf.add_font("DejaVu", "", FONT_PATH)
    pdf.set_font("DejaVu", "", 16)

    pdf.cell(0, 10, "Financial Threat Intelligence Report", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    pdf.set_font("DejaVu", "", 10)
    pdf.cell(0, 10, f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 10, f"Period: {(date.today()-timedelta(days=13)).isoformat()} to {date.today().isoformat()}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(5)
    pdf.set_font("DejaVu", "", 12)
    pdf.cell(0, 10, "Key Metrics (Last 14 Days)", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("DejaVu", "", 10)
    pdf.cell(0, 8, f"Phishing Domains: {phishing_count}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 8, f"Dark Web Hits: {darkweb_hits}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 8, f"WHOIS Flags: {whois_suspicious}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(5)
    pdf.image(chart_path, w=150)

    pdf.ln(10)
    pdf.set_font("DejaVu", "", 12)
    pdf.cell(0, 10, "Recent High-Signal Findings", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("DejaVu", "", 9)

    # ✅ Fix multi_cell by giving explicit width instead of 0
    for idx, (domain, source, date_found) in enumerate(recent, 1):
        safe_text = f"{idx}. {domain} - {source} - {date_found}"
        pdf.multi_cell(190, 5, safe_text)  # force width to 190mm

    pdf_path = "day21_threat_report.pdf"
    pdf.output(pdf_path)
    return pdf_path

def send_email(attachment_path):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = "Day 21 OSINT Threat Report"

    msg.attach(MIMEText("Please find attached the Day 21 Threat Intelligence Report.", "plain"))

    with open(attachment_path, "rb") as f:
        part = MIMEApplication(f.read(), Name=os.path.basename(attachment_path))
        part["Content-Disposition"] = f'attachment; filename="{os.path.basename(attachment_path)}"'
        msg.attach(part)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

    print(f"[+] Email sent to {EMAIL_RECEIVER} with attachment {attachment_path}")

if __name__ == "__main__":
    phishing_count, darkweb_hits, whois_suspicious, trend, recent = fetch_data()
    chart_path = generate_chart(trend)
    pdf_path = generate_pdf(phishing_count, darkweb_hits, whois_suspicious, chart_path, recent)
    send_email(pdf_path)
