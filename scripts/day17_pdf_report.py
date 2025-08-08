import sqlite3
from fpdf import FPDF
from datetime import datetime
import smtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage

# ----------------------------
# 🔐 Load environment variables
# ----------------------------
load_dotenv()
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# ----------------------------
# 📁 Correct DB path (go up one level)
# ----------------------------
db_path = os.path.abspath("../osint_threats.db")

# ----------------------------
# 🧠 Fetch threat data from SQLite
# ----------------------------
def fetch_summary():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM threats")
    total = cur.fetchone()[0]

    cur.execute("SELECT source, COUNT(*) FROM threats GROUP BY source ORDER BY COUNT(*) DESC")
    sources = cur.fetchall()

    cur.execute("SELECT type, COUNT(*) FROM threats GROUP BY type ORDER BY COUNT(*) DESC")
    types = cur.fetchall()

    cur.execute("SELECT id, source, type, keyword, domain, date_detected FROM threats ORDER BY date_detected DESC LIMIT 5")
    recent = cur.fetchall()

    conn.close()
    return total, sources, types, recent

# ----------------------------
# 📄 Generate the PDF Report
# ----------------------------
def create_pdf(total, sources, types, recent):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Day 17: OSINT Threat Report", ln=True)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(0, 10, f"Total Threats: {total}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Top Sources", ln=True)
    pdf.set_font("Arial", "", 12)
    for source, count in sources:
        pdf.cell(0, 10, f"{source}: {count}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Top Threat Types", ln=True)
    pdf.set_font("Arial", "", 12)
    for typ, count in types:
        pdf.cell(0, 10, f"{typ}: {count}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Recent Entries", ln=True)
    pdf.set_font("Arial", "", 12)
    for row in recent:
        pdf.cell(0, 10, f"{row[5]} - {row[1]} - {row[2]} - {row[4]}", ln=True)

    filename = f"day17_threat_report.pdf"
    pdf.output(filename)
    return filename

# ----------------------------
# 📧 Send Email with PDF Attached
# ----------------------------
def send_email_with_attachment(filename):
    msg = EmailMessage()
    msg['Subject'] = 'Day 17 Threat Intelligence Report'
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg.set_content('Find attached the Day 17 threat intelligence PDF report.')

    with open(filename, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=filename)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print(f"[+] Email sent to {EMAIL_RECEIVER} with {filename}")

# ----------------------------
# 🚀 Run
# ----------------------------
if __name__ == "__main__":
    total, sources, types, recent = fetch_summary()
    pdf_file = create_pdf(total, sources, types, recent)
    send_email_with_attachment(pdf_file)
