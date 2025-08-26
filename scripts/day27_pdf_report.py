import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from fpdf import FPDF, XPos, YPos
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Register fonts at initialization
        self.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
        self.add_font("DejaVu", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")

    def header(self):
        self.set_font("DejaVu", "B", 14)
        self.cell(0, 10, "OSINT Threat Intelligence Report - Day 27",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def chapter_title(self, title):
        self.set_font("DejaVu", "B", 12)
        self.cell(0, 10, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def chapter_body(self, body):
        self.set_font("DejaVu", "", 10)
        self.multi_cell(0, 10, body)
        self.ln()

def generate_report():
    pdf = PDF()
    pdf.add_page()

    # Title
    pdf.set_font("DejaVu", "B", 16)
    pdf.cell(0, 10, "Day 27 – Release & Documentation",
              new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(10)

    # Metadata
    pdf.set_font("DejaVu", "", 10)
    pdf.cell(0, 10, f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
              new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(10)

    # Sections
    pdf.chapter_title("Achievements")
    pdf.chapter_body(
        "- Packaged the final release build.\n"
        "- Updated the README.md with Day 27 progress.\n"
        "- Logged the success_journal entry for milestone tracking.\n"
        "- Generated automated PDF reporting with email integration."
    )

    pdf.chapter_title("Lessons Learned")
    pdf.chapter_body(
        "- Final release packaging ensures reproducibility.\n"
        "- Documentation updates should be consistent with project progress.\n"
        "- Automating reporting saves time and avoids human error.\n"
        "- Email delivery of reports ensures accountability."
    )

    pdf.chapter_title("Status")
    pdf.chapter_body("✅ Release finalized, documentation updated, reporting automated.")

    output_file = "day27_report.pdf"
    pdf.output(output_file)
    print(f"✅ PDF report generated: {os.path.abspath(output_file)}")
    return output_file

def send_email(report_file):
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")

    if not sender or not password or not receiver:
        raise ValueError("❌ Missing email environment variables. Check your .env file.")

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = "Day 27 OSINT Report"

    body = "Attached is the Day 27 OSINT Threat Intelligence Report."
    msg.attach(MIMEText(body, "plain"))

    with open(report_file, "rb") as f:
        attachment = MIMEApplication(f.read(), Name=os.path.basename(report_file))
    attachment["Content-Disposition"] = f'attachment; filename="{os.path.basename(report_file)}"'
    msg.attach(attachment)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())

    print("📧 Email sent successfully.")

if __name__ == "__main__":
    report_file = generate_report()
    send_email(report_file)
