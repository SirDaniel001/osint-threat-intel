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
INPUT_FILE = "../data/unified_threat_dataset.csv"
REPORT_FILE = "../data/day11_unified_report.pdf"
CHART_DIR = "../data/charts_day11"
LOGO_PATH = "../data/logo.png"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

os.makedirs(CHART_DIR, exist_ok=True)

# ----------------------------
# Generate Charts
# ----------------------------
def generate_charts(df):
    # Source Distribution
    plt.figure(figsize=(6, 4))
    df['source_type'].value_counts().plot(kind='bar', color=['blue', 'purple'])
    plt.title('Source Distribution (Surface vs Dark Web)')
    plt.xlabel('Source')
    plt.ylabel('Count')
    source_chart = os.path.join(CHART_DIR, "source_distribution.png")
    plt.tight_layout()
    plt.savefig(source_chart)
    plt.close()

    # IOC Tags Frequency
    all_tags = []
    df['IOC_tags'].dropna().apply(lambda x: all_tags.extend(x.split(',')))
    tags_series = pd.Series(all_tags).value_counts()
    plt.figure(figsize=(6, 4))
    tags_series.plot(kind='bar', color='green')
    plt.title('IOC Tags Frequency')
    plt.xlabel('Tag')
    plt.ylabel('Frequency')
    ioc_chart = os.path.join(CHART_DIR, "ioc_tags.png")
    plt.tight_layout()
    plt.savefig(ioc_chart)
    plt.close()

    # Risk Score Distribution
    if 'risk_score' in df.columns:
        plt.figure(figsize=(6, 4))
        df['risk_score'].fillna(0).plot(kind='hist', bins=10, color='orange', edgecolor='black')
        plt.title('Risk Score Distribution')
        plt.xlabel('Risk Score')
        plt.ylabel('Frequency')
        risk_chart = os.path.join(CHART_DIR, "risk_score.png")
        plt.tight_layout()
        plt.savefig(risk_chart)
        plt.close()
    else:
        risk_chart = None

    return source_chart, ioc_chart, risk_chart

# ----------------------------
# Generate PDF
# ----------------------------
def generate_pdf(total_records, unique_domains, surface_count, darkweb_count, high_risk_count, source_chart, ioc_chart, risk_chart):
    pdf = FPDF()
    pdf.add_page()

    # Add Logo
    if os.path.exists(LOGO_PATH):
        pdf.image(LOGO_PATH, x=80, y=10, w=50)
    pdf.ln(40)

    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Day 11 - Unified Threat Intelligence Report", ln=True, align='C')

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
    pdf.cell(70, 10, "Unique Domains", 1)
    pdf.cell(50, 10, str(unique_domains), 1, ln=True)
    pdf.cell(70, 10, "Surface Count", 1)
    pdf.cell(50, 10, str(surface_count), 1, ln=True)
    pdf.cell(70, 10, "Darkweb Count", 1)
    pdf.cell(50, 10, str(darkweb_count), 1, ln=True)
    pdf.cell(70, 10, "High-Risk Domains", 1)
    pdf.cell(50, 10, str(high_risk_count), 1, ln=True)

    # Add Charts
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Source Distribution", ln=True)
    pdf.image(source_chart, x=10, y=None, w=180)

    pdf.ln(80)
    pdf.cell(0, 10, "IOC Tags Frequency", ln=True)
    pdf.image(ioc_chart, x=10, y=None, w=180)

    if risk_chart:
        pdf.ln(80)
        pdf.cell(0, 10, "Risk Score Distribution", ln=True)
        pdf.image(risk_chart, x=10, y=None, w=180)

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
        print("[ERROR] Unified dataset file not found.")
        exit()

    df = pd.read_csv(INPUT_FILE)

    total_records = len(df)
    unique_domains = df['domain'].nunique()
    surface_count = len(df[df['source_type'] == 'surface'])
    darkweb_count = len(df[df['source_type'] == 'darkweb'])
    high_risk_count = len(df[df['risk_score'] > 50]) if 'risk_score' in df.columns else 0

    source_chart, ioc_chart, risk_chart = generate_charts(df)
    generate_pdf(total_records, unique_domains, surface_count, darkweb_count, high_risk_count, source_chart, ioc_chart, risk_chart)

    send_email(
        subject="Day 11 - Unified Threat Intelligence Report",
        body=f"Please find attached the Day 11 Threat Report.\nTotal Records: {total_records}\nUnique Domains: {unique_domains}\nHigh-Risk Domains: {high_risk_count}",
        attachment=REPORT_FILE
    )
