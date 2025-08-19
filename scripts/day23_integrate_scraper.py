import sqlite3
import pandas as pd
from datetime import datetime
import os

# Paths
DB_PATH = os.path.join(os.path.dirname(__file__), "../database/osint_threats.db")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "../day3_phishing_scraper/output/clean_phishing_domains.csv")

def integrate_scraper_results():
    if not os.path.exists(OUTPUT_PATH):
        print(f"[!] No cleaned domains found at {OUTPUT_PATH}")
        return

    # Load clean phishing domains
    df = pd.read_csv(OUTPUT_PATH)

    if df.empty:
        print("[*] No new domains in clean_phishing_domains.csv")
        return

    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    inserted = 0
    for domain in df['Domain'].unique():
        # Check if already exists in DB
        cursor.execute("SELECT id FROM threats WHERE indicator = ?", (domain,))
        if cursor.fetchone():
            continue  # Skip duplicates

        # Insert as a new phishing threat
        cursor.execute("""
            INSERT INTO threats (source, threat_type, indicator, description, date_detected, confidence)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "scraper",             # source
            "phishing",            # type
            domain,                # indicator
            "Domain detected by Day3 scraper", # description
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Medium"               # default confidence
        ))
        inserted += 1

    conn.commit()
    conn.close()

    print(f"[+] Inserted {inserted} new phishing domains into threats DB.")

if __name__ == "__main__":
    integrate_scraper_results()
