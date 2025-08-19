import requests
from bs4 import BeautifulSoup
from googlesearch import search
import pandas as pd
import re
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

OUTPUT_DIR = "output"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Headers to avoid bot detection
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0 Safari/537.36"
}

# Session with retry
session = requests.Session()
retry = Retry(total=3, backoff_factor=2, status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount("http://", adapter)
session.mount("https://", adapter)


def scrape_google():
    google_queries = [
        '"verify your account" + "http"',
        '"Office365 login" + "password"'
    ]
    results = []

    print("[+] Starting Google scraping...")
    for query in google_queries:
        print(f"[+] Searching for: {query}")
        try:
            for url in search(query, num_results=10):
                print("[Google] Found:", url)
                results.append(url)
        except Exception as e:
            print("[!] Google scraping error:", e)

    out_file = os.path.join(OUTPUT_DIR, "google_phishing_urls.csv")
    pd.DataFrame(results, columns=['URL']).to_csv(out_file, index=False)
    print(f"[+] Google URLs saved to {out_file}")
    return results


def scrape_pastebin():
    pastebin_url = 'https://pastebin.com/archive'
    pattern = re.compile(r'(https?://[^\s]+)')
    results = []

    print("[+] Fetching Pastebin archive...")
    try:
        res = session.get(pastebin_url, headers=HEADERS, timeout=10)
        res.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[!] Failed to fetch Pastebin archive: {e}")
        return results  # graceful fallback

    soup = BeautifulSoup(res.text, 'html.parser')
    paste_links = [a['href'] for a in soup.select('a') if a.get('href', '').startswith('/')]
    full_links = ['https://pastebin.com' + link for link in paste_links if len(link) > 1]

    print(f"[+] Found {len(full_links)} paste links. Checking first 10...")
    for link in full_links[:10]:
        try:
            paste = session.get(link, headers=HEADERS, timeout=10)
            paste.raise_for_status()
            urls = pattern.findall(paste.text)
            if urls:
                for u in urls:
                    print("[Pastebin] Found:", u)
                    results.append(u)
        except requests.exceptions.RequestException as e:
            print(f"[!] Error fetching {link}: {e}")

    out_file = os.path.join(OUTPUT_DIR, "pastebin_phishing_urls.csv")
    pd.DataFrame(results, columns=['URL']).to_csv(out_file, index=False)
    print(f"[+] Pastebin URLs saved to {out_file}")
    return results


def merge_results(google_results, pastebin_results):
    all_urls = sorted(set(google_results + pastebin_results))
    out_file = os.path.join(OUTPUT_DIR, "all_phishing_urls.csv")
    pd.DataFrame(all_urls, columns=['URL']).to_csv(out_file, index=False)
    print(f"[+] All URLs merged into {out_file}")


if __name__ == "__main__":
    google_results = scrape_google()
    pastebin_results = scrape_pastebin()
    merge_results(google_results, pastebin_results)
