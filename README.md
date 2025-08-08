# 🔍 OSINT Threat Intelligence Project

![OSINT Banner](data/data_banner.png)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Status](https://img.shields.io/badge/Progress-13%2F30-green)
![OSINT](https://img.shields.io/badge/Category-OSINT-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Last Update](https://img.shields.io/badge/Last%20Update-August%207%2C%202025-blueviolet)
![Database](https://img.shields.io/badge/Database-SQLite-lightgrey)
![Report Automation](https://img.shields.io/badge/Automated-PDF%20%26%20Email-brightgreen)
![Dark Web](https://img.shields.io/badge/DarkWeb-Tor%20Enabled-purple)
![WHOIS Enrichment](https://img.shields.io/badge/Feature-WHOIS%20Analysis-lightblue)

---

## 📖 Project Overview

This **30-Day OSINT Threat Intelligence Project** focuses on:
- Gathering phishing and fraud intelligence from open sources and the dark web
- Cleaning, analyzing, and visualizing cyber threat data
- Automating alerting and reporting systems
- Building dashboards for better insights
- Advanced tooling including WHOIS enrichment, IOC tagging, PDF/email reporting, and dark web monitoring

---

## 📅 Project Progress

![Progress](https://progress-bar.dev/13/?title=Completed&width=500&color=4caf50)

---

## ✅ Completed Days Breakdown

### ✅ Day 1 – Environment Setup
**Objective:** Prepare project environment for OSINT automation.

- Installed **Kali Linux** and verified **Python 3.x**
- Created structured project directories
- Initialized Git repository for version control

---

### ✅ Day 2 – Target Research
**Objective:** Define the OSINT focus and identify reliable intelligence sources.

- Selected threat sources: OpenPhish, PhishTank, URLhaus, Abuse.ch, Twitter OSINT, dark web
- Outlined core use cases: phishing detection, fraud tracking, IOC extraction

---

### ✅ Day 3 – Project Structure
**Objective:** Establish a clean and scalable project layout.

osint-threat-intel/
├── database/
├── scripts/
├── venv/
└── README.md

yaml
Copy
Edit

- Added `requirements.txt`
- Documented directory purpose

---

### ✅ Day 4 – OSINT Feeds Research
**Objective:** Discover and document threat intelligence APIs and formats.

- Collected feed URLs and endpoints from:
  - OpenPhish (CSV)
  - PhishTank (JSON)
  - URLhaus (TXT/CSV)
- Verified formats for ingestion

---

### ✅ Day 5–11 – Manual Data Collection
**Objective:** Test ingesting feeds manually before full automation.

- Manually collected indicators from selected sources
- Created sample datasets for:
  - Phishing domains
  - URLs
  - Hashes
- Verified indicator types and coverage
- Generated sample email + PDF reports from dark web scans

---

### ✅ Day 12 – SQLite Database Setup
**Objective:** Create the foundation for threat data persistence.

- Activated Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install requests pandas python-telegram-bot rich fpdf2
| Field          | Type     | Description                        |
| -------------- | -------- | ---------------------------------- |
| id             | INTEGER  | Primary key (auto increment)       |
| source         | TEXT     | Feed name (e.g., Twitter, URLhaus) |
| threat\_type   | TEXT     | Category (phishing, malware, etc.) |
| indicator      | TEXT     | IOC (URL, domain, IP, hash)        |
| description    | TEXT     | Optional human-readable info       |
| date\_detected | DATETIME | Default is current timestamp       |
| confidence     | INTEGER  | Score 1–100                        |
| extra\_info    | TEXT     | JSON-encoded metadata              |
Created create_db.py and test_insert.py

Verified insertion using:

bash
Copy
Edit
sqlite3 database/osint_threats.db "SELECT * FROM threats;"
osint-threat-intel/
├── database/
│   ├── osint_threats.db
│   ├── create_db.py
├── scripts/
│   └── test_insert.py
│   └── day12_pdf_report.py
├── data/
│   └── day12_report.pdf
├── README.md
✅ Day 13 – Phishing Data Ingestion
Objective: Automate ingesting phishing URLs into the SQLite database.

Created sample_phishing_feed.csv with test IOCs

Created insert_from_csv.py:

Read CSV

Parsed indicators

Inserted into threats table

Verified with:sqlite3 database/osint_threats.db "SELECT * FROM threats;"
Generated and emailed:

day13_pdf_report.py

day13_report.pdf → 📧 Sent to: danielmuteti590@gmail.com

📈 Highlights:

Used pandas to read feed and transform data

Handled date/time + default confidence scores

Verified source-specific record counts
### ✅ Day 13 – Phishing Feed Ingestion
**Objective:** Automate ingestion from feeds  
✔ Populated database from multiple sources  
✔ Confirmed ingestion through queries  
✔ Generated `day13_report.pdf`  
✔ Emailed report to danielmuteti590@gmail.com  

---

### ✅ Day 14 – Threat Search and Export
**Objective:** Implement advanced search + export  
✔ Created `search_threats.py` with CLI:
- `--keyword`
- `--source`
- `--from-date` / `--to-date`
- `--threat_type`
- `--min-confidence`
- `--export` (CSV/JSON)
- `--sort-by` + `--desc`
  
✔ Validated:
- Keyword match  
- Source filter  
- Date filter  
- Confidence threshold  

✔ Exported:
- `../results/search_results_day14.csv`
- `../results/search_results_day14.json`

✔ Generated report: `day14_report.pdf`  
✔ Report includes summary + top 5 threats  
✔ Emailed to danielmuteti590@gmail.com  

---

🏗 **Current Directory Tree**
osint-threat-intel/
├── database/
│ └── osint_threats.db
├── scripts/
│ ├── create_db.py
│ ├── test_insert.py
│ ├── ingest_feeds.py
│ ├── search_threats.py
│ └── day14_pdf_report.py
├── results/
│ ├── search_results_day14.csv
│ └── search_results_day14.json
├── data/
│ └── day14_report.pdf
├── venv/
├── README.md
└── requirements.txt


---

### ✅ Day 15 – Telegram Alert Bot Integration
**Objective:** Automate threat notifications to Telegram using a bot.

✔ Developed `telegram_alert.py` script  
✔ Configured `.env` with `TELEGRAM_TOKEN` and `CHAT_ID`  
✔ Bot integrated with DB to monitor new entries  
✔ Sent live threat alerts with fields:
  - Source  
  - Type  
  - Indicator  
  - Date Detected  
  - Confidence  

✔ Exported summary to PDF (`day15_report.pdf`)  
✔ Email delivery successful to `danielmuteti590@gmail.com`

📲 Bot Username: **@PhishingAlertBot**
[ALERT] New Threat Detected!
Source: OpenPhish
Type: phishing
Indicator: http://malicious-site1.com
Detected: 2025-08-07 10:00:00
Confidence: N/A

📅 Day 16 – Continuous Telegram Alert Loop + Logging
✔ Implemented auto_alert_loop.py to send new threat alerts every 5 minutes
✔ Prevented duplicate alerts using alerts_sent table in SQLite
✔ Logged each alert to logs/alert_log.txt for audit trails and redundancy
✔ Ensured continuous delivery via Telegram bot: @PhishingAlertBot
✔ Gracefully handled KeyboardInterrupt for safe manual exits
✔ Built day16_pdf_report.py for automated documentation
✔ PDF generated & emailed successfully
✔ Updated README.md and SUCCESS_JOURNAL.md

Sample Logged Alert:
[2025-08-08 14:28:00] 🚨 New Threat Detected!
Source: Twitter
Type: phishing
Indicator: maliciousdomain.com
Detected: 2025-08-06 13:33:27
Confidence: 85

## ✅ Day 17 – Threat Dashboard + Reporting Automation

### 📊 Features Implemented

- 🔐 **Basic Authentication** using credentials stored securely in `.env`
- 📋 **Threats Table View** at `/threats` with:
  - Pagination
  - Search filters (by keyword and source)
  - CSV export
  - Access logging (`access.log`)
- 📈 **Interactive Dashboard** at `/dashboard` with:
  - Pie chart: Threats by Type
  - Bar chart: Threats by Source
  - Line chart: Threats over Time (human-readable date format)
  - Chart click events that redirect to filtered views
- 🚪 **Logout** via `/logout` (returns 401 to re-prompt login)
- 🎨 **Bootstrap 5 styling** for polished UI/UX
- 📄 **PDF Report Generator** (`scripts/day17_pdf_report.py`) that:
  - Connects to `osint_threats.db`
  - Summarizes threat intelligence
  - Generates and emails a PDF report automatically
- 📧 **Email Integration** using `smtplib` and `.env` for secure credentials

### 🛠️ Environment Configuration (`.env`)

Ensure the following are set in your project root:

```env
ADMIN_USERNAME=SirDaniel
ADMIN_PASSWORD=Daniel@001

EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECEIVER=your_email@gmail.com
📁 Project Structure Highlights

osint-threat-intel/
├── dashboard/
│   ├── app.py                  # Flask server with auth and routes
│   ├── templates/
│   │   ├── index.html
│   │   ├── threats.html
│   │   └── dashboard.html
├── scripts/
│   └── day17_pdf_report.py     # PDF report generation and email sender
├── osint_threats.db            # SQLite database
├── .env                        # Env file with sensitive config
├── access.log                  # Threats route access log
└── README.md

## 💻 Requirements

💻 Requirements
Python 3.10+

SQLite

Telegram Bot API

Libraries:

pip install requests pandas rich fpdf python-telegram-bot

- Python 3.10+  
- SQLite3  
- Required Packages:
  ```bash
  pip install -r requirements.txt

💻 Requirements
Python 3.10+

SQLite 3

📦 Required Packages:pip install -r requirements.txt
Dependencies:

requests

pandas

python-telegram-bot

rich

fpdf2

matplotlib

python-dotenv

🛡 Ethical Use
This project is built for educational and ethical security research purposes only.

⚠️ All data used in this project is from publicly accessible, non-restricted OSINT feeds.
Do NOT use this platform to interact with systems you are not explicitly authorized to investigate.                                                                 
Let me know if you also want the updated `SUCCESS_JOURNAL.md` next for Day 13. You're doing an incredible job keeping everything properly documented and automated 💪.

