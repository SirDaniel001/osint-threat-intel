# OSINT Threat Intelligence Platform

## 📌 Project Overview
This project is a **30-day challenge** to build a professional-grade OSINT-based Threat Intelligence Platform. The platform focuses on detecting phishing domains, monitoring dark web sources, and generating real-time alerts for threats targeting financial institutions in Kenya, including the Central Bank of Kenya and related services (e.g., M-PESA).

---

## ✅ Objectives
- Detect **phishing domains** targeting financial entities.
- Monitor **surface web** and **dark web forums** for malicious activity.
- Collect, enrich, and correlate threat intelligence data.
- Provide **real-time alerts** and a **visual dashboard** for analysts.

---

## 🛠 Tech Stack
- **Backend:** Python (Flask, FastAPI)
- **Database:** SQLite / PostgreSQL
- **OSINT Tools & APIs:** Shodan, PhishTank, AbuseIPDB, WHOIS, Dark Web Crawler
- **Visualization:** Chart.js, Flask Templates
- **Deployment:** Linux (Kali)

---

## 📂 Project Structure
```
osint-threat-intel/
│── venv/                # Virtual environment
│── data/                # Raw and processed OSINT data
│── scripts/             # Scrapers and API scripts
│── core/                # Core logic (enrichment, correlation)
│── dashboard/           # Web dashboard (Flask templates/static)
│── config/              # API keys and environment configs
│── logs/                # Logs and error reports
│── requirements.txt     # Python dependencies
│── README.md            # Project documentation
│── main.py              # Entry point
```

---

## ✅ 30-Day Development Plan
| Day | Task |
|-----|------|
| 1   | Setup environment & install dependencies |
| 2   | Organize folder structure & Git setup |
| 3   | Build basic phishing domain scraper (Google & Pastebin) |
| 4   | Integrate PhishTank API |
| 5   | Clean & process collected data |
| 6   | Add error handling to scraping scripts |

---

## ✅ How to Run
1. Clone this repo:
   ```bash
   git clone https://github.com/YOUR_USERNAME/osint-threat-intel.git
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Add your API keys in `config/.env`:
   ```
   SHODAN_API_KEY=your_key
   ABUSEIPDB_API_KEY=your_key
   ```
4. Run the main script:
   ```bash
   python main.py
   ```

---

## ✅ Features (Planned)
- [ ] Surface Web Scraper for phishing domains
- [ ] Dark Web crawler (Tor + Stem)
- [ ] WHOIS & DNS enrichment
- [ ] SQLite database for storing IOCs
- [ ] Telegram bot alerts for new threats
- [ ] Flask dashboard with filtering & graphs
- [ ] PDF reporting for analysts

---

## ✅ Legal Disclaimer
This project is for **educational and defensive purposes only**. Use it ethically and within legal boundaries. Do not target unauthorized systems or engage in illegal activities.

---

## 👤 Author
**SirDaniel**  
Aspiring Cybersecurity Professional  
Email: danielmuteti590@gmail.com
