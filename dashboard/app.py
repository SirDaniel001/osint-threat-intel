from flask import Flask, render_template, Response
import sqlite3
import os
import csv
import io
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

def fetch_threats():
    db_path = os.path.abspath('../osint_threats.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, source, type, keyword, domain, date_detected
        FROM threats
        ORDER BY date_detected DESC
        LIMIT 10;
    """)
    results = cursor.fetchall()
    conn.close()
    return results

@app.route("/threats")
def threats():
    data = fetch_threats()

    # 📜 Log access to /threats route
    with open("access.log", "a") as log:
        log.write(f"{datetime.now()} - /threats accessed\n")

    return render_template("threats.html", threats=data)

@app.route("/export-csv")
def export_csv():
    data = fetch_threats()

    # Write data to CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Source', 'Type', 'Keyword', 'Domain', 'Date Detected'])
    for row in data:
        writer.writerow(row)

    # Return as downloadable file
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment;filename=threats_export.csv"}
    )

if __name__ == "__main__":
    app.run(debug=True)
