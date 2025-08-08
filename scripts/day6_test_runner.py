import subprocess
import os
import pandas as pd
from datetime import datetime

# ----------------------------
# Config
# ----------------------------
DATA_DIR = "../data"
LOG_DIR = "../logs"
SUMMARY_LOG = os.path.join(LOG_DIR, "day6_test_summary.log")

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

def run_script(script_name):
    print(f"\n[INFO] Running {script_name}...")
    try:
        result = subprocess.run(["python", script_name], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"[ERROR] {result.stderr}")
    except Exception as e:
        print(f"[ERROR] Failed to run {script_name}: {e}")

def get_csv_stats(file_path):
    if not os.path.exists(file_path):
        return 0
    df = pd.read_csv(file_path)
    return len(df), df

def log_summary(summary_text):
    with open(SUMMARY_LOG, "a") as log_file:
        log_file.write(f"\n--- {datetime.now()} ---\n")
        log_file.write(summary_text)
        log_file.write("\n")

if __name__ == "__main__":
    print("\n[INFO] Starting Day 6 Test Runner...\n")

    # Run scripts
    run_script("openphish_integration.py")
    run_script("phishing_feeds_combined.py")
    run_script("day5_cleaning_script.py")

    # Collect stats
    openphish_file = os.path.join(DATA_DIR, "openphish_data.csv")
    combined_file = os.path.join(DATA_DIR, "combined_phishing_data.csv")
    cleaned_file = os.path.join(DATA_DIR, "cleaned_phishing_data.csv")

    openphish_count, _ = get_csv_stats(openphish_file)
    combined_count, _ = get_csv_stats(combined_file)
    cleaned_count, cleaned_df = get_csv_stats(cleaned_file)

    kenyan_count = 0
    if cleaned_count > 0 and "tld" in cleaned_df.columns:
        kenyan_count = cleaned_df[cleaned_df["tld"] == "ke"].shape[0]

    # Print summary
    summary = f"""
    [SUMMARY REPORT - Day 6]
    OpenPhish URLs: {openphish_count}
    Combined URLs (OpenPhish + URLhaus): {combined_count}
    Cleaned URLs: {cleaned_count}
    Kenyan URLs: {kenyan_count}
    Data Directory: {DATA_DIR}
    Log saved to: {SUMMARY_LOG}
    """
    print(summary)

    # Save to log
    log_summary(summary)
    print("[INFO] Day 6 Test Summary logged successfully!")
