import sqlite3
import os
import random
from datetime import datetime, timedelta

DB_PATH = os.path.abspath('osint_threats.db')

# Remove old DB if exists
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Create table
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

sources = ["pastebin", "google", "darkweb", "phishtank", "twitter"]
types = ["phishing", "malware", "scam", "data leak"]
keywords = ["cbk", "mpesa", "loan", "crypto", "bank", "password", "verify", "secure"]
domains = ["phish-{n}.com", "malware-{n}.net", "scam-{n}.org", "leak-{n}.io"]

now = datetime.utcnow()

# Generate 60 random threats in past 30 days
rows = []
for i in range(60):
    days_ago = random.randint(0, 29)
    date_str = (now - timedelta(days=days_ago)).strftime("%Y-%m-%d")
    src = random.choice(sources)
    typ = random.choice(types)
    kw = random.choice(keywords)
    dom = random.choice(domains).format(n=random.randint(1, 100))
    rows.append((src, typ, kw, dom, date_str))

c.executemany("INSERT INTO threats (source, type, keyword, domain, date_detected) VALUES (?,?,?,?,?)", rows)

conn.commit()
conn.close()

print(f"Seeded {len(rows)} threats into {DB_PATH}")
