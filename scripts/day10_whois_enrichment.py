import pandas as pd
import requests
import os
from urllib.parse import urlparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# ----------------------------
# Config
# ----------------------------
INPUT_FILE = "../data/darkweb_analysis.csv"  # Output from Day 9
OUTPUT_FILE = "../data/whois_enriched.csv"
API_KEY = "YOUR_API_KEY"  # Replace with your WhoisXML API key
API_URL = "https://www.whoisxmlapi.com/whoisserver/WhoisService"
MAX_THREADS = 5  # Don't overload the API
RATE_LIMIT_DELAY = 1  # Seconds between requests
SUSPICIOUS_TLDS = {"app", "xyz", "tk", "top", "gq", "ml"}
FREE_REGISTRARS = ["freenom", "000domains"]

os.makedirs("../data", exist_ok=True)

# ----------------------------
# Helpers
# ----------------------------
def extract_domain(url):
    try:
        parsed = urlparse(url)
        return parsed.netloc.lower()
    except:
        return None

def fetch_whois(domain):
    params = {
        "apiKey": API_KEY,
        "domainName": domain,
        "outputFormat": "JSON"
    }
    try:
        response = requests.get(API_URL, params=params, timeout=15)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"[ERROR] API error for {domain}: {response.status_code}")
            return None
    except Exception as e:
        print(f"[ERROR] Exception fetching WHOIS for {domain}: {e}")
        return None

def analyze_whois(domain, data):
    if not data or "WhoisRecord" not in data:
        return {"registrar": "Unknown", "risk_score": 0, "status": "Failed"}

    registrar = data.get("WhoisRecord", {}).get("registrarName", "Unknown")
    risk_score = 0
    if any(free in registrar.lower() for free in FREE_REGISTRARS):
        risk_score += 50

    tld = domain.split('.')[-1]
    if tld in SUSPICIOUS_TLDS:
        risk_score += 30

    return {"registrar": registrar, "risk_score": risk_score, "status": "Success"}

def process_domain(domain):
    if not domain or ".onion" in domain:
        return {"domain": domain, "registrar": "Skipped", "risk_score": 0, "whois_status": "Skipped", "checked_at": datetime.now()}

    data = fetch_whois(domain)
    analysis = analyze_whois(domain, data)
    time.sleep(RATE_LIMIT_DELAY)  # Respect rate limit
    return {
        "domain": domain,
        "registrar": analysis["registrar"],
        "risk_score": analysis["risk_score"],
        "whois_status": analysis["status"],
        "checked_at": datetime.now()
    }

# ----------------------------
# Main
# ----------------------------
if not os.path.exists(INPUT_FILE):
    print(f"[ERROR] Input file not found: {INPUT_FILE}")
    exit()

print(f"[INFO] Reading domains from {INPUT_FILE}...")
df = pd.read_csv(INPUT_FILE)

# Extract domains from URLs in Day 9 output
urls = df['url'].dropna().tolist()
domains = list(set([extract_domain(url) for url in urls if extract_domain(url)]))

print(f"[INFO] Found {len(domains)} unique domains for WHOIS lookup.")

results = []
with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    futures = {executor.submit(process_domain, domain): domain for domain in domains}
    for future in as_completed(futures):
        results.append(future.result())

# Save results
pd.DataFrame(results).to_csv(OUTPUT_FILE, index=False)
print(f"[+] WHOIS enrichment completed. Data saved to {OUTPUT_FILE}")
print(f"[+] Total domains processed: {len(results)}")
print(f"[+] High-risk domains: {len([r for r in results if r['risk_score'] > 0])}")
