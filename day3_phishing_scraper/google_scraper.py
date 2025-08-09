from googlesearch import search
import pandas as pd

# Define Google dorks
queries = [
    '"verify your account" + "http"',
    '"Office365 login" + "password"'
]

results = []

for query in queries:
    print(f"[+] Searching for: {query}")
    try:
        for url in search(query, num_results=10):
            print("[+] Found:", url)
            results.append(url)
    except Exception as e:
        print(f"[!] Error during search: {e}")

if results:
    df = pd.DataFrame(results, columns=['URL'])
    df.to_csv('output/google_phishing_urls.csv', index=False)
    print(f"[+] Saved {len(results)} URLs to output/google_phishing_urls.csv")
else:
    print("[!] No results found.")
