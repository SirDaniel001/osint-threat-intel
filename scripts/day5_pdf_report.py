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
# Load environment variables
# ----------------------------
load_dotenv()
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# ----------------------------
# Config
# ----------------------------
INPUT_FILE = "../data/cleaned_phishing_data.csv"
REPORT_FILE = "../data/day5_report.pdf"
CHART_DIR = "../data/charts"
LOGO_PATH = "../data/logo.png"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

os.makedirs(CHART_DIR, exist_ok=True)

# ----------------------------
# Generate Charts
# ----------------------------
def generate_charts(df):
    # TLD Distribution Chart
    tld_counts = df['tld'].value_counts()
    plt.figure(figsize=(6,4))
    tld_counts.plot(kind='bar', color='orange')
    plt.title('TLD Distribution')
    plt.xlabel('TLD')
    plt.ylabel('Count')
    tld_chart_path = os.path.join(CHART_DIR, "tld_distribution.png")
    plt.tight_layout()
    plt.savefig(tld_chart_path)
    plt.close()

    # Top 5 Domains Chart
    top_domains = df['domain'].value_counts().head(5)
    plt.figure(figsize=(6,4))
    top_domains.plot(kind='barh', color='teal')
    plt.title('Top 5 Domains')
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
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "OSINT Threat Intelligence - Day 5 Report", ln=True, align='C')
    
    # Date
    pdf.set_font("Arial", '', 12)
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.cell(200, 10, f"Generated on: {date_str}", ln=True, align='C')
    
    # Summary Table
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
    
    # Charts
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "TLD Distribution", ln=True)
    pdf.image(tld_chart, x=10, y=None, w=180)
    
    pdf.ln(80)
    pdf.cell(0, 10, "Top 5 Domains", ln=True)
    pdf.image(domains_chart, x=10, y=None, w=180)
    
    # Save PDF
    pdf.output(REPORT_FILE)
    print(f"[+] PDF Report Generated with Logo: {REPORT_FILE}")

# ----------------------------
# Send Email with PDF
# ----------------------------
def send_email_with_attachment(subject, body, attachment_path):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = subject
        
        # Body
        msg.attach(MIMEText(body, 'plain'))
        
        # Attachment
        if os.path.exists(attachment_path):
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment_path)}"')
                msg.attach(part)
        
        # Connect and send
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"[+] Email sent to {EMAIL_RECEIVER} with attachment {attachment_path}")
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
    
    # Kenyan URLs count
    kenyan_count = df[df['tld'] == 'ke'].shape[0]
    
    # Generate charts
    tld_chart, domains_chart = generate_charts(df)
    
    # Generate PDF
    generate_pdf(len(df), df['domain'].nunique(), kenyan_count, tld_chart, domains_chart)
    
    # Send Email
    send_email_with_attachment(
        subject="OSINT Threat Intelligence - Day 5 Report",
        body=f"Please find attached the Day 5 OSINT report.\n\nTotal Records: {len(df)}\nKenyan URLs: {kenyan_count}",
        attachment_path=REPORT_FILE
    )
