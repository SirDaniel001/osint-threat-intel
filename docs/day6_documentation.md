# 📄 Day 6 – Advanced Feed Automation & Reporting

---

## ✅ Purpose
Enhance threat intelligence data collection by:
- Integrating multiple phishing feeds
- Automating pipeline from **data fetch → cleaning → reporting**
- Generating **professional PDF reports**
- Implementing **email delivery** for reports

---

## 🔍 Why This Step is Important
- Expands OSINT coverage (OpenPhish + URLhaus)
- Increases reliability & volume of phishing indicators
- Adds **error handling & retry logic**
- Enables **fully automated reporting & distribution**

---

## ✅ Objectives Completed
✔ Integrated **OpenPhish + URLhaus** feeds  
✔ Implemented **retry logic** for feed fetching  
✔ Created **Kenyan phishing filter**  
✔ Built **Day 6 Test Runner** for automation  
✔ Generated **PDF report** (TLD chart + Top Domains)  
✔ Enabled **email sending with Gmail SMTP**

---

## ✅ Implementation Details

### **1. Combined Feed Script**
**File:** `scripts/phishing_feeds_combined.py`

- Fetches from **OpenPhish (TXT)** & **URLhaus (CSV)**
- Auto-detects `url` column in CSV
- Handles failures with **retry logic**
- Saves combined data → `data/combined_phishing_data.csv`
- Logs to → `logs/combined_feeds.log`

**Output:**
