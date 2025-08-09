import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

base_url = 'https://pastebin.com/archive'
url_pattern = re.compile(r'(https?://[^\s]+)')

print("[+] Fetching Pastebin archive...")
response = requests.get(base_url)

if response.status_code != 200:
    print("[!] Failed to fetch Pastebin archive.")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')
paste_links = [a['href'] for a in soup.select('a') if a.get('href', '').startswith('/')]
full_links = ['https://pastebin.com' + link for link in paste_links if len(link) > 1]

results = []

print(f"[+] Found {len(full_links)} paste links. Checking each...")
for link in full_links[:10]:  # Limit to first 10 for demo
    paste = requests.get(link)
    urls = url_pattern.findall(paste.text)
    if urls:
        for u in urls:
            results.append(u)
            print(f"[+] Found URL: {u}")

if results:
    df = pd.DataFrame(results, columns=['URL'])
    df.to_csv('output/pastebin_phishing_urls.csv', index=False)
    print(f"[+] Saved {len(results)} URLs to output/pastebin_phishing_urls.csv")
else:
    print("[!] No URLs found in Pastebin pastes.")
