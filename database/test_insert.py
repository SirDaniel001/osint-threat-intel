import sqlite3

data = (
    "Twitter",
    "phishing",
    "maliciousdomain.com",
    "Reported phishing site from feed",
    85,
    '{"country":"US","first_seen":"2025-08-06"}'
)

conn = sqlite3.connect('osint_threats.db')
cursor = conn.cursor()

cursor.execute('''
INSERT INTO threats (source, threat_type, indicator, description, confidence, extra_info)
VALUES (?, ?, ?, ?, ?, ?)
''', data)

conn.commit()
conn.close()

print("✅ Test data inserted.")
