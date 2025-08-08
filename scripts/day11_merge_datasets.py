import pandas as pd
import os

# ✅ Paths
SURFACE_PATH = "../data/combined_phishing_data.csv"
DARKWEB_PATH = "../data/darkweb_analysis.csv"
WHOIS_PATH = "../data/whois_enriched.csv"
OUTPUT_CSV = "../data/unified_threat_dataset.csv"
OUTPUT_JSON = "../data/unified_threat_dataset.json"

def safe_load_csv(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        print(f"[WARN] Missing file: {path}")
        return pd.DataFrame()

# ✅ Load datasets
surface_df = safe_load_csv(SURFACE_PATH)
darkweb_df = safe_load_csv(DARKWEB_PATH)
whois_df = safe_load_csv(WHOIS_PATH)

# ✅ Normalize Surface Web Data
if not surface_df.empty:
    surface_df['source_type'] = 'surface'
    if 'url' not in surface_df.columns:
        print("[WARN] No 'url' column in surface dataset, creating empty one.")
        surface_df['url'] = None
    if 'domain' not in surface_df.columns:
        surface_df['domain'] = surface_df['url'].apply(
            lambda x: x.split("/")[2] if pd.notnull(x) and "://" in x else x
        )
else:
    surface_df = pd.DataFrame(columns=['source_type', 'url', 'domain'])

surface_df = surface_df[['source_type', 'url', 'domain']]

# ✅ Normalize Dark Web Data
if not darkweb_df.empty:
    darkweb_df['source_type'] = 'darkweb'
    # Rename if needed
    if 'onion_url' in darkweb_df.columns:
        darkweb_df.rename(columns={'onion_url': 'url'}, inplace=True)
    elif 'url' not in darkweb_df.columns:
        darkweb_df['url'] = None

    if 'domain' not in darkweb_df.columns:
        darkweb_df['domain'] = None

    if 'risk_score' not in darkweb_df.columns:
        darkweb_df['risk_score'] = 0
else:
    darkweb_df = pd.DataFrame(columns=['source_type', 'url', 'domain', 'risk_score'])

darkweb_df = darkweb_df[['source_type', 'url', 'domain', 'risk_score']]

# ✅ Normalize WHOIS Data
if not whois_df.empty:
    whois_df['source_type'] = 'whois'
    if 'domain' not in whois_df.columns:
        whois_df['domain'] = None
else:
    whois_df = pd.DataFrame(columns=['source_type', 'domain'])

whois_df = whois_df[['source_type', 'domain']]

# ✅ Merge all data
unified_df = pd.concat([surface_df, darkweb_df, whois_df], ignore_index=True)

# ✅ Save unified dataset
unified_df.to_csv(OUTPUT_CSV, index=False)
unified_df.to_json(OUTPUT_JSON, orient='records')

print("\n[+] Unified dataset created:")
print(f"    - {OUTPUT_CSV}")
print(f"    - {OUTPUT_JSON}")
print(f"Total records: {len(unified_df)}")
print(f"Unique domains: {unified_df['domain'].nunique()}")
print(f"Surface count: {len(surface_df)}")
print(f"Darkweb count: {len(darkweb_df)}")
print(f"WHOIS count: {len(whois_df)}")
