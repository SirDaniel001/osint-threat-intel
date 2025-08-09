import sqlite3

# Connect to SQLite (creates the file if it doesn't exist)
conn = sqlite3.connect('osint_threats.db')
cursor = conn.cursor()

# Create table for threats
cursor.execute('''
CREATE TABLE IF NOT EXISTS threats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    threat_type TEXT NOT NULL,
    indicator TEXT NOT NULL,
    description TEXT,
    date_detected DATETIME DEFAULT CURRENT_TIMESTAMP,
    confidence INTEGER,
    extra_info TEXT
)
''')

conn.commit()
conn.close()

print("✅ Database 'osint_threats.db' and table 'threats' created successfully.")
