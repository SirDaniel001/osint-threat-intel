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
INPUT_FILE = "../data/darkweb_analysis.csv"
REPORT_FILE = "../data/day8_report.pdf"
CHART_DIR = "../data/charts"
LOGO_PATH = "../data/logo.png"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

os.makedirs(CHART_DIR, exist_ok=True)

# ----------------------------
# Generate Charts
# ----------------------------
def generate_charts(df):
    # Threat Score Distribution
    plt.figure(figsize=(6,4))
    df['threat_score'].hist(bins=10, color='darkred')
    plt.title('Threat Score Distribution')
    plt.xlabel('Threat Score')
    plt.ylabel('Frequency')
    threat_chart_path = os.path.join(CHART_DIR, "threat_distribution.png")
    plt.tight_layout()
    plt.savefig(threat_chart_path)
    plt.close()

    # Keyword Frequency Chart
    keyword_series = df['keywords_found'].dropna()
    keywords_list = []
    for keywords in keyword_series:
        if keywords != "None":
            keywords_list.extend(keywords.split(","))
    keyword_freq = pd.Series(keywords_list).value_counts()

    if not keyword_freq.empty:
        plt.figure(figsize=(6,4))
        keyword_freq.head(10).plot(kind='bar', color='navy')
        plt.title('Top Keywords Found')
        plt.xlabel('Keywords')
        plt.ylabel('Frequency')
        keywords_chart_path = os.path.join(CHART_DIR, "keyword_frequency.png")
        plt.tight_layout()
        plt.savefig(keywords_chart_path)
        plt.close()
    else:
        keywords_chart_path = None
    
    return threat_chart_path, keywords_chart_path

# ----------------------------
# Generate PDF Report
# ----------------------------
def generate_pdf(total_sites, reachable_sites, avg_score, threat_chart, keywords_chart):
    pdf = FPDF()
    pdf.add_page()

    # Add Logo
    if os.path.exists(LOGO_PATH):
        pdf.image(LOGO_PATH, x=80, y=10, w=50)
    pdf.ln(40)

    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "OSINT Threat Intelligence - Day 8 Report", ln=True, align='C')

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
    pdf.cell(60, 10, "Total Sites", 1)
    pdf.cell(60, 10, str(total_sites), 1, ln=True)
    pdf.cell(60, 10, "Reachable Sites", 1)
    pdf.cell(60, 10, str(reachable_sites), 1, ln=True)
    pdf.cell(60, 10, "Avg Threat Score", 1)
    pdf.cell(60, 10, str(avg_score), 1, ln=True)

    # Charts
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Threat Score Distribution", ln=True)
    pdf.image(threat_chart, x=10, y=None, w=180)

    if keywords_chart:
        pdf.ln(80)
        pdf.cell(0, 10, "Keyword Frequency", ln=True)
        pdf.image(keywords_chart, x=10, y=None, w=180)

    # Save PDF
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

        # Send email
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
        print("[ERROR] Dark web analysis data file not found.")
        exit()

    df = pd.read_csv(INPUT_FILE)
    total_sites = len(df)
    reachable_sites = df[df['status'] == 200].shape[0]
    avg_score = round(df['threat_score'].mean(), 2)

    threat_chart, keywords_chart = generate_charts(df)
    generate_pdf(total_sites, reachable_sites, avg_score, threat_chart, keywords_chart)

    send_email_with_attachment(
        subject="OSINT Threat Intelligence - Day 8 Report",
        body=f"Please find attached the Day 8 report.\n\nTotal Sites: {total_sites}\nReachable: {reachable_sites}\nAvg Threat Score: {avg_score}",
        attachment_path=REPORT_FILE
    )
