import requests
from bs4 import BeautifulSoup
import random
import time
import os
import csv
import logging
from datetime import datetime
from stem import Signal
from stem.control import Controller

# ----------------------------
# Configurations
# ----------------------------
TOR_PROXY = "socks5h://127.0.0.1:9050"
URL_LIST_FILE = "../data/darkweb_sites.txt"
OUTPUT_FILE = "../data/darkweb_analysis.csv"
LOG_FILE = "../logs/day8_darkweb_analysis.log"
CONTROL_PORT = 9051
KEYWORDS = ["mpesa", "cbk", "equity", "kcb", "kenya", "carding", "bank", "paypal", "atm dump"]

os.makedirs("../logs", exist_ok=True)
os.makedirs("../data", exist_ok=True)

# Logging setup
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# ----------------------------
# Tor Identity Rotation
# ----------------------------
def rotate_identity():
    try:
        with Controller.from_port(port=CONTROL_PORT) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
            logging.info("Rotated Tor identity.")
            time.sleep(5)
    except Exception as e:
        logging.error(f"Failed to rotate identity: {e}")

# ----------------------------
# Fetch Onion Page
# ----------------------------
def fetch_page(url):
    try:
        response = requests.get(url, proxies={"http": TOR_PROXY, "https": TOR_PROXY}, timeout=30)
        return response.status_code, response.text
    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")
        return None, None

# ----------------------------
# Analyze Page Content
# ----------------------------
def analyze_content(html):
    if not html:
        return [], 0
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text().lower()
    found_keywords = [kw for kw in KEYWORDS if kw in text]
    score = (len(found_keywords) * 10)
    return found_keywords, score

# ----------------------------
# Main Execution
# ----------------------------
def main():
    if not os.path.exists(URL_LIST_FILE):
        print(f"[ERROR] URL list file not found: {URL_LIST_FILE}")
        return
    
    with open(URL_LIST_FILE, "r") as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]

    results = []
    for idx, url in enumerate(urls, 1):
        print(f"[INFO] Crawling ({idx}/{len(urls)}): {url}")
        logging.info(f"Crawling: {url}")
        
        status, html = fetch_page(url)
        found_keywords, keyword_score = analyze_content(html)
        threat_score = keyword_score + (200 if status == 200 else 0)
        
        results.append({
            "url": url,
            "status": status if status else "error",
            "keywords_found": ",".join(found_keywords) if found_keywords else "None",
            "threat_score": threat_score,
            "crawled_at": datetime.now()
        })

        # Save progress incrementally
        with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["url", "status", "keywords_found", "threat_score", "crawled_at"])
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(results[-1])
        
        # Rotate IP every 2 requests
        if idx % 2 == 0:
            rotate_identity()
        
        # Random delay (8–15s)
        time.sleep(random.randint(8, 15))

    print(f"[+] Analysis complete. Results saved to {OUTPUT_FILE}")
    logging.info(f"Analysis complete. {len(results)} records processed.")

if __name__ == "__main__":
    main()
