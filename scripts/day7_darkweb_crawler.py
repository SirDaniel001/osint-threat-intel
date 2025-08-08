import requests
import csv
import os
import time
import random
from datetime import datetime
from stem import Signal
from stem.control import Controller
import logging

# ----------------------------
# Configurations
# ----------------------------
TOR_SOCKS_PROXY = "socks5h://127.0.0.1:9050"
CONTROL_PORT = 9051
DATA_DIR = "../data"
LOG_DIR = "../logs"
OUTPUT_FILE = os.path.join(DATA_DIR, "darkweb_data.csv")
LOG_FILE = os.path.join(LOG_DIR, "darkweb.log")
ONION_FILE = os.path.join(DATA_DIR, "darkweb_sites.txt")

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Logging setup
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Proxy settings
proxies = {'http': TOR_SOCKS_PROXY, 'https': TOR_SOCKS_PROXY}

# ----------------------------
# Helper Functions
# ----------------------------
def get_current_ip():
    try:
        ip = requests.get("https://httpbin.org/ip", proxies=proxies, timeout=10).json()['origin']
        logging.info(f"Current Tor IP: {ip}")
        return ip
    except:
        logging.warning("Could not fetch current IP")
        return "Unknown"

def renew_identity():
    with Controller.from_port(port=CONTROL_PORT) as controller:
        controller.authenticate()  # Using cookie authentication
        controller.signal(Signal.NEWNYM)
    logging.info("Tor identity rotated successfully.")
    time.sleep(5)  # Wait for new circuit

def load_onion_sites():
    if not os.path.isfile(ONION_FILE):
        logging.error(f"Onion list file not found: {ONION_FILE}")
        return []
    with open(ONION_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

def crawl_site(url):
    retries = 3
    for attempt in range(1, retries + 1):
        try:
            ip = get_current_ip()
            logging.info(f"[{ip}] Crawling attempt {attempt}: {url}")
            response = requests.get(url, proxies=proxies, timeout=30)
            status = response.status_code
            logging.info(f"Status {status} for {url}")
            return status
        except requests.RequestException as e:
            logging.warning(f"Attempt {attempt} failed for {url}: {e}")
            time.sleep(5)
    return "ERROR"

def crawl_all_sites():
    results = []
    sites = load_onion_sites()
    if not sites:
        print("[ERROR] No onion sites found. Add URLs to darkweb_sites.txt")
        return []

    for idx, site in enumerate(sites):
        status = crawl_site(site)
        results.append([site, status, datetime.now()])

        # Random delay to mimic human browsing
        delay = random.randint(5, 15)
        logging.info(f"Sleeping for {delay} seconds before next request...")
        time.sleep(delay)

        # Rotate identity every 2 sites
        if (idx + 1) % 2 == 0:
            renew_identity()

    return results

def save_results(results):
    file_exists = os.path.isfile(OUTPUT_FILE)
    with open(OUTPUT_FILE, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["onion_url", "status", "timestamp"])
        writer.writerows(results)
    logging.info(f"Results saved to {OUTPUT_FILE}")

# ----------------------------
# Main Execution
# ----------------------------
if __name__ == "__main__":
    logging.info("Day 7 Enhanced Dark Web Crawler started.")
    data = crawl_all_sites()
    if data:
        save_results(data)
        print(f"[+] Crawling complete. Results saved in {OUTPUT_FILE}")
        print(f"[+] Log file: {LOG_FILE}")

