from flask import Flask, render_template, request, Response
import sqlite3
import os
import csv
import io
from datetime import datetime
from functools import wraps
from dotenv import load_dotenv

# ---------------------------
# 🔐 Load environment variables
# ---------------------------
load_dotenv()
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# Debug print — remove in production
print("Loaded username:", ADMIN_USERNAME)
print("Loaded password:", ADMIN_PASSWORD)

# ---------------------------
# Flask App
# ---------------------------
app = Flask(__name__)

# ---------------------------
# 🔐 Basic Auth
# ---------------------------
def check_auth(username, password):
    return username == ADMIN_USERNAME and password == ADMIN_PASSWORD

def authenticate():
    return Response(
        'Access denied.\n', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            print("[AUTH DEBUG] Missing or invalid credentials:", auth)
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# ---------------------------
# 🧠 Data Fetchers
# ---------------------------
def fetch_threats(keyword=None, source=None, limit=10, offset=0):
    db_path = os.path.abspath('../osint_threats.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
        SELECT id, source, type, keyword, domain, date_detected
        FROM threats
    """
    filters = []
    params = []

    if keyword:
        filters.append("keyword LIKE ?")
        params.append(f"%{keyword}%")
    if source:
        filters.append("source LIKE ?")
        params.append(f"%{source}%")

    if filters:
        query += " WHERE " + " AND ".join(filters)

    query += " ORDER BY date_detected DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

def fetch_chart_data():
    db_path = os.path.abspath('../osint_threats.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT type, COUNT(*) FROM threats GROUP BY type")
    threats_by_type = cursor.fetchall()

    cursor.execute("SELECT source, COUNT(*) FROM threats GROUP BY source")
    threats_by_source = cursor.fetchall()

    # 👇 UPDATED: Human-readable chart dates (e.g., "08-Aug")
    cursor.execute("SELECT strftime('%d-%b', date_detected), COUNT(*) FROM threats GROUP BY date_detected ORDER BY date_detected")
    threats_by_date = cursor.fetchall()

    conn.close()
    return {
        "by_type": threats_by_type,
        "by_source": threats_by_source,
        "by_date": threats_by_date
    }

# ---------------------------
# 🌐 Routes
# ---------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/threats")
@requires_auth
def threats():
    keyword = request.args.get("keyword")
    source = request.args.get("source")
    page = int(request.args.get("page", 1))
    per_page = 5
    offset = (page - 1) * per_page

    data = fetch_threats(keyword=keyword, source=source, limit=per_page, offset=offset)

    with open("access.log", "a") as log:
        log.write(f"{datetime.now()} - /threats accessed by {request.authorization.username}\n")

    return render_template("threats.html", threats=data, page=page, keyword=keyword or "", source=source or "")

@app.route("/dashboard")
@requires_auth
def dashboard():
    chart_data = fetch_chart_data()
    print("[DEBUG] Chart data:", chart_data)
    return render_template("dashboard.html", chart_data=chart_data)

@app.route("/export-csv")
@requires_auth
def export_csv():
    data = fetch_threats()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Source', 'Type', 'Keyword', 'Domain', 'Date Detected'])
    for row in data:
        writer.writerow(row)

    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment;filename=threats_export.csv"}
    )

# ---------------------------
# 🔓 Logout Trigger
# ---------------------------
@app.route("/logout")
def logout():
    return Response(
        'Logged out.\n', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

# ---------------------------
# 🏁 Start Server
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
