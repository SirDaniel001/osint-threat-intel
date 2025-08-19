import sqlite3
import os
import random
from datetime import datetime, timedelta

# Path to your main threats database
DB_PATH = os.path.abspath('osint_threats.db')

# Remove old DB so we start fresh
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

# Connect and create table
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("""
CREATE TABLE threats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT,
    type TEXT,
    keyword TEXT,
    domain TEXT,
    date_detected TEXT
)
""")

# Sample data pools
sources = ["pastebin", "google", "darkweb", "phishtank", "twitter", "github", "telegram"]
types = ["phishing", "malware", "scam", "data leak", "ransomware", "fraud"]
keywords = [
    "cbk", "mpesa", "loan", "crypto", "bank", "password", "verify", "secure",
    "update", "account", "m-pesa", "central bank", "btc", "wallet"
]
domain_patterns = [
    "phish-{n}.com", "malware-{n}.net", "scam-{n}.org",
    "leak-{n}.io", "fraud-{n}.biz", "hack-{n}.xyz"
]

now = datetime.utcnow()
rows = []

# Generate 120 entries in the last 30 days
for _ in range(120):
    days_ago = random.randint(0, 29)
    date_str = (now - timedelta(days=days_ago)).strftime("%Y-%m-%d")
    src = random.choice(sources)
    typ = random.choice(types)
    kw = random.choice(keywords)
    dom = random.choice(domain_patterns).format(n=random.randint(1, 999))
    rows.append((src, typ, kw, dom, date_str))

# Insert all at once
c.executemany(
    "INSERT INTO threats (source, type, keyword, domain, date_detected) VALUES (?,?,?,?,?)",
    rows
)

conn.commit()
conn.close()
print(f"✅ Seeded {len(rows)} threats into {DB_PATH}")
