#!/usr/bin/env python3
# 📄 Day 18 PDF OSINT Threat Report Generator + Email Automation + Local AI Cover + Transparent Flowchart Overlay + Modern Title

import os
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
from fpdf import FPDF, XPos, YPos
import matplotlib.pyplot as plt
from matplotlib import rcParams
from PIL import Image
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# === LOAD ENV VARIABLES ===
load_dotenv()
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# === PATHS ===
DB_PATH = os.path.expanduser("~/osint-threat-intel/osint_threats.db")
REPORTS_DIR = os.path.expanduser("~/osint-threat-intel/reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

REPORT_FILE = os.path.join(REPORTS_DIR, f"day18_threat_report_{datetime.now().strftime('%Y%m%d')}.pdf")
COVER_IMAGE = os.path.join(REPORTS_DIR, "day18_ai_image.png")
FLOWCHART_IMAGE = os.path.join(REPORTS_DIR, "day18_flowchart.png")
FLOWCHART_TRANSPARENT = os.path.join(REPORTS_DIR, "day18_flowchart_transparent.png")

# === MAKE FLOWCHART TRANSPARENT ===
def make_flowchart_transparent(input_path, output_path, alpha=150):
    if not os.path.exists(input_path):
        print(f"[WARN] Flowchart image not found: {input_path}")
        return
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()
    new_data = []
    for item in datas:
        if item[3] > 0:
            new_data.append((item[0], item[1], item[2], alpha))
        else:
            new_data.append(item)
    img.putdata(new_data)
    img.save(output_path)
    print(f"[INFO] Transparent flowchart saved: {output_path}")

# === PDF CLASS ===
class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, 'OSINT Daily Threat Intelligence Report', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.set_font('Helvetica', '', 10)
        self.cell(0, 10, datetime.now().strftime('%Y-%m-%d %H:%M'), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.ln(5)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')

# === FETCH DATA FROM DB ===
def fetch_data():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM threats")
    total_threats = cur.fetchone()[0] or 0
    cur.execute("SELECT source, COUNT(*) FROM threats GROUP BY source ORDER BY COUNT(*) DESC LIMIT 5")
    top_sources = cur.fetchall()
    cur.execute("SELECT type, COUNT(*) FROM threats GROUP BY type ORDER BY COUNT(*) DESC LIMIT 5")
    top_types = cur.fetchall()
    cur.execute("SELECT date_detected, COUNT(*) FROM threats GROUP BY date_detected ORDER BY date_detected")
    threats_by_date = cur.fetchall()
    cur.execute("SELECT id, source, type, keyword, domain, date_detected FROM threats ORDER BY date_detected DESC LIMIT 10")
    recent_threats = cur.fetchall()
    conn.close()
    return total_threats, top_sources, top_types, threats_by_date, recent_threats

# === GENERATE CHARTS ===
def generate_charts(top_sources, top_types, threats_by_date):
    rcParams.update({'figure.autolayout': True})

    if top_sources:
        labels, counts = zip(*top_sources)
        plt.figure(figsize=(4, 4))
        plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title("Top Threat Sources")
        plt.savefig(os.path.join(REPORTS_DIR, "top_sources.png"))
        plt.close()

    if top_types:
        labels, counts = zip(*top_types)
        plt.figure(figsize=(4, 4))
        plt.bar(labels, counts, color='red')
        plt.title("Top Threat Types")
        plt.savefig(os.path.join(REPORTS_DIR, "top_types.png"))
        plt.close()

    if threats_by_date:
        dates, counts = zip(*threats_by_date)
        plt.figure(figsize=(5, 3))
        plt.plot(dates, counts, marker='o', color='green')
        plt.title("Threats Over Time")
        plt.xticks(rotation=45)
        plt.savefig(os.path.join(REPORTS_DIR, "threats_timeline.png"))
        plt.close()

# === BUILD PDF ===
def build_pdf(total, sources, types, dates, recent):
    pdf = PDF()

    # COVER PAGE
    pdf.add_page()
    if os.path.exists(COVER_IMAGE):
        pdf.image(COVER_IMAGE, x=0, y=0, w=210, h=297)
    if os.path.exists(FLOWCHART_TRANSPARENT):
        pdf.image(FLOWCHART_TRANSPARENT, x=120, y=200, w=80)

    # Simulated semi-transparent background (light gray)
    pdf.set_fill_color(30, 30, 30)  # dark background
    pdf.rect(10, 250, 190, 15, style='F')

    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", 'B', 20)
    pdf.set_xy(10, 253)
    pdf.cell(190, 10, "Day 18 OSINT Threat Intelligence Report", align='C')

    # CONTENT PAGE
    pdf.set_text_color(0, 0, 0)
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, f"Total Threats: {total}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Top Sources
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 8, "Top Sources", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", '', 10)
    for src, cnt in sources:
        pdf.cell(0, 6, f"{src}: {cnt}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    if os.path.exists(os.path.join(REPORTS_DIR, "top_sources.png")):
        pdf.image(os.path.join(REPORTS_DIR, "top_sources.png"), w=80)
    pdf.ln(5)

    # Top Types
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 8, "Top Types", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", '', 10)
    for typ, cnt in types:
        pdf.cell(0, 6, f"{typ}: {cnt}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    if os.path.exists(os.path.join(REPORTS_DIR, "top_types.png")):
        pdf.image(os.path.join(REPORTS_DIR, "top_types.png"), w=80)
    pdf.ln(5)

    # Threats Over Time
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 8, "Threats Over Time", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    if os.path.exists(os.path.join(REPORTS_DIR, "threats_timeline.png")):
        pdf.image(os.path.join(REPORTS_DIR, "threats_timeline.png"), w=120)
    pdf.ln(5)

    # Flowchart (full size)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 8, "Automation Flowchart", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    if os.path.exists(FLOWCHART_IMAGE):
        pdf.image(FLOWCHART_IMAGE, w=160)
    pdf.ln(5)

    # Recent Threats
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 8, "Recent Threats", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", '', 9)
    for row in recent:
        pdf.cell(0, 6, f"ID:{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.output(REPORT_FILE)
    print(f"[{datetime.now()}] 📄 PDF report generated: {REPORT_FILE}")

# === EMAIL PDF ===
def email_pdf():
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = "Day 18 OSINT PDF Threat Report"
    with open(REPORT_FILE, "rb") as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(REPORT_FILE)}"')
        msg.attach(part)
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
    print(f"[{datetime.now()}] 📧 PDF emailed to {EMAIL_RECEIVER}")

# === MAIN EXECUTION ===
if __name__ == "__main__":
    make_flowchart_transparent(FLOWCHART_IMAGE, FLOWCHART_TRANSPARENT, alpha=150)
    total, top_sources, top_types, threats_by_date, recent_threats = fetch_data()
    generate_charts(top_sources, top_types, threats_by_date)
    build_pdf(total, top_sources, top_types, threats_by_date, recent_threats)
    email_pdf()
