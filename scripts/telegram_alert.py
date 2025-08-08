import requests
import sqlite3
from datetime import datetime
import os

# --- Configuration ---

# Telegram
TELEGRAM_TOKEN = "8006180164:AAGPz7wImUHlBeB1_8ARM_I9bMBmkMVcynA"
CHAT_ID = "7044331741"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

# Email (not used here, just for reference)
EMAIL_SENDER = "danielmuteti590@gmail.com"
EMAIL_PASSWORD = "mmprpqvniofzfjvu"
EMAIL_RECEIVER = "danielmuteti590@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Paths
DB_PATH = os.path.join(os.path.dirname(__file__), "../database/osint_threats.db")
LOG_FILE = os.path.join(os.path.dirname(__file__), "../logs/alert_log.txt")


# --- Core Functions ---

def send_telegram_alert(threat):
    message = f"""
🚨 *New Threat Detected!*

*Source:* {threat['source']}
*Type:* {threat['threat_type']}
*Indicator:* {threat['indicator']}
*Description:* {threat['description'] or "-"}
*Detected:* {threat['date_detected']}
*Confidence:* {threat['confidence'] or "N/A"}
    """

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    response = requests.post(TELEGRAM_API_URL, json=payload)

    if response.status_code == 200:
        print(f"[+] Telegram alert sent for threat ID {threat['id']}")
        return True
    else:
        print(f"[!] Failed to send alert: {response.text}")
        return False


def check_new_threats():
    print("[*] Checking for new threats...")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create alerts_sent table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts_sent (
            threat_id INTEGER PRIMARY KEY,
            sent_at TEXT
        );
    """)

    # Get IDs of threats already alerted
    cursor.execute("SELECT threat_id FROM alerts_sent;")
    sent_ids = {row[0] for row in cursor.fetchall()}

    # Get all threats
    cursor.execute("SELECT * FROM threats;")
    rows = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]

    # Ensure logs dir exists
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    for row in rows:
        threat = dict(zip(columns, row))
        if threat["id"] in sent_ids:
            continue  # Skip already alerted

        success = send_telegram_alert(threat)

        if success:
            # Log in alerts_sent
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO alerts_sent (threat_id, sent_at) VALUES (?, ?);",
                (threat["id"], now)
            )

            # Log to file
            with open(LOG_FILE, "a") as log_file:
                log_entry = f"[{now}] ALERT SENT - {threat['source']} | {threat['threat_type']} | {threat['indicator']}\n"
                log_file.write(log_entry)

    conn.commit()
    conn.close()


# --- Entry Point ---

if __name__ == "__main__":
    check_new_threats()
