#!/usr/bin/env python3
import os
import smtplib
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from dotenv import load_dotenv

# === CONFIG ===
LOG_FILE = "../logs/alert_log.txt"
PDF_PATH = "../reports/day16_telegram_loop_report.pdf"
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
FONT_REGULAR = os.path.join(FONT_DIR, "DejaVuSans.ttf")
FONT_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

# === Email Settings ===
load_dotenv()
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")   # Loaded from .env
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))


# === PDF Class ===
class PDF(FPDF):
    def header(self):
        self.set_font("DejaVu", "B", 16)
        self.cell(0, 10, "Day 16 – Continuous Telegram Alert Loop",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.set_font("DejaVu", "", 12)
        self.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.ln(5)


def generate_pdf():
    pdf = PDF()

    # Try loading custom fonts, fallback to Arial if missing
    try:
        pdf.add_font("DejaVu", "", FONT_REGULAR)
        pdf.add_font("DejaVu", "B", FONT_BOLD)
    except Exception as e:
        print(f"[!] Font load failed, using default font: {e}")
        pdf.set_font("Arial", "", 12)

    pdf.set_font("DejaVu", "", 11)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # === Summary Section ===
    pdf.set_font("DejaVu", "B", 13)
    pdf.cell(0, 10, "Summary of Tasks",
              new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("DejaVu", "", 10)

    summary_points = [
        "Developed 'auto_alert_loop.py' for 24/7 continuous threat monitoring.",
        "Telegram bot integrated for live push alerts.",
        "alerts_sent table used to avoid alert duplication.",
        "Every alert logged to logs/alert_log.txt for tracking.",
        "Confirmed delivery of real-time alerts to Telegram.",
        "Alert fields include: Source, Type, Indicator, Description, Date, Confidence.",
    ]

    # usable width instead of 0
    usable_width = pdf.w - 2 * pdf.l_margin

    for point in summary_points:
        safe_text = f"- {point}"
        try:
            pdf.multi_cell(usable_width, 8, safe_text, align="L")
        except Exception:
            pdf.cell(usable_width, 8, safe_text[:80],
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # === Sample Alerts ===
    pdf.ln(4)
    pdf.set_font("DejaVu", "B", 13)
    pdf.cell(0, 10, "Sample Logged Alerts",
              new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("DejaVu", "", 10)

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()[-10:]
            for line in lines:
                safe_line = line.strip()
                try:
                    pdf.multi_cell(usable_width, 7, safe_line, align="L")
                except Exception:
                    pdf.cell(usable_width, 7, safe_line[:80],
                             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    else:
        pdf.set_text_color(255, 0, 0)
        pdf.cell(usable_width, 8, "[!] No alert_log.txt found!",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_text_color(0, 0, 0)

    os.makedirs(os.path.dirname(PDF_PATH), exist_ok=True)
    pdf.output(PDF_PATH)
    print(f"[+] PDF Report Generated: {PDF_PATH}")
    return PDF_PATH


def send_email(pdf_file):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = "Day 16 - Telegram Auto Alert Loop Report"

    body = MIMEText("Attached is the PDF report for Day 16 – Continuous Alert Loop.\n\nRegards,\nOSINT Threat Intel System", "plain")
    msg.attach(body)

    with open(pdf_file, "rb") as f:
        part = MIMEApplication(f.read(), Name=os.path.basename(pdf_file))
        part["Content-Disposition"] = f'attachment; filename="{os.path.basename(pdf_file)}"'
        msg.attach(part)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        print(f"[📧] PDF emailed successfully to {EMAIL_RECEIVER}")


# === MAIN ===
if __name__ == "__main__":
    print("[*] Generating Day 16 PDF Report...")
    pdf_file = generate_pdf()
    print("[*] Sending Report via Email...")
    send_email(pdf_file)
