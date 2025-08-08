import os
import smtplib
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fpdf import FPDF
from fpdf.enums import XPos, YPos

# === CONFIG ===
LOG_FILE = "../logs/alert_log.txt"
PDF_PATH = "../reports/day16_telegram_loop_report.pdf"
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
FONT_REGULAR = os.path.join(FONT_DIR, "DejaVuSans.ttf")
FONT_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

# === Email Settings ===
EMAIL_SENDER = "danielmuteti590@gmail.com"
EMAIL_PASSWORD = "mmprpqvniofzfjvu"
EMAIL_RECEIVER = "danielmuteti590@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# === PDF Class ===
class PDF(FPDF):
    def header(self):
        self.set_font("DejaVu", "B", 16)
        self.cell(0, 10, "Day 16 – Continuous Telegram Alert Loop", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.set_font("DejaVu", "", 12)
        self.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.ln(5)

def generate_pdf():
    pdf = PDF()
    pdf.add_font("DejaVu", "", FONT_REGULAR)
    pdf.add_font("DejaVu", "B", FONT_BOLD)

    pdf.set_font("DejaVu", "", 11)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # === Summary Section ===
    pdf.set_font("DejaVu", "B", 13)
    pdf.cell(0, 10, "Summary of Tasks", ln=True)
    pdf.set_font("DejaVu", "", 10)

    summary_points = [
        "Developed 'auto_alert_loop.py' for 24/7 continuous threat monitoring.",
        "Telegram bot integrated for live push alerts.",
        "alerts_sent table used to avoid alert duplication.",
        "Every alert logged to logs/alert_log.txt for tracking.",
        "Confirmed delivery of real-time alerts to Telegram.",
        "Alert fields include: Source, Type, Indicator, Description, Date, Confidence.",
    ]

    for point in summary_points:
        try:
            pdf.multi_cell(0, 8, f"- {point}")
        except Exception as e:
            pdf.cell(0, 8, "[!] Could not render this line.")

    # === Sample Alerts
    pdf.ln(4)
    pdf.set_font("DejaVu", "B", 13)
    pdf.cell(0, 10, "Sample Logged Alerts", ln=True)
    pdf.set_font("DejaVu", "", 10)

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()[-10:]
            for line in lines:
                try:
                    pdf.multi_cell(0, 7, line.strip())
                except:
                    pdf.cell(0, 7, "[!] Error rendering this log entry.")
    else:
        pdf.set_text_color(255, 0, 0)
        pdf.cell(0, 8, "[!] No alert_log.txt found!", ln=True)
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
