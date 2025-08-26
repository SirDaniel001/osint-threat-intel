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

# 📅 Day 18 – Automated PDF OSINT Threat Report with AI Cover & Email Delivery
📅 Day 18 – Automated PDF Threat Reports with AI Cover & Email Delivery
Date: 2025-08-09

✔ Developed day18_pdf_report.py to automatically generate a professional PDF threat intelligence report
✔ Integrated AI-generated cybersecurity-themed cover image for a polished first impression
✔ Implemented multi-page PDF layout with:

Cover page (full-page AI image)

Summary statistics (total threats, top sources, top types)

Visual analytics (pie, bar, and line charts via Matplotlib)

Recent threat listings (latest 10 threats with full details)
✔ Connected to SQLite database to pull live threat data:

Top 5 sources

Top 5 types

Threat counts over time

Latest 10 records
✔ Added email automation via Gmail SMTP with secure .env credentials (no plaintext passwords in code)
✔ Designed reports folder structure for consistent archiving: /reports/day18_threat_report_YYYYMMDD.pdf
✔ Tested report generation end-to-end — verified PDF received in inbox 📧
✔ Updated requirements.txt to pin all dependencies for full reproducibility
✔ Maintained modular structure for easy reuse in future reporting workflows

📌 Impact: This completes a fully automated Daily Threat Intelligence Reporting System, delivering actionable intelligence directly to email every morning with minimal human intervention.
#  ## 📅 Day 19 — Advanced Filtering & Search in OSINT Dashboard

**Objective:**  
Enhance the OSINT Threat Intelligence Dashboard with advanced search, filtering, and API integration for real-time threat queries.

**Tasks Completed:**
- Implemented advanced filtering in `/threats` route:
  - Keyword search
  - Source filtering
  - Threat type filtering
  - Domain filtering
  - Date range filtering (`date_from` & `date_to`)
- Updated `app.py`:
  - New `fetch_threats()` supports multiple filter criteria
  - Added `count_threats()` to support API pagination
  - New `/api/threats` endpoint returning JSON data with total, page, per_page
  - Secure parameterized SQL queries to prevent injection
- Updated `templates/threats.html`:
  - Added full filter form (keyword, source, type, domain, date range)
  - Integrated AJAX to fetch and update threats table without page reload
  - Pagination dynamically updates without reloading the entire page
- API test via `curl`:
  ```bash
  curl -u SirDaniel:Daniel@001 "http://127.0.0.1:5000/api/threats?keyword=CBK&per_page=5&page=1"

## ✅ Day 20 — Automation Meets Threat Intel

**Date:** 2025-08-11  

### 🏆 Today’s Wins
- **Database Validation & Repair**
  - Fixed `osint_threats.db` so it matches all Flask dashboard queries.
  - Populated with realistic sample data for development testing.

- **Dashboard Stability**
  - Eliminated the `metrics is undefined` Jinja2 error.
  - All charts and metrics load without manual page refreshes.
  - Risk scoring now displays cleanly with color-coded badges.

- **PDF Report Automation**
  - Built `day20_pdf_report.py` from scratch.
  - Styled PDF layout with consistent section colors.
  - Displays total threats, top 5 sources, top 5 types, and the 10 most recent threats.
  - Removed problematic emojis to fix Unicode export errors.

- **Email Integration**
  - Implemented Gmail SMTP sending with App Password authentication.
  - Securely stored credentials in `.env`.
  - Email includes the PDF attachment + clear terminal confirmation on success.

### 💡 Key Insights
- App passwords bypass Gmail’s “Less Secure App” blocking and are essential for automation.
- PDF generation works best with strict ASCII for compatibility.
- Secure environment variables prevent credential leaks and keep automation scripts safe to share.

### 🚀 Momentum for Tomorrow
- Add **charts directly into PDF reports** for at-a-glance visuals.
- Schedule daily report sending with `cron` to remove manual triggers.
- Continue refining styling for both email body and PDF.

## ✅ Day 21 — Clickable Charts & Unified Metrics
Date: 2025-08-13

🏆 Today’s Wins
Interactive Chart Filtering

Added JavaScript event handlers so clicking on any chart segment automatically filters and opens the relevant threats view.

Enabled filtering by type, source, and detection date directly from the dashboard charts.

Consistent Reporting Periods

Updated backend logic so phishing_count, darkweb_hits, and whois_suspicious now match the 14-day trend chart period for accurate comparisons.

Ensured both PDF and HTML reports pull from the same unified timeframe.

Navigation & UX Enhancements

Fixed / route to redirect to /dashboard to eliminate the 404 error on load.

Refined dashboard.html layout for better responsiveness and visual balance.

Data Safety & Stability

Added null-checks in templates to prevent empty values from breaking the UI.

Verified that new features work with both real and sample datasets.

💡 Key Insights
Clickable chart interactions speed up investigations by reducing the need for manual filtering.

Aligning all metrics to the same timeframe prevents misleading trends and KPI discrepancies.

Route redirection improves user experience and prevents broken entry points.

🚀 Momentum for Tomorrow
Embed clickable trend charts directly into PDF reports for offline interactivity.

Add advanced filtering in the threats table (multi-select types, date ranges).

Start integrating dark web scraping results into the live dashboard for real-time alerts.

## ✅ Day 22 — Dark Mode & Dynamic Chart Themes
Date: 2025-08-13

🏆 Today’s Wins

Dark Mode Implementation

Added a Dark Mode toggle button in the navbar for instant theme switching.

Saved user theme preference in localStorage so it persists across sessions.

Applied smooth transitions to background, text, cards, tables, and lists for a premium feel.

Dynamic Chart Theme Switching

Charts now automatically recolor based on the selected theme.

Implemented high-contrast palettes for dark mode while retaining original colors in light mode.

Added 500 ms animations so chart color changes feel smooth instead of abrupt.

UI & UX Enhancements

Refined metric card hover animations for better interactivity.

Improved badge contrast for risk scores in both themes.

Ensured tables, chart legends, and list groups remain fully readable in dark mode.

Event-Driven Chart Refresh

Added a custom themeChange event in darkmode.js.

Chart rendering code listens for this event and rebuilds charts dynamically without page reload.

💡 Key Insights

Dark Mode greatly improves readability during extended investigations, especially in low-light environments.

Dynamic chart recoloring ensures visual consistency without requiring user refreshes.

Smooth transitions make the dashboard feel more polished and professional.

🚀 Momentum for Tomorrow

Begin integrating real-time OSINT data feeds into charts so visualizations update without manual refresh.

Explore adding a theme-aware PDF export to match the current dashboard style in reports.

### ✅ Day 23 — Full Threat Intelligence Pipeline

Date: 2025-08-16

🏆 Today’s Wins

Phishing Data Collection

Implemented Google search scraping for phishing-related queries.

Collected fresh Pastebin archives and extracted phishing URLs.

Deduplicated and saved results into structured CSV files.

Domain Extraction & Cleaning

Extracted unique domains from collected URLs.

Stored clean domains into output/clean_phishing_domains.csv for analysis.

Database Integration

Automated insertion of new phishing domains into threats.db.

Prevented duplication by validating against existing records.

Alerts & Reporting

Sent real-time Telegram alerts for newly discovered threats.

Delivered a daily summary report with the latest 20 domains.

Successfully connected the pipeline from scraping → database → alerting.

💡 Key Insights

Automating scraping + domain extraction + database insertion reduces manual effort and ensures consistency.

Telegram integration provides immediate visibility of new phishing threats.

Building the pipeline in stages (scraper → extractor → DB → alerts) ensured smooth debugging and integration.

🚀 Momentum for Tomorrow

Enhance domain reputation scoring (e.g., using VirusTotal or AbuseIPDB API).

Add visualization of phishing domain trends directly in the dashboard.

Automate pipeline execution via cron for scheduled intelligence updates.
## # ✅ Day 24 – Database Performance & Testing

## Achievements
- Refactored `insert_script.py` to support clean, reusable inserts.
- Implemented unit test for insert correctness (`tests/test_insert_script.py`).
- Added performance benchmark comparing legacy vs optimized bulk insert (`tests/test_insert_comparison.py`).
- Created automated performance test for query speed (`tests/test_query_perf.py`).
- Achieved blazing insert speed (~200K rec/s).
- Verified fast query response for domain, date, and keyword lookups.

## Lessons Learned
- `executemany` in SQLite massively improves bulk insert performance.
- Proper testing structure (`tests/`, `PYTHONPATH=.`) avoids import headaches.
- Performance tests ensure the database won’t choke at scale.
- Always automate query benchmarks to catch regressions early.

## Status
🎩 All tests passing — pipeline is optimized, tested, and production-ready.

### ✅ Day 25 – Setup Documentation & GitHub Integration
Achievements

Wrote PROJECT_SETUP.md with full environment setup and usage instructions.

Fixed and verified phishing_scraper.py to properly scrape Google + Pastebin.

Generated reports and confirmed Flask dashboard works (live at 127.0.0.1:5000).

Set up GitHub SSH authentication (no more password prompts).

Merged local day24-fixes into master and pushed all project updates to GitHub.

Repo is now fully synced and ready for collaboration/portfolio showcase.

Lessons Learned

Always add a setup guide (PROJECT_SETUP.md) to make the project reproducible for others.

GitHub SSH keys are safer and faster than HTTPS passwords.

Rebasing before pushing avoids messy merge commits.

Structuring commits by “Day XX” keeps progress traceable and professional.

Status

🚀 Project is fully documented, version-controlled, and synced to GitHub — foundation is rock-solid for the final stretch (Day 26–30).

## ✅ Day 25 – Final Setup Guide & GitHub Integration

## Achievements
- Wrote and added `PROJECT_SETUP.md` with complete setup instructions (environment, DB, scrapers, dashboard, alerts, reports).
- Updated `requirements.txt` with Day 25 notes (documentation & GitHub integration).
- Fixed GitHub remote URL to use **SSH keys** for secure authentication.
- Successfully merged Day 24 fixes into `master` and pushed the entire project to GitHub (`SirDaniel001/osint-threat-intel`).
- Verified repo is clean, organized, and ready for sharing or further development.

## Lessons Learned
- Always keep a **PROJECT_SETUP.md** for smooth onboarding and reproducibility.
- SSH keys are the secure and recommended way to push to GitHub.
- Proper branch merging avoids conflicts and ensures history stays clean.
- Documentation is just as critical as code for project success.

## Status
🎯 Project documentation and GitHub integration complete — **Day 25 wraps up the build phase successfully**.
---

## 📝 Success Journal — Day 27 (23/08)

**Task:** Push project to GitHub & publish first release 🚀  

✅ Successfully committed and pushed all pending changes, including reports and helper scripts.  
✅ Verified `.env` secrets are safe and excluded from the repo.  
✅ Created and published **Release v1.0.0** on GitHub with proper release notes.  
✅ Linked the official release in the README.md for easy access.  

**Reflection:**  
Today marks a major milestone — the project is now publicly available on GitHub in its first stable form. I learned how to properly manage commits, drafts, and GitHub releases, which made my work look polished and professional.  

**Next Step:**  
Prepare for **Day 28 — Project Presentation with diagrams**. This will serve as the final wrap-up before showcasing the work.  

## # Success Journal – Day 28 (24/08)

## 🎯 Goal of the Day
Prepare professional project presentation with architecture diagrams, workflows, and visual reports.

---

## ✅ Achievements
- Completed **master architecture diagram** (`day28_architecture.png`) showing data sources → processing → alerts → dashboard
- Created supporting **workflow, DFD, and testing pipeline diagrams**
- Linked diagrams into `README.md` for easy reference
- Organized repository artifacts (`reports/`, `database/`, `dashboard/`)
- Practiced presentation narrative (problem → solution → results)

---

## 📂 Evidence of Work
- `reports/day28_architecture.png` (main diagram for slides)
- Updated `README.md` with Day 28 diagrams
- Review of past outputs (`day24_report.pdf`, `day27_report.pdf`) integrated into presentation
- Tested dashboard screenshots and trend charts (`trend_chart.png`, `top_sources.png`)

---

## 🚀 Progress Reflection
Today’s focus was **clarity and presentation**. By converting the technical build into visual and documented form, I made the project accessible to both technical and non-technical audiences. This step transforms the raw system into a polished **threat intelligence product** ready for demonstration.

---

