import requests
import pandas as pd
import os
from datetime import datetime
import logging

# ----------------------------
# Configuration
# ----------------------------
OPENPHISH_URL = "https://raw.githubusercontent.com/openphish/public_feed/refs/heads/main/feed.txt"
DATA_DIR = "../data"
LOG_DIR = "../logs"
OUTPUT_FILE = os.path.join(DATA_DIR, "openphish_data.csv")
LOG_FILE = os.path.join(LOG_DIR, "openphish.log")

# Keywords for Kenyan targets
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
# Functions
# ----------------------------
def fetch_openphish_data():
    """
    Fetch phishing URLs from OpenPhish feed and return as a list.
    """
    logging.info("Starting fetch from OpenPhish...")
    try:
        response = requests.get(OPENPHISH_URL, timeout=15)
        response.raise_for_status()
        urls = response.text.strip().split('\n')
        logging.info(f"Successfully fetched {len(urls)} URLs from OpenPhish.")
        print(f"[DEBUG] Total URLs fetched: {len(urls)}")
        return urls
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching OpenPhish data: {e}")
        print(f"[ERROR] Could not fetch data: {e}")
        return []

def filter_kenyan_targets(urls):
    """
    Filter URLs for Kenyan financial targets (CBK, M-PESA, .ke domains).
    """
    filtered = [url for url in urls if any(keyword in url.lower() for keyword in KENYAN_KEYWORDS)]
    logging.info(f"Filtered {len(filtered)} URLs matching Kenyan targets from {len(urls)} total URLs.")
    print(f"[DEBUG] Kenyan URLs found: {len(filtered)}")
    return filtered

def save_to_csv(urls, source="OpenPhish"):
    """
    Save URLs to a CSV file with metadata.
    """
    if not urls:
        logging.warning("No URLs to save.")
        print("[INFO] No URLs to save. Skipping CSV write.")
        return False
    
    os.makedirs(DATA_DIR, exist_ok=True)
    df = pd.DataFrame(urls, columns=["phishing_url"])
    df['source'] = source
    df['fetched_at'] = datetime.now()
    
    try:
        df.to_csv(OUTPUT_FILE, index=False)
        logging.info(f"Data saved to {OUTPUT_FILE}. Total entries: {len(df)}")
        print(f"[+] Data saved: {OUTPUT_FILE}")
        print(f"[+] Total phishing URLs collected: {len(df)}")
        return True
    except Exception as e:
        logging.error(f"Error saving data: {e}")
        print(f"[ERROR] Could not save data: {e}")
        return False

# ----------------------------
# Main Execution
# ----------------------------
if __name__ == "__main__":
    urls = fetch_openphish_data()
    if urls:
        kenyan_urls = filter_kenyan_targets(urls)
        
        # Toggle behavior: Save Kenyan URLs if available; otherwise save all
        if kenyan_urls:
            print("[INFO] Saving Kenyan URLs only...")
            save_to_csv(kenyan_urls)
        else:
            print("[INFO] No Kenyan URLs found. Saving ALL URLs instead.")
            save_to_csv(urls)
