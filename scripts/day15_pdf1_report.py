from fpdf import FPDF
from fpdf.enums import XPos, YPos
from datetime import datetime
import smtplib
from email.message import EmailMessage
import os

# Email Config
EMAIL_SENDER = "danielmuteti590@gmail.com"
EMAIL_PASSWORD = "mmprpqvniofzfjvu"
EMAIL_RECEIVER = "danielmuteti590@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

PDF_OUTPUT_PATH = "../data/day15_report.pdf"

class PDF(FPDF):
    def header(self):
        self.set_font("DejaVu", "B", 12)
        self.set_text_color(50, 50, 50)
        self.cell(0, 10, "OSINT Threat Intelligence - Daily Report", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "I", 8)
        self.set_text_color(128)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_pdf():
    pdf = PDF()
    pdf.add_page()

    # Use a Unicode-compatible font
    pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    pdf.add_font("DejaVu", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    pdf.add_font("DejaVu", "I", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf")
    pdf.set_font("DejaVu", "", 11)

    # Title
    pdf.set_font("DejaVu", "B", 14)
    pdf.cell(0, 10, "Day 15 - Telegram Alert Bot Report", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    # Date
    pdf.set_font("DejaVu", "", 12)
    pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    pdf.ln(10)
    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(0, 10, "Summary:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font("DejaVu", "", 11)
    summary = [
        "• Connected Telegram Bot (@PhishingAlertBot) to the threat intelligence database.",
        "• Developed 'telegram_alert.py' to monitor and send new threat alerts.",
        "• Successfully tested Telegram bot integration with SQLite.",
        "• Each alert includes: Source, Type, Indicator, Detection Date, and Confidence Score.",
        "• Verified live alerts delivered to Telegram app in real time."
    ]

    for item in summary:
        item = item.strip().replace('\n', ' ')
        if item:
            pdf.multi_cell(0, 8, item, new_x="LMARGIN", new_y="NEXT")

    pdf.ln(5)
    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(0, 10, "Sample Telegram Alerts", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font("DejaVu", "", 11)
    alerts = [
        "[ALERT] New Threat Detected!\nSource: OpenPhish\nType: phishing\nIndicator: http://malicious-site1.com\nDetected: 2025-08-07 10:00:00\nConfidence: N/A",
        "[ALERT] New Threat Detected!\nSource: URLhaus\nType: malware\nIndicator: http://badstuff.biz\nDetected: 2025-08-07 10:15:00\nConfidence: N/A",
        "[ALERT] New Threat Detected!\nSource: PhishTank\nType: phishing\nIndicator: http://phishy-login.co\nDetected: 2025-08-07 11:00:00\nConfidence: N/A"
    ]

    for alert in alerts:
        pdf.multi_cell(0, 8, alert, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

    # Save PDF
    os.makedirs(os.path.dirname(PDF_OUTPUT_PATH), exist_ok=True)
    pdf.output(PDF_OUTPUT_PATH)
    print(f"[+] PDF Report Generated: {PDF_OUTPUT_PATH}")
    return PDF_OUTPUT_PATH

def send_email(pdf_path):
    msg = EmailMessage()
    msg['Subject'] = "Day 15 - Telegram Alert Bot Report"
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg.set_content("Attached is the Day 15 PDF Report on Telegram Bot Integration with Threat Alerts.")

    with open(pdf_path, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=os.path.basename(pdf_path))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

    print(f"[+] Email sent to {EMAIL_RECEIVER}")

if __name__ == "__main__":
    print("[*] Generating PDF...")
    pdf_path = generate_pdf()
    print("[*] Sending Email...")
    send_email(pdf_path)
