import os
import time
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup
from stem import Signal
from stem.control import Controller
from datetime import datetime
from fpdf import FPDF
import matplotlib.pyplot as plt
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import smtplib
from dotenv import load_dotenv

# ----------------------------
# Config
# ----------------------------
DATA_DIR = "../data"
LOGO_PATH = os.path.join(DATA_DIR, "logo.png")
ONION_LIST = os.path.join(DATA_DIR, "onion_sites.txt")
OUTPUT_CSV = os.path.join(DATA_DIR, "darkweb_analysis.csv")
PDF_REPORT = os.path.join(DATA_DIR, "day9_darkweb_report.pdf")
CHART_DIR = os.path.join(DATA_DIR, "charts")
os.makedirs(CHART_DIR, exist_ok=True)

# Keywords for detection
KEYWORDS = ["cbk", "mpesa", ".ke", "bank", "login", "password", "account", "kcb", "equity", "safaricom", "crypto", "wallet", "paypal"]

# Tor proxy
PROXIES = {"http": "socks5h://127.0.0.1:9050", "https": "socks5h://127.0.0.1:9050"}

# Email config
load_dotenv()
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# ----------------------------
# Tor Identity Rotation
# ----------------------------
def renew_identity():
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
            time.sleep(3)
            print("[INFO] Rotated Tor identity.")
    except Exception as e:
        print(f"[ERROR] Tor identity rotation failed: {e}")

# ----------------------------
# Crawl Function
# ----------------------------
def crawl_sites():
    if not os.path.exists(ONION_LIST):
        print(f"[ERROR] {ONION_LIST} not found.")
        return []

    with open(ONION_LIST, "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    results = []
    for idx, url in enumerate(urls, start=1):
        print(f"[INFO] Crawling ({idx}/{len(urls)}): {url}")
        try:
            response = requests.get(url, proxies=PROXIES, timeout=30)
            if response.status_code == 200:
                text = BeautifulSoup(response.text, "html.parser").get_text().lower()
                found = [kw for kw in KEYWORDS if kw in text]
                score = len(found) * 50
                results.append({
                    "url": url,
                    "status": "200",
                    "keywords_found": ",".join(found) if found else "None",
                    "threat_score": score,
                    "crawled_at": datetime.now()
                })
            else:
                results.append({"url": url, "status": str(response.status_code), "keywords_found": "None", "threat_score": 0, "crawled_at": datetime.now()})
        except Exception as e:
            print(f"[ERROR] Could not fetch {url}: {e}")
            results.append({"url": url, "status": "error", "keywords_found": "None", "threat_score": 0, "crawled_at": datetime.now()})

        # Rotate IP after every 2 sites
        if idx % 2 == 0:
            renew_identity()

        time.sleep(random.randint(5, 10))  # Random delay
    return results

# ----------------------------
# Generate Charts
# ----------------------------
def generate_charts(df):
    # Threat score distribution
    plt.figure(figsize=(6, 4))
    df['threat_score'].plot(kind='hist', bins=5, color='red')
    plt.title('Threat Score Distribution')
    plt.xlabel('Threat Score')
    plt.ylabel('Frequency')
    threat_chart = os.path.join(CHART_DIR, "threat_score.png")
    plt.tight_layout()
    plt.savefig(threat_chart)
    plt.close()

    # Keyword frequency
    keyword_counts = {}
    for kws in df['keywords_found']:
        if kws != "None":
            for kw in kws.split(","):
                keyword_counts[kw] = keyword_counts.get(kw, 0) + 1
    if keyword_counts:
        plt.figure(figsize=(6, 4))
        pd.Series(keyword_counts).sort_values(ascending=False).plot(kind='bar', color='blue')
        plt.title('Keyword Frequency')
        plt.ylabel('Count')
        keyword_chart = os.path.join(CHART_DIR, "keyword_freq.png")
        plt.tight_layout()
        plt.savefig(keyword_chart)
        plt.close()
    else:
        keyword_chart = None

    return threat_chart, keyword_chart

# ----------------------------
# Generate PDF Report
# ----------------------------
def generate_pdf(total_sites, high_risk, threat_chart, keyword_chart):
    pdf = FPDF()
    pdf.add_page()

    # Add Logo
    if os.path.exists(LOGO_PATH):
        pdf.image(LOGO_PATH, x=80, y=10, w=50)
    pdf.ln(40)

    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Dark Web Analysis Report - Day 9", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')

    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Summary", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(60, 10, "Total Sites", 1)
    pdf.cell(60, 10, str(total_sites), 1, ln=True)
    pdf.cell(60, 10, "High-Risk Sites", 1)
    pdf.cell(60, 10, str(high_risk), 1, ln=True)

    pdf.ln(10)
    if threat_chart:
        pdf.cell(0, 10, "Threat Score Distribution", ln=True)
        pdf.image(threat_chart, x=10, y=None, w=180)
    if keyword_chart:
        pdf.ln(80)
        pdf.cell(0, 10, "Keyword Frequency", ln=True)
        pdf.image(keyword_chart, x=10, y=None, w=180)

    pdf.output(PDF_REPORT)
    print(f"[+] PDF Report Generated: {PDF_REPORT}")

# ----------------------------
# Email Function
# ----------------------------
def send_email(attachment):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = "Dark Web Analysis - Day 9 Report"

        msg.attach(MIMEText("Please find attached the Day 9 Dark Web Analysis Report."))

        with open(attachment, "rb") as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment)}"')
            msg.attach(part)

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"[+] Email sent to {EMAIL_RECEIVER}")
    except Exception as e:
        print(f"[-] Email sending failed: {e}")

# ----------------------------
# Main Execution
# ----------------------------
if __name__ == "__main__":
    data = crawl_sites()
    df = pd.DataFrame(data)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"[+] Analysis saved to {OUTPUT_CSV}")

    high_risk = df[df['threat_score'] > 0].shape[0]
    threat_chart, keyword_chart = generate_charts(df)
    generate_pdf(len(df), high_risk, threat_chart, keyword_chart)
    send_email(PDF_REPORT)
