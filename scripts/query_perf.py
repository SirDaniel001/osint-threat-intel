import sqlite3
import time

DB_PATH = "osint_threats_test.db"

def timed_query(conn, query, params=None):
    """Run a query with timing."""
    start = time.time()
    cursor = conn.execute(query, params or ())
    rows = cursor.fetchall()
    elapsed = time.time() - start
    return rows, elapsed


if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)

    print("🔎 Benchmarking queries...")

    # Example query 1: lookup by domain
    rows, t = timed_query(conn, "SELECT * FROM threats WHERE domain = ?", ("example.com",))
    print(f"[QUERY] Domain lookup returned {len(rows)} rows in {t:.4f}s")

    # Example query 2: threats in date range
    rows, t = timed_query(conn,
        "SELECT * FROM threats WHERE date_detected BETWEEN ? AND ?",
        ("2024-01-01", "2025-01-01")
    )
    print(f"[QUERY] Date range lookup returned {len(rows)} rows in {t:.4f}s")

    # Example query 3: keyword search
    rows, t = timed_query(conn, "SELECT * FROM threats WHERE keyword LIKE ?", ("%phishing%",))
    print(f"[QUERY] Keyword search returned {len(rows)} rows in {t:.4f}s")

    conn.close()
    print("✅ Benchmark complete.")
