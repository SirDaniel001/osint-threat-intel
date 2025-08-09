import requests
from bs4 import BeautifulSoup
from googlesearch import search
import pandas as pd
import re
import os

# Create output folder if it doesn't exist
if not os.path.exists("output"):
    os.makedirs("output")

# ============ GOOGLE SCRAPER ============
google_queries = [
    '"verify your account" + "http"',
    '"Office365 login" + "password"'
]
google_results = []

print("[+] Starting Google scraping...")
for query in google_queries:
    print(f"[+] Searching for: {query}")
    try:
        for url in search(query, num_results=10):
            print("[Google] Found:", url)
            google_results.append(url)
    except Exception as e:
        print("[!] Google scraping error:", e)

google_csv = "output/google_phishing_urls.csv"
pd.DataFrame(google_results, columns=['URL']).to_csv(google_csv, index=False)
print(f"[+] Google URLs saved to {google_csv}")

# ============ PASTEBIN SCRAPER ============
pastebin_url = 'https://pastebin.com/archive'
pattern = re.compile(r'(https?://[^\s]+)')

print("[+] Fetching Pastebin archive...")
res = requests.get(pastebin_url)
pastebin_results = []

if res.status_code == 200:
    soup = BeautifulSoup(res.text, 'html.parser')
    paste_links = [a['href'] for a in soup.select('a') if a.get('href', '').startswith('/')]
    full_links = ['https://pastebin.com' + link for link in paste_links if len(link) > 1]

    print(f"[+] Found {len(full_links)} paste links. Checking first 10...")
    for link in full_links[:10]:
        paste = requests.get(link)
        urls = pattern.findall(paste.text)
        if urls:
            for u in urls:
                print("[Pastebin] Found:", u)
                pastebin_results.append(u)

pastebin_csv = "output/pastebin_phishing_urls.csv"
pd.DataFrame(pastebin_results, columns=['URL']).to_csv(pastebin_csv, index=False)
print(f"[+] Pastebin URLs saved to {pastebin_csv}")

# ============ MERGE ============
all_urls = list(set(google_results + pastebin_results))
merged_csv = "output/all_phishing_urls.csv"
pd.DataFrame(all_urls, columns=['URL']).to_csv(merged_csv, index=False)
print(f"[+] All URLs merged into {merged_csv}")
