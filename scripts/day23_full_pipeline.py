import subprocess
import sqlite3
import pandas as pd
import requests

DB_PATH = "threats.db"
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

def run_cmd(cmd):
    print(f"[Day23] Running {cmd} ...")
    subprocess.run(cmd, shell=True, check=True)

def get_all_domains():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT domain, first_seen FROM threats ORDER BY first_seen DESC LIMIT 20",
        conn
    )
    conn.close()
    return df

def get_new_domains():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT domain, first_seen FROM threats WHERE date(first_seen) = date('now')",
        conn
    )
    conn.close()
    return df

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

def send_daily_report():
    all_domains = get_all_domains()
    new_domains = get_new_domains()

    message = "🛡️ Daily Threat Report (Day 23)\n\n"
    message += f"⚠️ New domains today: {len(new_domains)}\n"
    message += f"📋 Total recent (last 20): {len(all_domains)}\n\n"

    if not all_domains.empty:
        message += "Recent Threats:\n"
        for _, row in all_domains.iterrows():
            message += f"• {row['domain']} (since {row['first_seen']})\n"
    else:
        message += "No threats recorded in DB yet."

    send_telegram_message(message)
    print("[Day23] ✅ Daily report sent.")

if __name__ == "__main__":
    print("[Day23] 🚀 Starting full pipeline...")

    # Step 1: Run scrapers
    run_cmd("python day3_phishing_scraper/phishing_scraper.py")

    # Step 2: Extract clean domains
    run_cmd("python day3_phishing_scraper/domain_extractor.py")

    # Step 3: Insert into DB
    run_cmd("python scripts/day23_integrate_scraper.py")

    # Step 4: Instant alerts (new domains only)
    run_cmd("python scripts/telegram_alert.py")

    # Step 5: Daily report (summary of new + recent)
    print("[Day23] Sending daily Telegram report ...")
    send_daily_report()

    print("[Day23] 🎯 Pipeline complete.")
