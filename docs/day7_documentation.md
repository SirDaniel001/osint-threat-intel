# 📘 Day 7 Documentation – OSINT Threat Intelligence Project
**Date:** 30/07/2025  
**Focus:** Configure Tor + Stem on Kali, Enable Identity Rotation, Build Dark Web Crawler, Generate PDF Report with Email Delivery

---

## ✅ **Overview of Day 7 Tasks**
- Installed and configured **Tor** on Kali
- Installed Python libraries: `stem`, `requests[socks]`
- Verified Tor SOCKS proxy (127.0.0.1:9050)
- Enabled Tor **ControlPort** (9051) for Stem
- Implemented **Tor Identity Rotation** using Stem
- Built **Dark Web Crawler** with:
  - Tor proxy support
  - Onion site crawling (legal/public sites)
  - Random delays to mimic human browsing
  - Retry logic for failed requests
  - Logging and CSV export
- Generated **PDF Report** with:
  - Summary of sites crawled
  - Response code distribution chart
  - Project logo and date
- Sent PDF report via **Email (SMTP)** using `.env` for credentials

---

## ✅ **Commands Executed**
```bash
# Install Tor
sudo apt update && sudo apt install tor -y

# Install dependencies
source venv/bin/activate
pip install stem requests[socks] matplotlib fpdf python-dotenv

# Enable ControlPort
sudo nano /etc/tor/torrc
# Added:
ControlPort 9051
CookieAuthentication 1

# Restart Tor
sudo systemctl restart tor

# Verify ControlPort
netstat -tlnp | grep 9051

# Run identity rotation test
python scripts/day7_tor_rotation.py

# Run enhanced Dark Web crawler
python scripts/day7_darkweb_crawler.py

# Generate PDF report and send via email
python scripts/day7_pdf_report.py
