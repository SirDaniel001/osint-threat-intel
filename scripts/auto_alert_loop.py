import os
import time
import sqlite3
import requests
from datetime import datetime

# Telegram credentials (hardcoded for now, optional: move to .env later)
TELEGRAM_TOKEN = "8006180164:AAGPz7wImUHlBeB1_8ARM_I9bMBmkMVcynA"
CHAT_ID = "7044331741"

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), "../database/osint_threats.db")

# Initialize last alert time
last_alert_time = None

def fetch_new_threats():
    global last_alert_time
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if last_alert_time:
        query = "SELECT * FROM threats WHERE datetime(date_detected) > datetime(?) ORDER BY date_detected ASC"
        cursor.execute(query, (last_alert_time,))
    else:
        query = "SELECT * FROM threats ORDER BY date_detected ASC"
        cursor.execute(query)

    threats = cursor.fetchall()
    conn.close()

    if threats:
        last_alert_time = threats[-1][5]  # Update to latest 'date_detected'

    return threats

def send_telegram_alert(threat):
    id, source, threat_type, indicator, description, date_detected, confidence, _ = threat

    message = f"""
🚨 New Threat Detected!

Source: {source}
Type: {threat_type}
Indicator: {indicator}
Description: {description or '-'}
Detected: {date_detected}
Confidence: {confidence or 'N/A'}
"""

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message.strip()
    }

    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print(f"[+] Alert sent for threat ID {id}")
        else:
            print(f"[!] Failed to send alert: {response.text}")
    except Exception as e:
        print(f"[!] Error while sending alert: {e}")

def monitor_loop(interval=300):
    print(f"[*] Starting continuous threat monitoring every {interval} seconds...")
    while True:
        threats = fetch_new_threats()
        if threats:
            for threat in threats:
                send_telegram_alert(threat)
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] No new threats detected.")
        time.sleep(interval)

if __name__ == "__main__":
    monitor_loop()
