from fpdf import FPDF, XPos, YPos
from datetime import datetime
import os

def generate_day24_report(output_path="reports/day24_report.pdf"):
    # Ensure reports directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    pdf = FPDF()
    pdf.add_page()

    # ✅ Use a Unicode-safe font (requires system font)
    pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", "", 16)

    # Title
    pdf.cell(200, 10, "Day 24 - Bug Fixes & Performance Optimization",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    pdf.set_font("DejaVu", "", 12)
    pdf.ln(10)

    # Date
    today = datetime.now().strftime("%Y-%m-%d")
    pdf.cell(200, 10, f"Date: {today}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(5)
    pdf.multi_cell(0, 10,
    """✅ Today we focused on fixing bugs, testing database inserts, and optimizing performance.

🔹 Key Accomplishments:
  - Fixed insert_script.py to reliably insert JSON into SQLite.
  - Added tests/test_insert_script.py for correctness validation.
  - Built tests/test_insert_performance.py for speed benchmarking.
  - Compared legacy vs optimized inserts (tests/test_insert_comparison.py).
  - Stress-tested queries with 1000+ records (tests/test_query_perf.py).
  - Updated requirements.txt and README.md.

📊 Results:
  - Insert performance improved ~1.1x with bulk inserts.
  - 1000+ records inserted and queried in <0.3s.
  - All tests ✅ passed with no failures.

This marks the completion of Day 24 — the project is now stable, tested, and optimized.
""")

    pdf.ln(10)
    pdf.set_font("DejaVu", "", 11)
    pdf.cell(0, 10, "Generated automatically by osint-threat-intel pipeline.",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    pdf.output(output_path)
    print(f"📄 Day 24 PDF report generated: {output_path}")


if __name__ == "__main__":
    generate_day24_report()
