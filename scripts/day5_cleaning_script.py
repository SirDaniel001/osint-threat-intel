import pandas as pd
import os
import logging
from urllib.parse import urlparse
from datetime import datetime

# ----------------------------
# Config
# ----------------------------
INPUT_FILE = "../data/combined_phishing_data.csv"
OUTPUT_FILE = "../data/cleaned_phishing_data.csv"
LOG_FILE = "../logs/day5_cleaning.log"
KENYAN_ONLY = False  # Set to True if you want only .ke domains or Kenyan keywords

# Setup logging
os.makedirs("../logs", exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def is_valid_url(url):
    """Basic validation: Check if URL has scheme and netloc"""
    try:
        parsed = urlparse(url)
        return all([parsed.scheme, parsed.netloc])
    except:
        return False

def extract_tld(domain):
    """Extract Top-Level Domain from domain name"""
    return domain.split('.')[-1] if '.' in domain else ''

def clean_and_process_data():
    # Load data
    if not os.path.exists(INPUT_FILE):
        print(f"[ERROR] Input file not found: {INPUT_FILE}")
        return
    
    print("[INFO] Loading data...")
    df = pd.read_csv(INPUT_FILE)
    logging.info(f"Loaded {len(df)} records from {INPUT_FILE}")
    
    # Remove duplicates
    df.drop_duplicates(subset=["phishing_url"], inplace=True)
    logging.info(f"After removing duplicates: {len(df)} rows")
    
    # Normalize URLs (strip spaces, lowercase)
    df["phishing_url"] = df["phishing_url"].astype(str).str.strip().str.lower()
    
    # Validate URLs
    df = df[df["phishing_url"].apply(is_valid_url)]
    logging.info(f"After URL validation: {len(df)} rows")
    
    # Extract domain & TLD
    df["domain"] = df["phishing_url"].apply(lambda x: urlparse(x).netloc)
    df["tld"] = df["domain"].apply(extract_tld)
    
    # Apply Kenyan filter if enabled
    if KENYAN_ONLY:
        df = df[df["tld"] == "ke"]
        logging.info(f"After Kenyan filter: {len(df)} rows")
    
    # Add cleaning timestamp
    df["cleaned_at"] = datetime.now()
    
    # Save cleaned data
    os.makedirs("../data", exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    logging.info(f"Cleaned data saved to {OUTPUT_FILE}")
    
    # Summary
    print("\n[SUMMARY]")
    print(f"Total valid records: {len(df)}")
    print(f"Unique domains: {df['domain'].nunique()}")
    print("\nTop 5 Domains:")
    print(df['domain'].value_counts().head(5))
    print("\nTLD Distribution:")
    print(df['tld'].value_counts())
    
    logging.info("Summary generated.")
    logging.info(f"Top 5 domains:\n{df['domain'].value_counts().head(5)}")
    logging.info(f"TLD distribution:\n{df['tld'].value_counts()}")
    
    print(f"\n[+] Cleaned data saved: {OUTPUT_FILE}")
    print(f"[+] Log file: {LOG_FILE}")

if __name__ == "__main__":
    clean_and_process_data()
