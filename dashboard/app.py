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
def fetch_threats(keyword=None, source=None, threat_type=None, date=None, limit=10, offset=0):
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
    if threat_type:
        filters.append("type LIKE ?")
        params.append(f"%{threat_type}%")
    if date:
        try:
            parsed_date = datetime.strptime(date, "%d-%b").replace(year=datetime.now().year)
            date_str = parsed_date.strftime("%Y-%m-%d")
            filters.append("date_detected = ?")
            params.append(date_str)
        except ValueError:
            pass

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

    cursor.execute("SELECT strftime('%d-%b', date_detected), COUNT(*) FROM threats GROUP BY date_detected ORDER BY date_detected")
    threats_by_date = cursor.fetchall()

    conn.close()
    return {
        "by_type": threats_by_type,
        "by_source": threats_by_source,
        "by_date": threats_by_date
    }

# ---------------------------
# 📊 Dashboard Metrics
# ---------------------------
def compute_risk_score(threat_row):
    try:
        _, source, typ, keyword, domain, _ = threat_row
    except Exception:
        return 0

    score = 0
    t = typ.lower() if typ else ""
    s = source.lower() if source else ""
    d = domain.lower() if domain else ""
    k = keyword.lower() if keyword else ""

    if "malware" in t:
        score += 70
    elif "phishing" in t:
        score += 55
    else:
        score += 30

    if "darkweb" in s:
        score += 20
    elif "pastebin" in s:
        score += 8
    elif "phishtank" in s:
        score += 5

    suspicious_tokens = ["secure", "login", "verify", "account", "update", "confirm"]
    if any(tok in d for tok in suspicious_tokens):
        score += 10

    if any(tok in k for tok in ["cbk", "mpesa", "m-pesa", "central bank", "bank"]):
        score += 5

    return min(100, score)

def fetch_dashboard_metrics():
    db_path = os.path.abspath('../osint_threats.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM threats")
    total = cursor.fetchone()[0] or 0

    cursor.execute("SELECT source, COUNT(*) FROM threats GROUP BY source ORDER BY COUNT(*) DESC LIMIT 5")
    top_sources = cursor.fetchall()

    cursor.execute("SELECT type, COUNT(*) FROM threats GROUP BY type ORDER BY COUNT(*) DESC LIMIT 5")
    top_types = cursor.fetchall()

    cursor.execute("SELECT keyword, COUNT(*) FROM threats GROUP BY keyword ORDER BY COUNT(*) DESC LIMIT 5")
    top_keywords = cursor.fetchall()

    cursor.execute("SELECT id, source, type, keyword, domain, date_detected FROM threats ORDER BY date_detected DESC LIMIT 10")
    rows = cursor.fetchall()

    recent_threats = []
    for r in rows:
        score = compute_risk_score(r)
        recent_threats.append({
            "id": r[0],
            "source": r[1],
            "type": r[2],
            "keyword": r[3],
            "domain": r[4],
            "date_detected": r[5],
            "risk_score": score
        })

    conn.close()
    avg_risk = round(sum(t["risk_score"] for t in recent_threats) / (len(recent_threats) or 1), 1)

    return {
        "total": total,
        "top_sources": top_sources,
        "top_types": top_types,
        "top_keywords": top_keywords,
        "recent_threats": recent_threats,
        "avg_risk": avg_risk
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
    threat_type = request.args.get("type")
    date = request.args.get("date")
    page = int(request.args.get("page", 1))
    per_page = 5
    offset = (page - 1) * per_page

    data = fetch_threats(
        keyword=keyword,
        source=source,
        threat_type=threat_type,
        date=date,
        limit=per_page,
        offset=offset
    )

    with open("access.log", "a") as log:
        log.write(f"{datetime.now()} - /threats accessed by {request.authorization.username}\n")

    return render_template(
        "threats.html",
        threats=data,
        page=page,
        keyword=keyword or "",
        source=source or "",
        threat_type=threat_type or "",
        date=date or ""
    )

@app.route("/dashboard")
@requires_auth
def dashboard():
    chart_data = fetch_chart_data()
    metrics = fetch_dashboard_metrics()
    return render_template("dashboard.html", chart_data=chart_data, metrics=metrics)

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

@app.route("/logout")
def logout():
    return Response(
        'Logged out.\n', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

if __name__ == "__main__":
    app.run(debug=True)
