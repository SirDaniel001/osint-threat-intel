import requests
import sqlite3
from datetime import datetime
import os
from dotenv import load_dotenv

# --- Load .env ---
load_dotenv()

# --- Configuration ---

# Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

# Email (optional, used by report scripts)
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

# Paths
DB_PATH = os.path.join(os.path.dirname(__file__), "../database/osint_threats.db")
LOG_FILE = os.path.join(os.path.dirname(__file__), "../logs/alert_log.txt")

# --- Core Functions ---

def send_telegram_alert(threat):
    message = f"""
🚨 <b>New Threat Detected!</b>

<b>Source:</b> {threat['source']}
<b>Type:</b> {threat['threat_type']}
<b>Indicator:</b> {threat['indicator']}
<b>Description:</b> {threat['description'] or "-"}
<b>Detected:</b> {threat['date_detected']}
<b>Confidence:</b> {threat['confidence'] or "N/A"}
    """

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"   # switched to HTML for safe formatting
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

    # Ensure alerts_sent table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts_sent (
            threat_id INTEGER PRIMARY KEY,
            sent_at TEXT
        );
    """)

    # Get IDs of already alerted threats
    cursor.execute("SELECT threat_id FROM alerts_sent;")
    sent_ids = {row[0] for row in cursor.fetchall()}

    # Get all threats
    cursor.execute("SELECT * FROM threats;")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    # Ensure logs directory exists
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    for row in rows:
        threat = dict(zip(columns, row))
        if threat["id"] in sent_ids:
            continue  # skip already alerted

        success = send_telegram_alert(threat)

        if success:
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

