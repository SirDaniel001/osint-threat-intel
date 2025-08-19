import sqlite3
import json
import time
import pytest
from database.insert_script import insert_from_json

@pytest.fixture
def dummy_json(tmp_path):
    """Generate a large dummy JSON file for benchmarking."""
    threats = []
    for i in range(5000):
        threats.append({
            "source": "unit-test",
            "threat_type": "phishing",
            "domain": f"malicious{i}.com",
            "keywords": ["phish", "scam"],
            "first_seen": "2025-08-18"
        })

    json_path = tmp_path / "bulk.json"
    with open(json_path, "w") as f:
        json.dump(threats, f)
    return str(json_path)


def legacy_insert(json_path, db_path="legacy.db"):
    """Old slow method: insert row by row (no executemany)."""
    with open(json_path, "r") as f:
        threats = json.load(f)

    conn = sqlite3.connect(db_path)
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

    for r in threats:
        cursor.execute("""
        INSERT INTO threats (source, type, domain, keyword, date_detected)
        VALUES (?, ?, ?, ?, ?)
        """, (
            r.get("source", ""),
            r.get("threat_type", "phishing"),
            r.get("domain", ""),
            ",".join(r.get("keywords", [])),
            r.get("first_seen", "")
        ))

    conn.commit()
    conn.close()
    return len(threats)


def test_comparison(dummy_json, tmp_path):
    """Compare legacy vs optimized insert performance."""
    legacy_db = tmp_path / "legacy.db"
    optimized_db = tmp_path / "optimized.db"

    # legacy timing
    start = time.time()
    legacy_count = legacy_insert(dummy_json, db_path=str(legacy_db))
    legacy_time = time.time() - start

    # optimized timing
    start = time.time()
    optimized_count = insert_from_json(dummy_json, db_path=str(optimized_db))
    optimized_time = time.time() - start

    print(f"\n[LEGACY]   {legacy_count} records in {legacy_time:.2f}s")
    print(f"[OPTIMIZED] {optimized_count} records in {optimized_time:.2f}s")
    print(f"[SPEEDUP]  ~{legacy_time/optimized_time:.1f}x faster")

    assert legacy_count == optimized_count == 5000
    assert optimized_time < legacy_time
