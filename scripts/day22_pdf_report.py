import sys
import os
import importlib.util
from datetime import datetime
import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from fpdf import FPDF  # Correct import for fpdf2

# ===== Debug: Check where fpdf2 is loaded from =====
fpdf_spec = importlib.util.find_spec("fpdf")
print(f"[DEBUG] Python executable: {sys.executable}")
print(f"[DEBUG] fpdf package location: {fpdf_spec.origin}")

if not fpdf_spec or fpdf_spec.origin is None:
    print("[ERROR] fpdf2 is not installed or cannot be found in this environment.")
    print("Run: pip install fpdf2")
    sys.exit(1)

if "venv" not in fpdf_spec.origin:
    print("[WARNING] fpdf is not loaded from your venv. This may cause import issues.")
    print("Make sure to activate your venv before running: source ../venv/bin/activate")

# ===== Email Configuration =====
EMAIL_SENDER = "danielmuteti590@gmail.com"
EMAIL_PASSWORD = "mmprpqvniofzfjvu"  # Gmail App Password
EMAIL_RECEIVER = "danielmuteti590@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# ===== 1. PDF Generation =====
class Day22PDF(FPDF):
    def header(self):
        # Add Unicode-capable font
        self.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", uni=True)
        self.set_font("DejaVu", '', 16)
        self.cell(0, 10, "📅 Day 22 — Dark Mode & Dynamic Chart Themes",
                  new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", '', 8)
        self.cell(0, 10, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", align="C")

    def chapter_title(self, title):
        self.set_font("DejaVu", '', 14)
        self.multi_cell(0, 8, title)
        self.ln(2)

    def chapter_body(self, body):
        self.set_font("DejaVu", '', 12)
        self.multi_cell(0, 7, body)
        self.ln(1)

def generate_day22_pdf(output_path, light_screenshot=None, dark_screenshot=None):
    pdf = Day22PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Overview
    pdf.chapter_title("🔹 Overview")
    pdf.chapter_body(
        "Today’s milestone focused on upgrading the dashboard’s UI/UX by adding Dark Mode "
        "support and making Chart.js visualizations adapt instantly to theme changes. "
        "This brings a more modern, premium feel to the OSINT Threat Intelligence Dashboard."
    )

    # Today’s Wins
    pdf.chapter_title("🏆 Today’s Wins")
    wins = [
        "Dark Mode toggle button in navbar for instant theme switching.",
        "Theme preference saved in localStorage and applied on page load.",
        "Smooth transitions for background, text, cards, and tables.",
        "Charts automatically recolor based on selected theme.",
        "High-contrast palettes for dark mode.",
        "500 ms smooth animations for theme transitions.",
        "Event-driven chart refresh using custom themeChange event."
    ]
    for w in wins:
        pdf.chapter_body(f"• {w}")

    # Key Insights
    pdf.chapter_title("💡 Key Insights")
    insights = [
        "Dark Mode improves readability in low-light environments.",
        "Dynamic chart recoloring ensures visual consistency without refresh.",
        "Smooth transitions make the dashboard feel polished and professional."
    ]
    for i in insights:
        pdf.chapter_body(f"• {i}")

    # Momentum for Tomorrow
    pdf.chapter_title("🚀 Momentum for Tomorrow")
    pdf.chapter_body(
        "Begin integrating real-time OSINT data feeds into charts so visualizations "
        "update without manual refresh. Explore adding a theme-aware PDF export "
        "to match the current dashboard style in reports."
    )

    # Screenshots
    if light_screenshot or dark_screenshot:
        pdf.chapter_title("📸 Dashboard Screenshots")
        if light_screenshot and os.path.exists(light_screenshot):
            pdf.chapter_body("Light Mode View:")
            pdf.image(light_screenshot, w=170)
            pdf.ln(5)
        if dark_screenshot and os.path.exists(dark_screenshot):
            pdf.chapter_body("Dark Mode View:")
            pdf.image(dark_screenshot, w=170)
            pdf.ln(5)

    pdf.output(output_path)
    print(f"[+] PDF generated at: {output_path}")

# ===== 2. Email Sending =====
def send_email_with_pdf(sender_email, sender_password, recipient_email, pdf_path):
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = "Day 22 Report — Dark Mode & Dynamic Chart Themes"

    body = "Attached is the Day 22 PDF report for your OSINT Threat Intelligence Dashboard."
    msg.attach(MIMEText(body, "plain"))

    with open(pdf_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(pdf_path)}")
        msg.attach(part)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

    print(f"[+] Email sent to {recipient_email}")

# ===== 3. Run Generation + Email =====
if __name__ == "__main__":
    OUTPUT_PDF = "day22_report.pdf"
    LIGHT_SCREENSHOT = "light_mode_dashboard.png"  # optional
    DARK_SCREENSHOT = "dark_mode_dashboard.png"    # optional

    generate_day22_pdf(OUTPUT_PDF, LIGHT_SCREENSHOT, DARK_SCREENSHOT)
    send_email_with_pdf(EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER, OUTPUT_PDF)
