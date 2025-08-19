# scripts/day23_pdf_report.py
"""
Day 23 — PDF Threat Report Generator
Generates a phishing threat PDF from threats.db (with fallback seeding if DB/table is missing).
"""

import os
import sqlite3
from datetime import datetime

import pandas as pd
from fpdf import FPDF

DB_PATH = "threats.db"
REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

# --- DB Setup ---------------------------------------------------------------
def ensure_db():
    """Ensure threats.db exists with a threats table and seed if empty."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # Create table if missing
    cur.execute("""
        CREATE TABLE IF NOT EXISTS threats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT NOT NULL,
            first_seen TEXT NOT NULL
        )
    """)
    conn.commit()

    # Seed if empty
    cur.execute("SELECT COUNT(*) FROM threats")
    count = cur.fetchone()[0]
    if count == 0:
        print("[Day23] ⚠️ No threats found in DB, seeding with sample data...")
        seed_data = [
            ("phishy-login.com", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            ("malicious-verify.net", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            ("fake-office365.org", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        ]
        cur.executemany("INSERT INTO threats (domain, first_seen) VALUES (?, ?)", seed_data)
        conn.commit()
    conn.close()

# --- Font discovery ---------------------------------------------------------
DEJAVU_CANDIDATE_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/dejavu",
    "/usr/local/share/fonts",
    os.path.expanduser("~/.local/share/fonts"),
]

def first_exists(paths):
    for p in paths:
        if p and os.path.isfile(p):
            return p
    return None

def find_dejavu():
    regular = first_exists([os.path.join(d, "DejaVuSans.ttf") for d in DEJAVU_CANDIDATE_DIRS])
    bold    = first_exists([os.path.join(d, "DejaVuSans-Bold.ttf") for d in DEJAVU_CANDIDATE_DIRS])
    italic  = first_exists([os.path.join(d, "DejaVuSans-Oblique.ttf") for d in DEJAVU_CANDIDATE_DIRS])
    return regular, bold, italic

# --- PDF Class --------------------------------------------------------------
class PDF(FPDF):
    def __init__(self, use_unicode=True, dejavu_paths=None):
        super().__init__()
        self.use_unicode = use_unicode
        self.dejavu_paths = dejavu_paths or (None, None, None)

        if self.use_unicode:
            reg, bold, italic = self.dejavu_paths
            self.add_font("DejaVu", "", reg)
            if bold: self.add_font("DejaVu", "B", bold)
            if italic: self.add_font("DejaVu", "I", italic)
            self.set_font("DejaVu", "", 12)
        else:
            self.set_font("Helvetica", "", 12)

    def header(self):
        if self.use_unicode:
            self.set_font("DejaVu", "B", 12)
        else:
            self.set_font("Helvetica", "B", 12)

        self.cell(0, 10, "OSINT Phishing Threat Report",
                  border=False, new_x="LMARGIN", new_y="NEXT", align="C")

        if self.use_unicode:
            self.set_font("DejaVu", "", 10)
        else:
            self.set_font("Helvetica", "", 10)

        self.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                  new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        if self.use_unicode and self.dejavu_paths[2]:
            self.set_font("DejaVu", "I", 8)
        else:
            self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

# --- Data Access ------------------------------------------------------------
def fetch_latest_threats(limit=20):
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(
            "SELECT domain, first_seen FROM threats ORDER BY first_seen DESC LIMIT ?",
            conn, params=(limit,)
        )
    finally:
        conn.close()
    return df

# --- Report Generation ------------------------------------------------------
def generate_pdf_report():
    ensure_db()
    df = fetch_latest_threats(limit=20)

    reg, bold, italic = find_dejavu()
    unicode_ready = all([reg, bold, italic])

    if unicode_ready:
        print("[Day23] ✨ Using DejaVu Sans (Unicode, bold, italic).")
        pdf = PDF(use_unicode=True, dejavu_paths=(reg, bold, italic))
    else:
        print("[Day23] ℹ️ DejaVu fonts not fully available. Falling back to core Helvetica (ASCII only).")
        pdf = PDF(use_unicode=False)

    pdf.add_page()

    if pdf.use_unicode:
        pdf.set_font("DejaVu", "B", 14)
    else:
        pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Latest Phishing Domains", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    if pdf.use_unicode:
        pdf.set_font("DejaVu", "B", 12)
    else:
        pdf.set_font("Helvetica", "B", 12)
    pdf.cell(110, 10, "Domain", 1, 0, "C")
    pdf.cell(70, 10, "First Seen", 1, 1, "C")

    if pdf.use_unicode:
        pdf.set_font("DejaVu", "", 10)
    else:
        pdf.set_font("Helvetica", "", 10)

    for _, row in df.iterrows():
        pdf.cell(110, 10, str(row["domain"]), 1, 0, "L")
        pdf.cell(70, 10, str(row["first_seen"]), 1, 1, "C")

    filename = f"day23_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    path = os.path.join(REPORTS_DIR, filename)
    pdf.output(path)
    return path

# --- Main -------------------------------------------------------------------
if __name__ == "__main__":
    print("[Day23] 📄 Generating PDF threat report...")
    out = generate_pdf_report()
    print(f"[Day23] ✅ Report saved to {out}")
    print("[Day23] 📧 Ready for email delivery (Day20 integration).")
