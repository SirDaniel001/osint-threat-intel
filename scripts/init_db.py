import sqlite3

DB_PATH = "threats.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create threats table
cursor.execute("""
CREATE TABLE IF NOT EXISTS threats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain TEXT UNIQUE,
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()
print("[+] threats.db initialized with 'threats' table.")
