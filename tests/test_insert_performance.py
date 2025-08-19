import os
import sqlite3
import time
import json
import tempfile
import pytest

from database.insert_script import insert_from_json


@pytest.fixture
def dummy_json(tmp_path):
    """Generate a large dummy JSON file for benchmarking."""
    threats = []
    for i in range(5000):  # adjust to make the test heavier
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


def test_bulk_insert_speed(dummy_json, tmp_path):
    """Benchmark bulk insert performance."""
    db_path = tmp_path / "perf_test.db"

    # create threats table
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE threats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            type TEXT,
            domain TEXT,
            keyword TEXT,
            date_detected TEXT
        )
    """)
    conn.commit()
    conn.close()

    # measure execution time
    start = time.time()
    count = insert_from_json(dummy_json, db_path=str(db_path))
    duration = time.time() - start

    print(f"\n[PERF] Inserted {count} records in {duration:.2f} seconds")

    # sanity checks
    assert count == 5000
    assert duration < 5.0  # must be reasonably fast (tweak as needed)
