from flask import Flask, render_template, request, Response
import sqlite3
import os
import csv
import io
from datetime import datetime
from functools import wraps

app = Flask(__name__)

# ---------------------------
# 🔐 Admin Login (HTTP Auth)
# ---------------------------
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "osint123"  # Change this before deployment

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
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# ---------------------------
# Database Access Function
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

# ---------------------------
# Routes
# ---------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/threats")
@requires_auth
def threats():
    # Get search filters and page number
    keyword = request.args.get("keyword")
    source = request.args.get("source")
    page = int(request.args.get("page", 1))
    per_page = 5
    offset = (page - 1) * per_page

    data = fetch_threats(keyword=keyword, source=source, limit=per_page, offset=offset)

    # Log access
    with open("access.log", "a") as log:
        log.write(f"{datetime.now()} - /threats accessed by {request.authorization.username}\n")

    return render_template("threats.html", threats=data, page=page, keyword=keyword or "", source=source or "")

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

if __name__ == "__main__":
    app.run(debug=True)
