import requests
import pandas as pd
import os
from datetime import datetime
import logging
import time
from io import StringIO  # ✅ Fix for reading CSV from text

# ----------------------------
# Configuration
# ----------------------------
OPENPHISH_URL = "https://raw.githubusercontent.com/openphish/public_feed/refs/heads/main/feed.txt"
URLHAUS_URL = "https://urlhaus.abuse.ch/downloads/csv_online/"

DATA_DIR = "../data"
LOG_DIR = "../logs"
OUTPUT_FILE = os.path.join(DATA_DIR, "combined_phishing_data.csv")
LOG_FILE = os.path.join(LOG_DIR, "combined_feeds.log")

KENYAN_KEYWORDS = ["cbk", "mpesa", ".ke"]

# ----------------------------
# Logging Setup
# ----------------------------
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ----------------------------
# Retry Function
# ----------------------------
def fetch_with_retry(url, retries=3, delay=5):
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"[ERROR] Attempt {attempt} failed for {url}: {e}")
            logging.error(f"Attempt {attempt} failed for {url}: {e}")
            if attempt < retries:
                print(f"[INFO] Retrying in {delay} seconds...")
                time.sleep(delay)
    return None

# ----------------------------
# Fetch Functions
# ----------------------------
def fetch_openphish():
    logging.info("Fetching data from OpenPhish...")
    response = fetch_with_retry(OPENPHISH_URL)
    if response:
        urls = response.text.strip().split('\n')
        logging.info(f"Fetched {len(urls)} URLs from OpenPhish.")
        print(f"[DEBUG] OpenPhish URLs: {len(urls)}")
        return [{"phishing_url": url, "source": "OpenPhish"} for url in urls]
    else:
        logging.error("Failed to fetch OpenPhish data after retries.")
        return []

def fetch_urlhaus():
    logging.info("Fetching data from URLhaus...")
    response = fetch_with_retry(URLHAUS_URL)
    if response:
        try:
            # ✅ Use StringIO for in-memory CSV parsing
            data = pd.read_csv(StringIO(response.text), comment='#')
            urls = [{"phishing_url": row['url'], "source": "URLhaus"} for _, row in data.iterrows()]
            logging.info(f"Fetched {len(urls)} URLs from URLhaus.")
            print(f"[DEBUG] URLhaus URLs: {len(urls)}")
            return urls
        except Exception as e:
            logging.error(f"Error parsing URLhaus CSV: {e}")
            print(f"[ERROR] Could not parse URLhaus CSV: {e}")
            return []
    else:
        logging.error("Failed to fetch URLhaus data after retries.")
        return []

# ----------------------------
# Utility Functions
# ----------------------------
def filter_kenyan_targets(records):
    filtered = [rec for rec in records if rec["phishing_url"] and any(keyword in rec["phishing_url"].lower() for keyword in KENYAN_KEYWORDS)]
    logging.info(f"Filtered {len(filtered)} Kenyan-target URLs from {len(records)} total.")
    print(f"[DEBUG] Kenyan URLs found: {len(filtered)}")
    return filtered

def save_combined_csv(records):
    if not records:
        logging.warning("No records to save.")
        print("[INFO] No data to save.")
        return False
    
    os.makedirs(DATA_DIR, exist_ok=True)
    df = pd.DataFrame(records)
    df['fetched_at'] = datetime.now()
    
    try:
        df.to_csv(OUTPUT_FILE, index=False)
        logging.info(f"Combined data saved to {OUTPUT_FILE}. Total entries: {len(df)}")
        print(f"[+] Data saved: {OUTPUT_FILE}")
        print(f"[+] Total entries: {len(df)}")
        return True
    except Exception as e:
        logging.error(f"Error saving combined data: {e}")
        print(f"[ERROR] Could not save data: {e}")
        return False

# ----------------------------
# Main Execution
# ----------------------------
if __name__ == "__main__":
    all_records = []
    
    # Fetch from both sources
    all_records.extend(fetch_openphish())
    all_records.extend(fetch_urlhaus())
    
    if not all_records:
        print("[ERROR] No data fetched from any source.")
    else:
        # Filter for Kenyan URLs
        kenyan_records = filter_kenyan_targets(all_records)
        
        if kenyan_records:
            print("[INFO] Saving Kenyan-target phishing URLs...")
            save_combined_csv(kenyan_records)
        else:
            print("[INFO] No Kenyan URLs found. Saving ALL URLs instead...")
            save_combined_csv(all_records)
