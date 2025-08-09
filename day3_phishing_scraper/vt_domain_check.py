import requests
import pandas as pd
import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ===== CONFIG =====
API_KEY = "79cadb54bd584f9d3cc26b2c5ad69a6e7ead38d3ebf80ee25fc22ff4faa282a0"

# Telegram
TELEGRAM_TOKEN = "8006180164:AAGPz7wImUHlBeB1_8ARM_I9bMBmkMVcynA"
CHAT_ID = "7044331741"

# Email
EMAIL_SENDER = "danielmuteti590@gmail.com"
EMAIL_PASSWORD = "mmprpqvniofzfjvu"  # Gmail App Password
EMAIL_RECEIVER = "danielmuteti590@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# File paths
input_file = "output/clean_phishing_domains.csv"
output_file = "output/domain_reputation.csv"
BASE_URL = "https://www.virustotal.com/api/v3/domains/"
HEADERS = {"x-apikey": API_KEY}

# ===== ALERTING =====
def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message}
        r = requests.post(url, data=payload)
        if r.status_code == 200:
            print(f"[+] Telegram alert sent.")
        else:
            print(f"[!] Telegram failed: {r.status_code}")
    except Exception as e:
        print(f"[!] Telegram send error: {e}")

def send_email_alert(subject, message):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        print(f"[+] Email alert sent.")
    except Exception as e:
        print(f"[!] Email send error: {e}")

# ===== MAIN LOGIC =====
if not os.path.exists(input_file):
    print(f"[!] Input file {input_file} not found.")
    exit()

df = pd.read_csv(input_file)
domains = df['Domain'].dropna().unique().tolist()
results = []

print("[+] Starting VirusTotal checks with Telegram + Email alerts...")
for domain in domains:
    url = BASE_URL + domain
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
            malicious = stats.get("malicious", 0)
            suspicious = stats.get("suspicious", 0)
            status = "Malicious" if malicious > 0 else "Suspicious" if suspicious > 0 else "Clean"

            results.append({
                "Domain": domain,
                "Malicious": malicious,
                "Suspicious": suspicious,
                "Status": status
            })

            print(f"[+] {domain} => {status}")

            if status != "Clean":
                alert_msg = f"⚠ ALERT: {domain} flagged as {status}\nMalicious: {malicious}, Suspicious: {suspicious}"
                send_telegram_message(alert_msg)
                send_email_alert("Phishing Alert!", alert_msg)

        else:
            print(f"[!] VT error {response.status_code} for {domain}")
        time.sleep(15)  # API rate limit
    except Exception as e:
        print(f"[!] Error checking {domain}: {e}")

# Save to CSV
pd.DataFrame(results).to_csv(output_file, index=False)
print(f"[+] Results saved to {output_file}")
