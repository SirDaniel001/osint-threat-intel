from flask import Flask, render_template, request, Response, jsonify, send_file, url_for, abort, redirect
import sqlite3
import os
import csv
import io
import shutil
import tempfile
import subprocess
from datetime import datetime, date, timedelta
from functools import wraps
from dotenv import load_dotenv

# ---------------------------
# 🔐 Load environment variables
# ---------------------------
load_dotenv()
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

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
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# ---------------------------
# 🧠 DB Helper
# ---------------------------
def db_connect():
    db_path = os.path.abspath('../osint_threats.db')
    return sqlite3.connect(db_path)

# ---------------------------
# 🧠 Data Fetchers
# ---------------------------
def fetch_threats(keyword=None, source=None, typ=None, domain=None,
                  date_from=None, date_to=None, limit=10, offset=0):
    conn = db_connect()
    cursor = conn.cursor()
    query = """
        SELECT id, source, type, keyword, domain, date_detected
        FROM threats
    """
    filters, params = [], []
    if keyword:
        filters.append("keyword LIKE ?"); params.append(f"%{keyword}%")
    if source:
        filters.append("source LIKE ?"); params.append(f"%{source}%")
    if typ:
        filters.append("type LIKE ?"); params.append(f"%{typ}%")
    if domain:
        filters.append("domain LIKE ?"); params.append(f"%{domain}%")
    if date_from:
        filters.append("date_detected >= ?"); params.append(date_from)
    if date_to:
        filters.append("date_detected <= ?"); params.append(date_to)

    if filters:
        query += " WHERE " + " AND ".join(filters)
    query += " ORDER BY date_detected DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

def count_threats(**kwargs):
    conn = db_connect()
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM threats"
    filters, params = [], []
    for field in ["keyword", "source", "typ", "domain", "date_from", "date_to"]:
        val = kwargs.get(field)
        if field == "keyword" and val:
            filters.append("keyword LIKE ?"); params.append(f"%{val}%")
        elif field == "source" and val:
            filters.append("source LIKE ?"); params.append(f"%{val}%")
        elif field == "typ" and val:
            filters.append("type LIKE ?"); params.append(f"%{val}%")
        elif field == "domain" and val:
            filters.append("domain LIKE ?"); params.append(f"%{val}%")
        elif field == "date_from" and val:
            filters.append("date_detected >= ?"); params.append(val)
        elif field == "date_to" and val:
            filters.append("date_detected <= ?"); params.append(val)
    if filters:
        query += " WHERE " + " AND ".join(filters)
    cursor.execute(query, params)
    total = cursor.fetchone()[0] or 0
    conn.close()
    return total

def fetch_chart_data():
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT type, COUNT(*) FROM threats GROUP BY type")
    threats_by_type = cursor.fetchall()
    cursor.execute("SELECT source, COUNT(*) FROM threats GROUP BY source")
    threats_by_source = cursor.fetchall()
    cursor.execute("SELECT date_detected, COUNT(*) FROM threats GROUP BY date_detected ORDER BY date_detected")
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
    if "malware" in t: score += 70
    elif "phishing" in t: score += 55
    else: score += 30
    if "darkweb" in s: score += 20
    elif "pastebin" in s: score += 8
    elif "phishtank" in s: score += 5
    suspicious_tokens = ["secure", "login", "verify", "account", "update", "confirm"]
    if any(tok in d for tok in suspicious_tokens): score += 10
    if any(tok in k for tok in ["cbk", "mpesa", "m-pesa", "central bank", "bank"]): score += 5
    return min(100, score)

def fetch_dashboard_metrics():
    conn = db_connect()
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
            "id": r[0], "source": r[1], "type": r[2],
            "keyword": r[3], "domain": r[4],
            "date_detected": r[5], "risk_score": score
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
# 🌐 API for Charts
# ---------------------------
@app.route("/api/trends/by_type")
@requires_auth
def api_by_type():
    data = fetch_chart_data()["by_type"]
    return jsonify({"labels": [x[0] for x in data], "data": [x[1] for x in data]})

@app.route("/api/trends/by_source")
@requires_auth
def api_by_source():
    data = fetch_chart_data()["by_source"]
    return jsonify({"labels": [x[0] for x in data], "data": [x[1] for x in data]})

@app.route("/api/trends/by_date")
@requires_auth
def api_by_date():
    data = fetch_chart_data()["by_date"]
    return jsonify({"labels": [x[0] for x in data], "data": [x[1] for x in data]})

# ---------------------------
# 🌐 Routes
# ---------------------------
@app.route("/")
def index():
    return redirect(url_for("dashboard"))  # Redirect home to dashboard

@app.route("/dashboard")
@requires_auth
def dashboard():
    metrics = fetch_dashboard_metrics()
    chart_data = fetch_chart_data()
    return render_template("dashboard.html", metrics=metrics, chart_data=chart_data)

@app.route("/threats")
@requires_auth
def threats():
    keyword = request.args.get("keyword")
    source = request.args.get("source")
    typ = request.args.get("type")
    domain = request.args.get("domain")
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")
    page = int(request.args.get("page", 1))
    per_page = 5
    offset = (page - 1) * per_page
    data = fetch_threats(keyword=keyword, source=source, typ=typ, domain=domain,
                         date_from=date_from, date_to=date_to, limit=per_page, offset=offset)
    return render_template("threats.html", threats=data, page=page,
                           keyword=keyword or "", source=source or "",
                           threat_type=typ or "", domain=domain or "",
                           date_from=date_from or "", date_to=date_to or "")

@app.route("/api/threats")
@requires_auth
def api_threats():
    keyword = request.args.get("keyword") or None
    source = request.args.get("source") or None
    typ = request.args.get("type") or None
    domain = request.args.get("domain") or None
    date_from = request.args.get("date_from") or None
    date_to = request.args.get("date_to") or None
    try: page = max(1, int(request.args.get("page", 1)))
    except ValueError: page = 1
    per_page = int(request.args.get("per_page", 10))
    offset = (page - 1) * per_page
    rows = fetch_threats(keyword=keyword, source=source, typ=typ, domain=domain,
                         date_from=date_from, date_to=date_to, limit=per_page, offset=offset)
    total = count_threats(keyword=keyword, source=source, typ=typ, domain=domain,
                          date_from=date_from, date_to=date_to)
    threats_list = [{"id": r[0], "source": r[1], "type": r[2],
                     "keyword": r[3], "domain": r[4], "date_detected": r[5]} for r in rows]
    return jsonify({"total": total, "page": page, "per_page": per_page, "threats": threats_list})

@app.route("/export-csv")
@requires_auth
def export_csv():
    data = fetch_threats()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Source', 'Type', 'Keyword', 'Domain', 'Date Detected'])
    for row in data: writer.writerow(row)
    return Response(output.getvalue(), mimetype='text/csv',
                    headers={"Content-Disposition": "attachment;filename=threats_export.csv"})

@app.route("/logout")
def logout():
    return Response('Logged out.\n', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

# ---------------------------
# 📄 PDF Report Routes (14-day KPIs)
# ---------------------------
@app.route("/report")
@requires_auth
def report_html():
    chart_data = fetch_chart_data()

    # 14-day period
    today = date.today()
    period_start = (today - timedelta(days=13)).isoformat()

    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, source, type, keyword, domain, date_detected
        FROM threats
        WHERE date_detected >= ?
        ORDER BY date_detected DESC
    """, (period_start,))
    rows = cursor.fetchall()
    conn.close()

    period_threats = []
    for r in rows:
        score = compute_risk_score(r)
        period_threats.append({
            "id": r[0], "source": r[1], "type": r[2],
            "keyword": r[3], "domain": r[4],
            "date_detected": r[5], "risk_score": score
        })

    kpis = {
        "phishing_count": sum(1 for t in period_threats if t["type"] and t["type"].lower() == "phishing"),
        "darkweb_hits": sum(1 for t in period_threats if t["source"] and "darkweb" in t["source"].lower()),
        "whois_suspicious": sum(1 for t in period_threats if t["source"] and "whois" in t["source"].lower()),
        "alerts": sum(1 for t in period_threats if t["risk_score"] >= 75)
    }

    labels = [d for d, _ in chart_data["by_date"]]
    values = [c for _, c in chart_data["by_date"]]

    recent = [
        {
            "domain": t["domain"],
            "source": t["source"],
            "date_found": t["date_detected"]
        }
        for t in period_threats[:10]
    ]

    meta = {
        "generated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "period": f"{period_start} to {today.isoformat()}",
    }

    return render_template(
        "report.html",
        kpis=kpis,
        recent=recent,
        labels=labels,
        values=values,
        meta=meta
    )

@app.route("/report.pdf")
@requires_auth
def report_pdf():
    report_url = url_for("report_html", _external=True)
    chromium = (shutil.which("chromium")
                or shutil.which("chromium-browser")
                or shutil.which("google-chrome")
                or shutil.which("chrome"))
    if not chromium:
        abort(500, "Chromium/Chrome not found. Install 'chromium' package.")
    tmp = tempfile.NamedTemporaryFile(prefix="osint_report_", suffix=".pdf", delete=False)
    tmp.close()
    pdf_path = tmp.name
    cmd = [
        chromium,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=6000",
        f"--print-to-pdf={pdf_path}",
        report_url
    ]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        abort(500, f"PDF render failed: {e}")
    filename = f"threat_intel_report_{date.today().isoformat()}.pdf"
    return send_file(pdf_path, as_attachment=True, download_name=filename)

# ---------------------------
# 🚀 Run App
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
