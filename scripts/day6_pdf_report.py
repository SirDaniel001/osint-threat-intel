import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import os
from datetime import datetime
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
INPUT_FILE = "../data/cleaned_phishing_data.csv"
OUTPUT_FILE = "../data/day6_report.pdf"
CHART_DIR = "../data/charts"
LOGO_PATH = "../data/logo.png"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

os.makedirs(CHART_DIR, exist_ok=True)

# ----------------------------
# Generate Charts
# ----------------------------
def generate_charts(df):
    tld_counts = df['tld'].value_counts().head(15)
    plt.figure(figsize=(6,4))
    tld_counts.plot(kind='bar', color='orange')
    plt.title('TLD Distribution (Top 15)')
    plt.xlabel('TLD')
    plt.ylabel('Count')
    tld_chart_path = os.path.join(CHART_DIR, "tld_distribution.png")
    plt.tight_layout()
    plt.savefig(tld_chart_path)
    plt.close()

    top_domains = df['domain'].value_counts().head(10)
    plt.figure(figsize=(6,4))
    top_domains.plot(kind='barh', color='teal')
    plt.title('Top 10 Domains')
    plt.xlabel('Count')
    plt.ylabel('Domain')
    domains_chart_path = os.path.join(CHART_DIR, "top_domains.png")
    plt.tight_layout()
    plt.savefig(domains_chart_path)
    plt.close()

    return tld_chart_path, domains_chart_path

# ----------------------------
# Generate PDF Report
# ----------------------------
def generate_pdf(total_records, unique_domains, kenyan_count, tld_chart, domains_chart):
    pdf = FPDF()
    pdf.add_page()

    # Add Logo
    if os.path.exists(LOGO_PATH):
        pdf.image(LOGO_PATH, x=80, y=10, w=50)
    pdf.ln(40)

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "OSINT Threat Intelligence - Day 6 Report", ln=True, align='C')

    pdf.set_font("Arial", '', 12)
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.cell(200, 10, f"Generated on: {date_str}", ln=True, align='C')

    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Summary:", ln=True)

    pdf.set_font("Arial", '', 12)
    pdf.cell(60, 10, "Metric", 1)
    pdf.cell(60, 10, "Value", 1, ln=True)
    pdf.cell(60, 10, "Total Records", 1)
    pdf.cell(60, 10, str(total_records), 1, ln=True)
    pdf.cell(60, 10, "Unique Domains", 1)
    pdf.cell(60, 10, str(unique_domains), 1, ln=True)
    pdf.cell(60, 10, "Kenyan URLs", 1)
    pdf.cell(60, 10, str(kenyan_count), 1, ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "TLD Distribution", ln=True)
    pdf.image(tld_chart, x=10, y=None, w=180)

    pdf.ln(80)
    pdf.cell(0, 10, "Top 10 Domains", ln=True)
    pdf.image(domains_chart, x=10, y=None, w=180)

    pdf.output(OUTPUT_FILE)
    print(f"[+] PDF Report Generated: {OUTPUT_FILE}")

# ----------------------------
# Send Email with Attachment
# ----------------------------
def send_email(subject, body, attachment_path):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        if os.path.exists(attachment_path):
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment_path)}"')
                msg.attach(part)

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        print(f"[+] Email sent to {EMAIL_RECEIVER} with attachment: {attachment_path}")
    except Exception as e:
        print(f"[-] Email sending failed: {e}")

# ----------------------------
# Main Execution
# ----------------------------
if __name__ == "__main__":
    if not os.path.exists(INPUT_FILE):
        print("[ERROR] Cleaned data file not found.")
        exit()

    df = pd.read_csv(INPUT_FILE)
    kenyan_count = df[df['tld'] == 'ke'].shape[0]

    tld_chart, domains_chart = generate_charts(df)
    generate_pdf(len(df), df['domain'].nunique(), kenyan_count, tld_chart, domains_chart)

    send_email(
        subject="OSINT Threat Intelligence - Day 6 Report",
        body=f"Please find attached the Day 6 OSINT report.\n\nTotal Records: {len(df)}\nKenyan URLs: {kenyan_count}",
        attachment_path=OUTPUT_FILE
    )
