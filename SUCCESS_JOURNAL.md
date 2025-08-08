# 🚀 Success Journal – OSINT Threat Intelligence Project

![Project Banner](data/data_banner.png)

---

## ✅ Day 6 – July 30, 2025
**Summary:**  
"Today, I automated an OSINT pipeline that fetches phishing data from multiple sources, cleans it, generates a professional report with charts, and emails it automatically—pushing my project to enterprise-level standards. Each script I wrote today is a building block toward a fully automated threat intelligence system, proving that consistency creates real innovation."  

— **@SirDaniel 💻✨**

---

### ✅ Key Achievements:
- Integrated **OpenPhish + URLhaus** feeds with retry logic
- Built automated **OSINT pipeline runner**
- Generated **Day 6 PDF Report**:
  - Threat summary table
  - IOC distribution chart
- Implemented **automated email delivery** for reports
- Updated **README.md** and created **Day 6 documentation**

---

🔥 **Next Milestone:**  
**Day 7 – Dark Web Crawler Setup (Tor Integration)**  

---

## ✅ Day 7 – July 31, 2025
**Summary:**  
"Day 7 was a major leap forward! I successfully integrated **Tor**, implemented **IP rotation with Stem**, and built a **Dark Web crawler** capable of navigating onion sites safely, with random delays and retry logic. I even automated a **PDF report with charts and email delivery**, transforming my project into a true OSINT powerhouse."  

— **@SirDaniel 🔐🌐**

---

### ✅ Key Achievements:
- Installed and configured **Tor** on Kali
- Enabled **ControlPort 9051** for Stem integration
- Implemented **Tor identity rotation** for anonymity
- Built **Dark Web crawler** with:
  - Onion site crawling via Tor proxy
  - Random delays and retry logic
  - IP rotation after every 2 sites
- Generated **Day 7 PDF Report**:
  - Summary table and status distribution chart
- Automated **email delivery** of the PDF report
- Updated **README.md** and created **Day 7 documentation**

---

🔥 **Next Milestone:**  
**Day 8 – Advanced Dark Web Analysis (Keyword Extraction + Threat Scoring)**  

---

## ✅ Day 8 – August 1, 2025
**Summary:**  
"Day 8 was a turning point! I transformed the Dark Web crawler into an **intelligent analysis engine** by adding keyword detection and a threat scoring system. Now, my OSINT workflow not only gathers data but also **prioritizes threats automatically**, making it closer to a professional-grade platform."  

— **@SirDaniel 🔍🕵♂**

---

### ✅ Key Achievements:
- Implemented **keyword extraction** for high-risk terms
- Built a **threat scoring system** for prioritization
- Enhanced crawler to generate **structured CSV output**
- Created **Day 8 PDF Report**:
  - Keyword frequency chart
  - Threat score distribution chart
- Automated **email delivery** of reports
- Updated **README.md** and started **Day 8 documentation**

---

🔥 **Next Milestone:**  
**Day 9 – Dark Web Search Automation + PDF Report**  

---

## ✅ Day 9 – August 2, 2025
**Summary:**  
"Today, I advanced my Dark Web analysis pipeline by **automating multi-site crawling**, adding **keyword-based threat scoring**, and generating a **professional PDF report** complete with summary tables and charts. I’ve now integrated **email delivery** into this pipeline, making the system almost production-ready for OSINT threat monitoring."  

— **@SirDaniel 🌑🔍**

---

### ✅ Key Achievements:
- Expanded crawler with **5+ .onion URLs**
- Improved **keyword detection & scoring**
- Automated **Tor identity rotation** during crawling
- Generated **Day 9 PDF report**:
  - Keyword frequency chart
  - Threat score distribution
  - Summary stats
- Automated **email delivery** of report
- Updated **README.md** and created **Day 9 documentation**

---

🔥 **Next Milestone:**  
**Day 10 – WHOIS Enrichment + IOC Tagging + Full Pipeline Integration**  

---

## ✅ Day 10 – August 4, 2025
**Summary:**  
"Day 10 was a breakthrough for intelligence correlation! I integrated **WHOIS enrichment**, **IOC tagging**, and **threat feed export** into my dark web pipeline. Now, the system extracts onion data, pulls WHOIS info for linked domains, assigns risk scores, tags with IOCs like `phishing` and `offline_onion`, and generates a **professional PDF report** with charts, an **interactive dashboard**, and even **emails the report automatically**. This is a huge step toward a fully automated Threat Intelligence platform!"  

— **@SirDaniel 🌍🔐📊**

---

### ✅ Key Achievements:
- Implemented **WHOIS enrichment** using WhoisXML API
- Added **risk scoring system**:
  - Free registrars → +50 points
  - Suspicious TLDs (.xyz, .tk, .app) → +30 points
- Built **IOC tagging** for:
  - `phishing`
  - `banking_fraud`
  - `free_domain_risk`
  - `offline_onion` for unreachable onion sources
- Exported **Threat Feeds**:
  - CSV + JSON for SIEM/TIP integration
- Combined Day 9 + Day 10 into **one advanced pipeline**:
  - Onion crawling → keyword detection → WHOIS enrichment → IOC tagging → Reporting
- Generated **interactive HTML dashboard** with Plotly
- Automated **email delivery of PDF report**
- Updated **README.md** and created **Day 10 documentation**

---

🔥 **Next Milestone:**  
**Day 11 – Unified Dataset + Interactive Dashboard + Docker Integration**  

---

## ✅ Day 11 – August 5, 2025
**Summary:**  
"Day 11 was a game-changer! I consolidated all threat data into a unified dataset, built a real-time interactive dashboard using Dash & Plotly, and containerized the entire OSINT pipeline with Docker for portability. This setup is enterprise-ready, scalable, and easy to deploy on any infrastructure. It’s no longer a project—it’s a full-fledged platform!"  

— **@SirDaniel ⚡🐳**

---

### ✅ Key Achievements:
- Created **Unified Dataset**:
  - Combined phishing feeds, dark web analysis, and WHOIS data
  - Exported to **CSV & JSON** for sharing
- Built **Interactive Dashboard**:
  - Risk score charts
  - IOC tag distribution
  - Source type breakdown
  - CSV download option for analysts
- **Dockerized** the entire OSINT pipeline:
  - Included Tor + OSINT scripts inside a secure container
  - Added `entrypoint.sh` with modes:
    - `dashboard` → Start dashboard
    - `fast` → Merge + Dashboard
    - `both` → Full pipeline + Dashboard
- Fixed **PySocks** issue for Tor requests
- Mounted `data/` for persistence
- Exposed ports:
  - `8050` for Dashboard
  - `9050` for Tor SOCKS Proxy
- Deliverables:
  - `scripts/day11_merge_datasets.py`
  - `scripts/day11_dashboard.py`
  - `Dockerfile + entrypoint.sh`
  - `data/unified_threat_dataset.csv`
  - `data/unified_threat_dataset.json`

---

🔥 **Next Milestone:**  
**Day 12 – Authentication for Dashboard + MISP Integration**  

---

## ✅ Day 12 – August 6, 2025
**Summary:**  
"Day 12 was all about laying the foundation for structured and queryable OSINT data storage. I created an **SQLite database** for threat intelligence, designed an optimized schema for Indicators of Compromise (IOCs), and implemented robust Python scripts for **database creation and test insertion**. Verified everything works perfectly and documented every step—setting the stage for automated ingestion on Day 13."  

— **@SirDaniel 🗄️📊**

---

### ✅ Key Achievements:
- Activated **Python virtual environment**
- Installed essential packages:
  ```bash
  pip install requests pandas python-telegram-bot rich
📅 Day 13 – August 7, 2025
Summary:
"Day 13 was all about data ingestion. I connected my OSINT scripts to phishing feeds like OpenPhish, URLhaus, and PhishTank and parsed them into my new database. It’s no longer just about collecting data — it's structured, searchable, and ready for threat correlation. Automation is now alive in the intelligence layer."

— @SirDaniel 🐍📥🛡
✅ Key Achievements:
Connected to:

OpenPhish (CSV), URLhaus (CSV), PhishTank (JSON)

Parsed, cleaned, and extracted relevant phishing indicators

Mapped fields to database schema:

Source, Threat Type, Indicator, Description, Date Detected

Stored data into osint_threats.db using ingestion script

Verified new entries using:


## 📅 Day 13 – Feed Ingestion & Storage
✔ Automated ingestion from multiple feeds (Twitter, OpenPhish, Abuse.ch)  
✔ Added multiple threat entries to `osint_threats.db`  
✔ Validated ingestion using queries  
✔ Wrote `day13_pdf_report.py` with stats and charts  
✔ Emailed PDF report to danielmuteti590@gmail.com  
✔ Updated `README.md` and `SUCCESS_JOURNAL.md`

---

## 📅 Day 14 – Threat Search, Query, and Export
✔ Built `search_threats.py` CLI tool with `argparse`  
✔ Supported filters:
  - `--keyword`
  - `--source`
  - `--threat_type`
  - `--from-date` and `--to-date`
  - `--min-confidence`
  - `--export` to CSV/JSON
  - `--sort-by`, `--desc`
✔ Validated CLI with real database queries  
✔ Exported matching results to:
  - `../results/search_results_day14.csv`
  - `../results/search_results_day14.json`
✔ Built `day14_pdf_report.py` summarizing search stats  
✔ PDF generated & emailed successfully  
✔ Updated `README.md` and `SUCCESS_JOURNAL.md`

---

📅 Day 15 – Telegram Alert Bot Integration & Automation
✔ Connected @PhishingAlertBot to the local SQLite database
✔ Developed telegram_alert.py to:

Periodically scan for new threats

Send real-time alerts to Telegram users
✔ Alert structure includes:

Source

Threat Type

Indicator

Description

Detection Date

Confidence Score
✔ Tested script:

3 phishing/malware alerts successfully delivered to Telegram
✔ Built improved PDF report via day15_pdf1_report.py
## 🧠 Learnings So Far
- Efficient SQL querying with filters
- CLI interface with argparse
- PDF reports with FPDF2
- Real-time search across structured threat data
- Importance of modular, clean Python scripts

---

## 📅 Day 16 – Continuous Telegram Alert Loop & Logging
**Date:** 2025-08-08

✔ Integrated real-time alert loop via `auto_alert_loop.py`  
✔ Telegram bot (@PhishingAlertBot) now sends continuous alerts every 300 seconds  
✔ Developed alert deduplication using `alerts_sent` SQLite table  
✔ Implemented local logging: `logs/alert_log.txt` to track every alert sent  
✔ Verified alerts sent for all current threats in database  
✔ Built `day16_pdf_report.py`:
   - Summarizes Day 16 tasks
   - Includes sample alerts
   - Logs Deprecation Warnings resolved
   - Uses Unicode-safe fonts (DejaVuSans)
✔ Report auto-emailed to 📧 danielmuteti590@gmail.com  
✔ Maintained professional codebase structure with future scalability in mind  


   - Logs Deprecation Warnings resolved
   - Uses Unicode-safe fonts (DejaVuSans)
✔ Report auto-emailed to 📧 danielmuteti590@gmail.com  
✔ Maintained professio


## 📅 Day 17 – Secure Dashboard + Automated PDF Threat Reporting
Date: 2025-08-08

✔ Added Basic Authentication using .env credentials to protect all endpoints
✔ Created /threats route with:

Search filters (keyword, source)

Pagination (5 entries per page)

CSV export functionality
✔ Access to /threats now logs every visit to access.log with timestamp and user
✔ Built /dashboard route with:

Pie chart (Threats by Type)

Bar chart (Threats by Source)

Line chart (Threats over Time, formatted as 08-Aug, etc.)
✔ Made charts interactive: Clicking segments redirects to filtered /threats views
✔ Applied Bootstrap 5 for professional UI (cards, layout, buttons, logout)
✔ Implemented /logout route that triggers 401 to re-prompt for login
✔ Created day17_pdf_report.py:

Connects to osint_threats.db

Generates PDF report with:
• Total threat count
• Top sources
• Top types
• 5 most recent threats
✔ Auto-emails report using Gmail SMTP + secure .env integration
✔ Verified working delivery to 📧 danielmuteti590@gmail.com
✔ Structured project cleanly:

scripts/day17_pdf_report.py

dashboard/app.py, templates/, .env, access.log


