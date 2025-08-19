FOR setup instructions, see [PROJECT_SETUP.md](PROJECT_SETUP.md)
# 🔍 OSINT Threat Intelligence Project

➡️ For installation & usage instructions, see [PROJECT_SETUP.md](PROJECT_SETUP.md)

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

### 📅 Day 18 — Automated PDF Intelligence Report with AI Cover

##  📅 Day 18 — Automated PDF Intelligence Report with AI Cover & Flowchart Overlay
Objective:
Enhance the OSINT Threat Intelligence Dashboard with automated PDF reporting, AI-generated visuals, flowchart diagrams, and email delivery.

Tasks Completed:

Developed scripts/day18_pdf_report.py:

Fetches real-time threat statistics from the SQLite database.

Generates charts for:

Top 5 Threat Sources

Top 5 Threat Types

Threats Timeline

Integrates AI-generated cover image (reports/day18_ai_image.png).

Overlays a transparent flowchart (reports/day18_flowchart_transparent.png) on the cover page.

Embeds full-size flowchart inside the PDF for process visualization.

Compiles all data and visuals into a professionally formatted PDF.

Emails the PDF automatically via Gmail SMTP.

New Files & Updates:

scripts/day18_pdf_report.py — Main PDF report generation and email automation script with charting & flowchart overlay.

reports/day18_ai_image.png — AI-generated cover image for the report.

reports/day18_flowchart.png — Original automation flowchart.

reports/day18_flowchart_transparent.png — Transparent overlay version for the cover page.

reports/day18_threat_report_YYYYMMDD.pdf — Generated PDF with charts, flowchart, and threat stats.

Environment Variables:

EMAIL_SENDER

EMAIL_PASSWORD (Gmail App Password)

EMAIL_RECEIVER

Automation:

Configured cron job to run day18_pdf_report.py daily at a set time (example: 10:35 AM).

Integrated with the existing daily_report.sh for text-based daily reports.

Outcome:

Fully automated daily threat intelligence PDF generation.

Enhanced professional presentation with AI-generated cover and visualized workflow.

Seamless email delivery for analyst review without manual intervention.

Improved clarity 


---

## 📅 Day 19 — Advanced Dashboard Filtering & Search

**Objective:**  
Enhance the OSINT Threat Intelligence Dashboard with advanced search, filtering, and API capabilities.

**Key Features Implemented:**
- Multiple filters in `/threats`:
  - Keyword
  - Source
  - Threat type
  - Domain
  - Date range (`date_from`, `date_to`)
- AJAX-powered search results for a faster experience
- CSV export for filtered results
- Secure parameterized SQL queries
- New `/api/threats` endpoint for JSON output with pagination
- Validation for date format in API (returns HTTP 400 for invalid dates)

**New Files/Updates:**
- **`dashboard/app.py`** — updated with `fetch_threats()`, `count_threats()`, `/api/threats` endpoint
- **`dashboard/templates/threats.html`** — updated UI with filters, AJAX search, and pagination
- **`scripts/day19_pdf_report.py`** — generates PDF report using AI cover from Day 18, includes charts, and emails to analyst

**API Test Example:**
```bash
curl -u SirDaniel:Daniel@001 "http://127.0.0.1:5000/api/threats?keyword=CBK&per_page=5&page=1"

## 📅 Day 20 — OSINT Threat Intelligence Dashboard & Automated PDF Email Report

**Date:** 2025-08-11  
**Status:** ✅ Completed

### 🔹 Overview
Today’s focus was on **automating threat intelligence reporting** and integrating it with the dashboard for professional-grade cyber intelligence workflows.  
This marks the completion of **Phase 2** of the 30-day OSINT & Threat Intel project.

---

### 🛠 Key Tasks Accomplished

1. **SQLite Database Preparation**
   - Verified and populated `osint_threats.db` with sample and real data.
   - Ensured table structure matches dashboard’s threat querying functions.

2. **Flask Dashboard Fixes**
   - Corrected `app.py` to pass `metrics` and `chart_data` to `dashboard.html`.
   - Updated Jinja templates to avoid undefined variable errors.
   - Verified charts, filters, and top sources/types statistics load correctly.

3. **`day20_pdf_report.py` Script**
   - Generates a **styled PDF report** with:
     - Total threats count
     - Top sources & top types
     - 10 most recent threats
   - Color-coded sections for better readability.
   - Uses Python `fpdf` for PDF generation.

4. **Automated Email Reporting**
   - Configured `.env` for secure SMTP credentials.
   - Integrated Gmail App Password authentication for secure sending.
   - Email includes PDF as attachment for archival and offline review.

5. **Testing & Verification**
   - Successfully generated PDF with sample data.
   - Verified email sending workflow using Gmail SMTP.
   - Fixed Unicode emoji issue in PDF by replacing with ASCII symbols.

---

### 📂 Files Added / Updated
- **`dashboard/app.py`** — Fixed data passing and improved stability.
- **`dashboard/templates/dashboard.html`** — Added metrics, risk score badges, and chart integration.
- **`scripts/day20_pdf_report.py`** — Main PDF & email reporting automation script.
- **`.env`** — Holds sensitive SMTP credentials (not tracked in Git).

---

### 📸 Sample Output
**Terminal Output:**

##  📅 Day 21 — Interactive Charts & Enhanced Threat Filtering
Date: 2025-08-13
Status: ✅ Completed

🔹 Overview
Today’s milestone was all about making the OSINT Threat Intelligence Dashboard interactive and enhancing data exploration.
We implemented clickable charts, improved report metrics alignment, and refined the HTML templates for a more intuitive workflow.

🛠 Key Tasks Accomplished
Interactive Chart Filtering

Added JavaScript event handlers to dashboard.html so clicking a chart element automatically filters and opens the relevant threats:

Type Pie Chart → Filters threats by selected type.

Source Bar Chart → Filters threats by selected source.

Date Line Chart → Filters threats by specific date.

Metrics Period Alignment

Updated backend logic in app.py to ensure phishing_count, darkweb_hits, and whois_suspicious metrics reflect the same 14-day timeframe as trend charts.

Template Improvements

Added safe navigation for missing data to prevent rendering errors.

Streamlined dashboard.html to keep design consistent while introducing interactivity.

Route & Default View Fixes

Created /dashboard as the main landing page instead of a missing / route to eliminate 404 errors on load.

Updated navbar link targets accordingly.

Final Functional Verification

Confirmed charts load correctly and click events redirect with proper query parameters.

Verified PDF and HTML reports remain functional after metric updates.

Tested with various sample datasets to ensure filtering works across all threat categories and date ranges.

📂 Files Added / Updated
dashboard/app.py — Added metric period alignment and route fixes.

dashboard/templates/dashboard.html — Implemented clickable chart sections for instant filtering.

dashboard/templates/report.html — Updated metrics to match unified timeframe.

## 📅 Day 22 — Dark Mode & Dynamic Chart Theme Switching
Date: 2025-08-13
Status: ✅ Completed

🔹 Overview
Today’s milestone focused on upgrading the dashboard’s UI/UX by adding Dark Mode support and making Chart.js visualizations adapt instantly to theme changes. This brings a more modern, premium feel to the OSINT Threat Intelligence Dashboard.

🛠 Key Tasks Accomplished

Dark Mode Implementation

Added a Dark Mode toggle button in the navbar.

Theme preference is stored in localStorage and applied on page load.

Smooth transitions for background, text, cards, and tables.

Dynamic Chart Theme Switching

Charts automatically recolor when toggling themes.

Added high-contrast palettes for dark mode and preserved original colors for light mode.

Implemented smooth 500 ms animations for theme transitions.

UI Enhancements

Polished metric card hover effects.

Improved badge colors for risk levels in both light and dark themes.

Ensured tables, lists, and chart legends maintain readability across modes.

Event-Driven Chart Refresh

Created a themeChange event in darkmode.js.

Chart rendering logic listens for this event and rebuilds charts on-the-fly.

📂 Files Added / Updated

dashboard/templates/dashboard.html — Added Dark Mode button, chart theme logic, smooth animations.

dashboard/static/css/style.css — Added full dark mode styling and transition effects.

dashboard/static/js/darkmode.js — Handles theme toggling, persistence, and triggers chart refresh events.

## 📅 Day 23 — Full Threat Intelligence Pipeline

Date: 2025-08-16
Status: ✅ Completed

🔹 Overview
Today’s milestone brings everything together into a single automated pipeline that collects phishing indicators, extracts domains, stores them in the database, and sends real-time alerts via Telegram. This marks the completion of the end-to-end OSINT → Threat Intel → Alerts workflow.

🛠 Key Tasks Accomplished

Phishing Data Collection

Scrapes Google search results for phishing-related queries.

Fetches recent Pastebin archives and extracts potential phishing URLs.

Cleans, deduplicates, and merges results into CSV outputs.

Domain Extraction & Cleaning

Extracts unique domains from URLs.

Saves domains to output/clean_phishing_domains.csv for further analysis.

Database Integration

Automatically inserts new phishing domains into threats.db.

Avoids duplicates by checking existing records.

Alerts & Reporting

Sends Telegram alerts for newly discovered domains.

Generates a daily summary report with the latest 20 threats.

Provides end-to-end visibility from collection → analysis → alerting.

📂 Files Added / Updated

day3_phishing_scraper/phishing_scraper.py — Updated Google & Pastebin scrapers.

day3_phishing_scraper/domain_extractor.py — Extracts and cleans unique domains.

scripts/day23_integrate_scraper.py — Inserts domains into SQLite threats.db.

scripts/telegram_alert.py — Sends real-time Telegram alerts.

scripts/day23_full_pipeline.py — Orchestrates the entire Day 23 pipeline.

📊 Final Outputs

output/google_phishing_urls.csv — Google-scraped phishing URLs.

output/pastebin_phishing_urls.csv — Pastebin-scraped phishing URLs.

output/all_phishing_urls.csv — Merged and deduplicated URLs.

output/clean_phishing_domains.csv — Extracted clean phishing domains.

threats.db — SQLite database of phishing domains with timestamps.

Telegram alerts & daily summary report — Sent automatically.

## 📅 Day 24 — Bug Fixing & Performance Optimization

Date: 2025-08-18  
Status: ✅ Completed  

🔹 Overview  
Day 24 focused on **stabilizing, fixing errors, and optimizing performance** across the project.  
We refactored the database insert pipeline, eliminated broken test dependencies, and introduced performance benchmarking to ensure scalability.  
This guarantees the threat intelligence system can handle **large datasets quickly and reliably**.  

🛠 Key Tasks Accomplished  

**Bug Fixes**  
- Fixed `test_insert.py` breaking due to missing CLI args by converting it into a clean importable module (`insert_script.py`).  
- Improved `scripts/day7_tor_test.py` with error handling when Tor service is unavailable.  

**Database Insert Optimization**  
- Refactored `database/insert_script.py` to use `executemany` for **bulk inserts**.  
- Created reusable `insert_from_json()` function for both CLI and test usage.  

**Testing Enhancements**  
- Added `tests/test_insert_script.py` to validate correctness of JSON → DB inserts.  
- Built `tests/test_insert_comparison.py` to compare **legacy vs optimized inserts**, showing ~1.1x speedup.  
- Added `tests/test_query_perf.py` to benchmark query speed on indexed columns (domain, date, keywords).  

**Performance Achievements**  
- Bulk inserts achieved speeds of **~200K records/sec**.  
- Query performance validated with indexed lookups (instantaneous results).  

📂 Files Added / Updated  
- `database/insert_script.py` — Refactored for modular inserts & bulk optimization.  
- `scripts/day7_tor_test.py` — Added timeout handling for Tor proxy.  
- `tests/test_insert_script.py` — Unit test for insert correctness.  
- `tests/test_insert_comparison.py` — Legacy vs optimized insert benchmark.  
- `tests/test_query_perf.py` — Query performance benchmark.  

📊 Final Outputs  
- ✅ All tests passing (unit + performance).  
- ✅ Database can handle **large-scale phishing feeds** efficiently.  
- ✅ Clean testable pipeline for inserts, queries, and performance metrics.  

## 📅 Day 25 — Documentation & GitHub Integration

Date: 2025-08-19
Status: ✅ Completed

🔹 Overview
Day 25 was all about solidifying the project foundation: creating full setup documentation, fixing scraper issues, ensuring the dashboard works, and syncing everything to GitHub with SSH authentication.
This makes the project reproducible, collaborative-ready, and portfolio-ready.

🛠 Key Tasks Accomplished

Documentation

Added PROJECT_SETUP.md with full environment + usage instructions.

Documented setup for virtualenv, database, scrapers, and dashboard.

Scraper Fixes

Fixed phishing_scraper.py so it successfully scrapes Google search + Pastebin for phishing URLs.

Outputs stored in CSVs and merged into output/all_phishing_urls.csv.

Dashboard Validation

Verified Flask dashboard runs at 127.0.0.1:5000.

Confirmed /dashboard + API endpoints (/api/trends/*) return expected data.

GitHub Integration

Configured GitHub SSH key (~/.ssh/id_ed25519) for secure pushes.

Corrected remote URL from placeholder → github.com/SirDaniel001/osint-threat-intel.git.

Merged day24-fixes → master and pushed all project history successfully.

📂 Files Added / Updated

PROJECT_SETUP.md — Full setup guide.

day3_phishing_scraper/phishing_scraper.py — Fixed and tested.

dashboard/* — Verified functional templates + API endpoints.

.git/config + SSH key setup — for GitHub authentication.

📊 Final Outputs

✅ Setup guide available for anyone cloning the repo.

✅ Working phishing scraper pipeline with Google + Pastebin feeds.

✅ Dashboard online, serving threat intel stats.

✅ GitHub repo fully synced & backed up.
🛡 Ethical Use  
This project is built for educational and ethical security research purposes only.  

⚠ All data used in this project is from publicly accessible, non-restricted OSINT feeds.  
Do NOT use this platform to interact with systems you are not explicitly authorized to investigate.  

🛡 Ethical Use
This project is built for educational and ethical security research purposes only.

⚠️ All data used in this project is from publicly accessible, non-restricted OSINT feeds.
Do NOT use this platform to interact with systems you are not explicitly authorized to investigate.                                                                 
Let me know if you also want the updated `SUCCESS_JOURNAL.md` next for Day 13. You're doing an incredible job keeping everything properly documented and automated 💪.

