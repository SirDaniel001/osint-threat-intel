#!/bin/bash
# 📊 Daily OSINT Threat Report & Secure Gmail Email Automation (with attachment)

# === CONFIGURATION ===
DB_PATH="$HOME/osint-threat-intel/osint_threats.db"
REPORT_PATH="$HOME/osint-threat-intel/reports/daily_report.txt"
CREDS_FILE="$HOME/osint-threat-intel/secure/email_creds.enc"
SMTP_SERVER="smtp.gmail.com"
SMTP_PORT=587
PASSPHRASE="Daniel@001"  # ⚠️ Keep this safe

# Ensure folders exist
mkdir -p "$(dirname "$REPORT_PATH")"
mkdir -p "$(dirname "$CREDS_FILE")"

# === ONE-TIME ENCRYPTION SETUP ===
if [ ! -f "$CREDS_FILE" ]; then
    echo "danielmuteti590@gmail.com|mmprpqvniofzfjvu" | \
    openssl enc -aes-256-cbc -pbkdf2 -salt -out "$CREDS_FILE" -pass pass:"$PASSPHRASE"
    echo "[SETUP] Credentials encrypted and saved to $CREDS_FILE"
fi

# === GENERATE REPORT ===
{
echo "=== 📅 DAILY OSINT THREAT REPORT ==="
date
echo

echo "=== TOTAL THREATS ==="
sqlite3 "$DB_PATH" "SELECT COUNT(*) AS total_threats FROM threats;"
echo

echo "=== TOP 5 SOURCES ==="
sqlite3 -header -column "$DB_PATH" "SELECT source, COUNT(*) AS count FROM threats GROUP BY source ORDER BY count DESC LIMIT 5;"
echo

echo "=== TOP 5 TYPES ==="
sqlite3 -header -column "$DB_PATH" "SELECT type, COUNT(*) AS count FROM threats GROUP BY type ORDER BY count DESC LIMIT 5;"
echo

echo "=== RECENT 10 THREATS ==="
sqlite3 -header -column "$DB_PATH" "SELECT id, source, type, keyword, domain, date_detected FROM threats ORDER BY date_detected DESC LIMIT 10;"
} > "$REPORT_PATH"

# === DECRYPT CREDENTIALS ===
DECRYPTED_CREDS=$(openssl enc -aes-256-cbc -d -pbkdf2 -in "$CREDS_FILE" -pass pass:"$PASSPHRASE")
EMAIL_SENDER=$(echo "$DECRYPTED_CREDS" | cut -d'|' -f1)
EMAIL_PASSWORD=$(echo "$DECRYPTED_CREDS" | cut -d'|' -f2)
EMAIL_RECEIVER="$EMAIL_SENDER"

# === SEND EMAIL VIA Python (smtplib) WITH ATTACHMENT ===
python3 <<EOF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

sender = "$EMAIL_SENDER"
password = "$EMAIL_PASSWORD"
receiver = "$EMAIL_RECEIVER"
report_path = "$REPORT_PATH"

msg = MIMEMultipart()
msg["Subject"] = "Daily OSINT Threat Report"
msg["From"] = sender
msg["To"] = receiver

# Email body
body_text = "Attached is the daily OSINT Threat Report.\n\nRegards,\nYour OSINT Automation System"
msg.attach(MIMEText(body_text, "plain"))

# Attachment
with open(report_path, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(report_path)}")
    msg.attach(part)

# Send email
try:
    with smtplib.SMTP("$SMTP_SERVER", $SMTP_PORT) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, [receiver], msg.as_string())
    print(f"[{__import__('datetime').datetime.now()}] ✅ Daily report generated and emailed to {receiver} with attachment")
except Exception as e:
    print(f"[ERROR] Failed to send email: {e}")
EOF
