import pandas as pd
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
# Load Environment Variables
# ----------------------------
load_dotenv()
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# ----------------------------
# Config
# ----------------------------
INPUT_FILE = "../data/whois_enriched.csv"
REPORT_FILE = "../data/day10_whois_report.pdf"
CHART_DIR = "../data/charts_day10"
LOGO_PATH = "../data/logo.png"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

os.makedirs(CHART_DIR, exist_ok=True)

# ----------------------------
# Generate Charts
# ----------------------------
def generate_charts(df):
    # WHOIS Status Chart
    status_counts = df['whois_status'].value_counts()
    plt.figure(figsize=(6, 4))
    status_counts.plot(kind='bar', color=['green', 'orange', 'red'])
    plt.title('WHOIS Status Distribution')
    plt.xlabel('Status')
    plt.ylabel('Count')
    whois_chart = os.path.join(CHART_DIR, "whois_status.png")
    plt.tight_layout()
    plt.savefig(whois_chart)
    plt.close()

    # Risk Score Distribution
    plt.figure(figsize=(6, 4))
    df['risk_score'].plot(kind='hist', bins=5, color='blue', edgecolor='black')
    plt.title('Risk Score Distribution')
    plt.xlabel('Risk Score')
    plt.ylabel('Frequency')
    score_chart = os.path.join(CHART_DIR, "risk_score.png")
    plt.tight_layout()
    plt.savefig(score_chart)
    plt.close()

    return whois_chart, score_chart

# ----------------------------
# Generate PDF
# ----------------------------
def generate_pdf(total_records, high_risk_count, whois_chart, score_chart):
    pdf = FPDF()
    pdf.add_page()

    # Add Logo if available
    if os.path.exists(LOGO_PATH):
        pdf.image(LOGO_PATH, x=80, y=10, w=50)
    pdf.ln(40)

    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Day 10 - WHOIS Enrichment Report", ln=True, align='C')

    # Date
    pdf.set_font("Arial", '', 12)
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.cell(200, 10, f"Generated on: {date_str}", ln=True, align='C')

    # Summary Table
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Summary:", ln=True)

    pdf.set_font("Arial", '', 12)
    pdf.cell(70, 10, "Metric", 1)
    pdf.cell(50, 10, "Value", 1, ln=True)
    pdf.cell(70, 10, "Total Records", 1)
    pdf.cell(50, 10, str(total_records), 1, ln=True)
    pdf.cell(70, 10, "High-Risk Domains", 1)
    pdf.cell(50, 10, str(high_risk_count), 1, ln=True)

    # Add Charts
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "WHOIS Status Distribution", ln=True)
    pdf.image(whois_chart, x=10, y=None, w=180)

    pdf.ln(80)
    pdf.cell(0, 10, "Risk Score Distribution", ln=True)
    pdf.image(score_chart, x=10, y=None, w=180)

    pdf.output(REPORT_FILE)
    print(f"[+] PDF Report Generated: {REPORT_FILE}")

# ----------------------------
# Send Email
# ----------------------------
def send_email(subject, body, attachment):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        if os.path.exists(attachment):
            with open(attachment, "rb") as file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment)}')
                msg.attach(part)

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"[+] Email sent to {EMAIL_RECEIVER} with attachment {attachment}")
    except Exception as e:
        print(f"[-] Email sending failed: {e}")

# ----------------------------
# Main Execution
# ----------------------------
if __name__ == "__main__":
    if not os.path.exists(INPUT_FILE):
        print("[ERROR] WHOIS enriched data file not found.")
        exit()

    df = pd.read_csv(INPUT_FILE)

    total_records = len(df)
    high_risk_count = df[df['risk_score'] > 0].shape[0]

    whois_chart, score_chart = generate_charts(df)
    generate_pdf(total_records, high_risk_count, whois_chart, score_chart)

    send_email(
        subject="Day 10 - WHOIS Enrichment Report",
        body=f"Please find attached the Day 10 WHOIS report.\nTotal Records: {total_records}\nHigh-Risk Domains: {high_risk_count}",
        attachment=REPORT_FILE
    )
