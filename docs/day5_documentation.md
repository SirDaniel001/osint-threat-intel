# 📄 Day 5 – Data Cleaning & Automated Reporting

---

## ✅ Purpose
To clean the collected phishing data, extract valuable metadata, generate actionable visual reports, and automate email delivery of these reports while ensuring credential security.

---

## ✅ Why This Step is Important
- Improves **data quality** by removing duplicates and invalid URLs.
- Extracts **domain names** and **TLDs** for better analytics.
- Automates **threat intelligence reporting** for quick analyst access.
- Secures **sensitive credentials** using `.env`.

---

## ✅ Tasks Completed

### ✔ 1. Data Cleaning
- Script: `scripts/day5_cleaning_script.py`
- Actions performed:
  - Removed duplicates and invalid URLs.
  - Normalized URLs (lowercase, stripped spaces).
  - Extracted `domain` and `tld`.
  - Added `cleaned_at` timestamp.
- Output:  
  ✅ `data/cleaned_phishing_data.csv`

**Sample Code:**
```python
def clean_data():
    df = pd.read_csv("../data/combined_phishing_data.csv")
    df.drop_duplicates(subset=["phishing_url"], inplace=True)
    df = df[df["phishing_url"].apply(is_valid_url)]
    df["domain"] = df["phishing_url"].apply(lambda x: urlparse(x).netloc)
    df["tld"] = df["domain"].apply(extract_tld)
    df["cleaned_at"] = datetime.now()
    df.to_csv("../data/cleaned_phishing_data.csv", index=False)
