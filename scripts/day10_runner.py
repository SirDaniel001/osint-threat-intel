import os
import subprocess
from datetime import datetime

# ---------------------------
# Config
# ---------------------------
WHOIS_SCRIPT = "day10_whois_enrichment.py"
PDF_REPORT_SCRIPT = "day10_pdf_report.py"
LOG_FILE = "../logs/day10_runner.log"

os.makedirs("../logs", exist_ok=True)

def log_message(message):
    with open(LOG_FILE, "a") as log:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{timestamp}] {message}\n")
    print(message)

def run_script(script_name):
    try:
        log_message(f"[INFO] Running {script_name}...")
        result = subprocess.run(["python", script_name], capture_output=True, text=True)
        log_message(result.stdout)
        if result.stderr:
            log_message(f"[ERROR] {result.stderr}")
    except Exception as e:
        log_message(f"[ERROR] Failed to run {script_name}: {e}")

if __name__ == "__main__":
    log_message("[INFO] Starting Day 10 Runner...")
    
    # Step 1: WHOIS Enrichment
    run_script(WHOIS_SCRIPT)
    
    # Step 2: Generate PDF + Email
    run_script(PDF_REPORT_SCRIPT)

    log_message("[+] Day 10 pipeline completed successfully!")
    print(f"\n[INFO] Log saved to {LOG_FILE}")
