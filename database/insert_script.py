import sqlite3
import json
import os
import time

try:
    from tqdm import tqdm
except ImportError:
    tqdm = lambda x, **kwargs: x  # fallback if tqdm not installed


def ensure_schema(conn):
    """Ensure the threats table and indexes exist."""
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS threats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        type TEXT,
        domain TEXT,
        keyword TEXT,
        date_detected TEXT
    )
    """)
    # useful indexes for faster queries
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_domain ON threats(domain)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_date ON threats(date_detected)")
    conn.commit()


def insert_from_json(json_path, db_path="osint_threats_test.db", log_path="logs/day24_perf.log"):
    """
    Insert threat records from a JSON file into the database with performance logging.
    Returns the number of records inserted.
    """
    # Load JSON
    with open(json_path, "r") as f:
        threats = json.load(f)

    rows = [
        (
            r.get("source", ""),
            r.get("threat_type", "phishing"),
            r.get("domain", ""),
            ",".join(r.get("keywords", [])),
            r.get("first_seen", "")
        )
        for r in threats
    ]

    # Connect DB + schema
    os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
    conn = sqlite3.connect(db_path)
    ensure_schema(conn)
    cursor = conn.cursor()

    # Bulk insert with timing
    start = time.time()
    cursor.executemany("""
        INSERT INTO threats (source, type, domain, keyword, date_detected)
        VALUES (?, ?, ?, ?, ?)
    """, tqdm(rows, desc="Inserting", unit="rec"))
    conn.commit()
    elapsed = time.time() - start
    conn.close()

    # Log performance
    os.makedirs(os.path.dirname(log_path) or ".", exist_ok=True)
    with open(log_path, "a") as logf:
        logf.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {len(rows)} records | {elapsed:.2f}s\n")

    return len(rows)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <enriched.json>")
        sys.exit(1)

    count = insert_from_json(sys.argv[1])
    print(f"✅ Inserted {count} records into threats table.")
