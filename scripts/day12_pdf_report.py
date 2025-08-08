import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from dotenv import load_dotenv

# ----------------------------
# Load .env variables
# ----------------------------
load_dotenv()
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# ----------------------------
# Config
# ----------------------------
CHART_DIR = "../data/charts_day12"
REPORT_FILE = "../data/day12_report.pdf"
LOGO_PATH = "../data/logo.png"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

os.makedirs(CHART_DIR, exist_ok=True)

# ----------------------------
# Generate Chart
# ----------------------------
def generate_source_chart():
    plt.figure(figsize=(6, 4))
    plt.bar(["Twitter"], [1], color='blue')
    plt.title("Insert Records Per Source")
    plt.xlabel("Source")
    plt.ylabel("Records")
    chart_path = os.path.join(CHART_DIR, "source_chart.png")
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()
    return chart_path

# ----------------------------
# Generate PDF
# ----------------------------
def generate_pdf(chart_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Add logo
    if os.path.exists(LOGO_PATH):
        pdf.image(LOGO_PATH, x=80, y=10, w=50)
        pdf.ln(40)

    # Title
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(200, 10, "Day 12 - OSINT Database Integration Report", ln=True, align='C')

    # Timestamp
    pdf.set_font("Helvetica", '', 12)
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.cell(200, 10, f"Generated on: {date_str}", ln=True, align='C')
    pdf.ln(10)

    # Summary Table
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "Summary:", ln=True)

    pdf.set_font("Helvetica", '', 12)
    summary = [
        ("Database Path", "database/osint_threats.db"),
        ("Table Name", "threats"),
        ("Records Inserted", "1"),
        ("Insert Verified", "Yes"),
    ]

    for label, value in summary:
        pdf.cell(70, 10, label, 1)
        pdf.cell(70, 10, value, 1, ln=True)

    # Chart
    pdf.ln(10)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "Insert Records Per Source", ln=True)
    pdf.image(chart_path, x=10, y=pdf.get_y() + 5, w=180)

    pdf.output(REPORT_FILE)
    print(f"[+] PDF Report Generated: {REPORT_FILE}")

# ----------------------------
# Send Email
# ----------------------------
def send_email():
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = "Day 12 - OSINT Database Integration Report"

        msg.attach(MIMEText("Attached is your Day 12 PDF Report.", 'plain'))

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
        print(f"[-] Email failed: {e}")

# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    chart_path = generate_source_chart()
    generate_pdf(chart_path)
    send_email()
