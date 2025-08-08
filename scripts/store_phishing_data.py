import sqlite3
import csv
from datetime import datetime

# Paths
CSV_FILE = "../data/sample_phishing_feed.csv"
DB_FILE = "../database/osint_threats.db"

# Connect to the database
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Read the CSV and insert each row
with open(CSV_FILE, 'r') as file:
    reader = csv.DictReader(file)
    rows_inserted = 0

    for row in reader:
        cursor.execute("""
            INSERT INTO threats (source, threat_type, indicator, date_detected)
            VALUES (?, ?, ?, ?)
        """, (
            row['source'],
            row['threat_type'],
            row['indicator'],
            row['date_detected']
        ))
        rows_inserted += 1

# Commit and close
conn.commit()
conn.close()

print(f"[+] Inserted {rows_inserted} phishing records into the database.")
