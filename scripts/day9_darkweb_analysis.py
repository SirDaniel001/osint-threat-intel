import requests
from bs4 import BeautifulSoup
from stem import Signal
from stem.control import Controller
import random
import time
import pandas as pd
from datetime import datetime
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse, parse_qs

# ----------------------------
# Tor Proxy Settings
# ----------------------------
PROXIES = {"http": "socks5h://127.0.0.1:9050", "https": "socks5h://127.0.0.1:9050"}
STATIC_ONION_SITES = [
    "http://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion"
]
AHMIA_URL = "https://ahmia.fi/search/?q=banking"
RESULT_LIMIT = 50  # Limit number of onion links to process

# Weighted keywords
KEYWORD_WEIGHTS = {
    r"\bcbk\b": 150,
    r"central bank of kenya": 150,
    r"m[-\s]?pesa": 120,
    r"\.ke": 50
}

OUTPUT_FILE = "../data/darkweb_analysis.csv"
MAX_THREADS = 5
MAX_RETRIES = 3

# ----------------------------
# Rotate Tor IP
# ----------------------------
def renew_identity():
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
        print("[INFO] Tor identity rotated.")
        time.sleep(5)
    except Exception as e:
        print(f"[ERROR] Failed to rotate Tor identity: {e}")

# ----------------------------
# Fetch dynamic onion links from Ahmia
# ----------------------------
def fetch_dynamic_onion_sites():
    print("[INFO] Fetching fresh onion links from Ahmia...")
    try:
        response = requests.get(AHMIA_URL, timeout=20)
        soup = BeautifulSoup(response.text, "html.parser")
        raw_links = [a["href"] for a in soup.find_all("a", href=True) if ".onion" in a["href"]]

        onion_domains = []
        for link in raw_links:
            # Extract actual onion URL
            if "redirect_url=" in link:
                parsed = parse_qs(urlparse(link).query)
                if "redirect_url" in parsed:
                    url = parsed["redirect_url"][0]
                else:
                    continue
            else:
                url = link

            # Extract root domain only
            parsed_url = urlparse(url)
            domain = parsed_url.scheme + "://" + parsed_url.hostname
            onion_domains.append(domain)

        # Deduplicate and limit results
        onion_domains = list(set(onion_domains))[:RESULT_LIMIT]
        print(f"[INFO] Extracted {len(onion_domains)} unique onion root URLs.")
        return onion_domains
    except Exception as e:
        print(f"[ERROR] Could not fetch Ahmia links: {e}")
        return []

# ----------------------------
# Analyze content
# ----------------------------
def analyze_content(text):
    found_keywords = []
    threat_score = 0
    lower_text = text.lower()

    for kw, weight in KEYWORD_WEIGHTS.items():
        if re.search(kw, lower_text):
            found_keywords.append(kw)
            threat_score += weight

    return found_keywords if found_keywords else None, threat_score

# ----------------------------
# Fetch URL with retries
# ----------------------------
def fetch_url(url):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"[INFO] Attempt {attempt}/{MAX_RETRIES} for {url}")
            response = requests.get(url, proxies=PROXIES, timeout=30)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                text = soup.get_text(separator=" ")
                keywords_found, score = analyze_content(text)
                return [url, "200", keywords_found, score, datetime.now()]
            else:
                print(f"[WARN] Non-200 response from {url}: {response.status_code}")
                return [url, response.status_code, None, 0, datetime.now()]
        except Exception as e:
            print(f"[ERROR] {url} failed on attempt {attempt}: {e}")
            if attempt < MAX_RETRIES:
                print("[INFO] Rotating Tor identity and retrying...")
                renew_identity()
                time.sleep(random.randint(5, 10))
            else:
                print(f"[FAIL] Max retries reached for {url}")
                return [url, "error", None, 0, datetime.now()]

# ----------------------------
# Crawl Sites (Multi-threaded)
# ----------------------------
def crawl_sites(onion_sites):
    records = []
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = {executor.submit(fetch_url, url): url for url in onion_sites}
        for future in as_completed(futures):
            records.append(future.result())

    print("[INFO] Rotating Tor identity after batch...")
    renew_identity()
    return records

# ----------------------------
# Save Results
# ----------------------------
def save_results(records):
    df = pd.DataFrame(records, columns=["url", "status", "keywords_found", "threat_score", "crawled_at"])
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"[+] Analysis complete. Results saved to {OUTPUT_FILE}")

# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    print("[INFO] Starting optimized dark web analysis...")
    dynamic_links = fetch_dynamic_onion_sites()
    all_sites = STATIC_ONION_SITES + dynamic_links
    print(f"[INFO] Total onion sites to analyze: {len(all_sites)}")
    data = crawl_sites(all_sites)
    save_results(data)

    # Summary
    total = len(data)
    success = sum(1 for r in data if r[1] == "200")
    print(f"[SUMMARY] Total: {total}, Success: {success}, Errors: {total - success}")
