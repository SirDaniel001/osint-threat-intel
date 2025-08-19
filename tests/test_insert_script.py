import os
import sqlite3
import pytest
from database.insert_script import insert_from_json

@pytest.fixture
def temp_db_file():
    """Create a temporary SQLite DB with a threats table."""
    import tempfile
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".db") as f:
        db_path = f.name
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE threats (
            id INTEGER PRIMARY KEY,
            source TEXT,
            type TEXT,
            domain TEXT,
            keyword TEXT,
            date_detected TEXT
        )
    """)
    conn.commit()
    conn.close()
    return db_path

def test_insert_from_dummy_json(temp_db_file):
    """Ensure dummy JSON inserts into DB correctly."""
    json_path = os.path.join("tests", "data", "dummy_threats.json")
    count = insert_from_json(json_path, db_path=temp_db_file)
    assert count == 1

    # Validate DB contents
    conn = sqlite3.connect(temp_db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT source, type, domain FROM threats")
    row = cursor.fetchone()
    conn.close()

    assert row == ("static_test", "phishing", "permanent-test.com")

    os.remove(temp_db_file)
