import pandas as pd
import tldextract
import os

input_file = "output/all_phishing_urls.csv"
output_file = "output/clean_phishing_domains.csv"

if not os.path.exists(input_file):
    print(f"[!] Input file {input_file} not found.")
    exit()

df = pd.read_csv(input_file)

domains = set()
for url in df['URL']:
    ext = tldextract.extract(str(url))
    if ext.domain and ext.suffix:
        domain = f"{ext.domain}.{ext.suffix}"
        domains.add(domain)

# Save unique domains
cleaned_domains = sorted(domains)
pd.DataFrame(cleaned_domains, columns=['Domain']).to_csv(output_file, index=False)

print(f"[+] Extracted {len(cleaned_domains)} unique domains.")
print(f"[+] Clean domains saved to {output_file}")
