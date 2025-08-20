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
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

# ----------------------------
# Config
# ----------------------------
INPUT_FILE = "../data/darkweb_data.csv"
REPORT_FILE = "../data/day7_darkweb_report.pdf"
CHART_DIR = "../data/charts"
LOGO_PATH = "../data/logo.png"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

os.makedirs(CHART_DIR, exist_ok=True)

# ----------------------------
# Generate Charts
# ----------------------------
def generate_charts(df):
    # Status Code Distribution Chart
    status_counts = df['status'].value_counts()
    plt.figure(figsize=(6,4))
    status_counts.plot(kind='bar', color='purple')
    plt.title('Dark Web Response Status Distribution')
    plt.xlabel('Status')
    plt.ylabel('Count')
    status_chart_path = os.path.join(CHART_DIR, "darkweb_status_distribution.png")
    plt.tight_layout()
    plt.savefig(status_chart_path)
    plt.close()
    
    return status_chart_path

# ----------------------------
# Generate PDF Report
# ----------------------------
def generate_pdf(total_sites, success_count, error_count, status_chart):
    pdf = FPDF()
    pdf.add_page()
    
    # Add Logo
    if os.path.exists(LOGO_PATH):
        pdf.image(LOGO_PATH, x=80, y=10, w=50)
    pdf.ln(40)
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "OSINT Threat Intelligence - Day 7 Dark Web Report", ln=True, align='C')
    
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
    pdf.cell(70, 10, "Value", 1, ln=True)
    pdf.cell(70, 10, "Total Onion Sites", 1)
    pdf.cell(70, 10, str(total_sites), 1, ln=True)
    pdf.cell(70, 10, "Successful Responses", 1)
    pdf.cell(70, 10, str(success_count), 1, ln=True)
    pdf.cell(70, 10, "Failed Responses", 1)
    pdf.cell(70, 10, str(error_count), 1, ln=True)
    
    # Chart
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Status Code Distribution", ln=True)
    pdf.image(status_chart, x=10, y=None, w=180)
    
    pdf.output(REPORT_FILE)
    print(f"[+] PDF Report Generated: {REPORT_FILE}")

# ----------------------------
# Send Email with PDF
# ----------------------------
def send_email_with_attachment(subject, body, attachment_path):
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
        print("[ERROR] Dark web data file not found.")
        exit()
    
    df = pd.read_csv(INPUT_FILE)
    
    total_sites = len(df)
    success_count = df[df['status'] != 'ERROR'].shape[0]
    error_count = df[df['status'] == 'ERROR'].shape[0]
    
    # Generate chart
    status_chart = generate_charts(df)
    
    # Generate PDF
    generate_pdf(total_sites, success_count, error_count, status_chart)
    
    # Send Email
    send_email_with_attachment(
        subject="OSINT Project - Day 7 Dark Web Report",
        body=f"Attached is the Day 7 Dark Web report.\nTotal Sites: {total_sites}\nSuccess: {success_count}\nErrors: {error_count}",
        attachment_path=REPORT_FILE
    )
