import sqlite3
import pytest
import time
from database.insert_script import insert_from_json

DB_PATH = "osint_threats_test.db"

@pytest.fixture(scope="module")
def setup_db(tmp_path_factory):
    """Create a temporary DB with sample data for query benchmarking."""
    db_path = tmp_path_factory.mktemp("data") / "test_perf.db"

    # sample dataset
    sample_data = [
        {
            "source": "test_feed",
            "threat_type": "phishing",
            "domain": f"example{i}.com",
            "keywords": ["phishing", "test"],
            "first_seen": "2025-01-01"
        }
        for i in range(1000)
    ]

    import json
    json_file = tmp_path_factory.mktemp("data") / "sample.json"
    with open(json_file, "w") as f:
        json.dump(sample_data, f)

    # insert into DB
    insert_from_json(str(json_file), db_path=str(db_path))
    return str(db_path)


def timed_query(conn, query, params=None):
    """Helper to time queries."""
    start = time.time()
    rows = conn.execute(query, params or ()).fetchall()
    elapsed = time.time() - start
    return len(rows), elapsed


def test_query_performance(setup_db):
    """Ensure queries run efficiently on threats table."""
    conn = sqlite3.connect(setup_db)

    # domain lookup
    rows, t = timed_query(conn, "SELECT * FROM threats WHERE domain = ?", ("example1.com",))
    assert rows > 0
    assert t < 0.05  # should be fast

    # date range
    rows, t = timed_query(conn,
        "SELECT * FROM threats WHERE date_detected BETWEEN ? AND ?",
        ("2024-01-01", "2025-12-31")
    )
    assert rows > 0
    assert t < 0.05

    # keyword search
    rows, t = timed_query(conn, "SELECT * FROM threats WHERE keyword LIKE ?", ("%phishing%",))
    assert rows > 0
    assert t < 0.05

    conn.close()
