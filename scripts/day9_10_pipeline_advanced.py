import os
import re
import requests
import pandas as pd
import json
import time
import random
from bs4 import BeautifulSoup
from stem import Signal
from stem.control import Controller
from urllib.parse import urlparse, parse_qs
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from fpdf import FPDF
import matplotlib.pyplot as plt
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import smtplib
from dotenv import load_dotenv
import plotly.express as px

# ----------------------------
# Load Environment Variables
# ----------------------------
load_dotenv()
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# ----------------------------
# Config
# ----------------------------
PROXIES = {"http": "socks5h://127.0.0.1:9050", "https": "socks5h://127.0.0.1:9050"}
AHMIA_URL = "https://ahmia.fi/search/?q=banking"
RESULT_LIMIT = 30
OUTPUT_DARKWEB = "../data/darkweb_analysis.csv"
OUTPUT_WHOIS = "../data/whois_enriched.csv"
OUTPUT_FEED_CSV = "../data/threat_feed.csv"
OUTPUT_FEED_JSON = "../data/threat_feed.json"
REPORT_FILE = "../data/full_pipeline_report.pdf"
HTML_DASHBOARD = "../data/ioc_dashboard.html"
CHART_DIR = "../data/charts_pipeline"
LOGO_PATH = "../data/logo.png"
API_KEY = "YOUR_WHOISXML_API_KEY"  # Replace with your API key
API_URL = "https://www.whoisxmlapi.com/whoisserver/WhoisService"
LOG_FILE = "../logs/full_pipeline.log"
MAX_THREADS = 5

os.makedirs("../data", exist_ok=True)
os.makedirs("../logs", exist_ok=True)
os.makedirs(CHART_DIR, exist_ok=True)

KEYWORD_WEIGHTS = {
    r"\bcbk\b": 150,
    r"central bank of kenya": 150,
    r"m[-\s]?pesa": 120,
    r"\.ke": 50
}
SUSPICIOUS_TLDS = {"app", "xyz", "tk", "top", "gq", "ml"}
FREE_REGISTRARS = ["freenom", "000domains"]

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")
    print(msg)

# ----------------------------
# IOC Tagging
# ----------------------------
def assign_ioc_tags(domain, keywords, registrar):
    tags = []
    if keywords:
        tags.append("banking_fraud")
    if registrar and any(free in registrar.lower() for free in FREE_REGISTRARS):
        tags.append("free_domain_risk")
    tld = domain.split('.')[-1]
    if tld in SUSPICIOUS_TLDS:
        tags.append("phishing")
    tags.append("darkweb_reference")
    return ",".join(tags)

# ----------------------------
# Tor Identity Rotation
# ----------------------------
def renew_identity():
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
        log("[INFO] Tor identity rotated.")
        time.sleep(5)
    except Exception as e:
        log(f"[ERROR] Failed to rotate Tor identity: {e}")

# ----------------------------
# Fetch Onion Links
# ----------------------------
def fetch_dynamic_onion_sites():
    log("[INFO] Fetching onion links from Ahmia...")
    try:
        response = requests.get(AHMIA_URL, timeout=20)
        soup = BeautifulSoup(response.text, "html.parser")
        raw_links = [a["href"] for a in soup.find_all("a", href=True) if ".onion" in a["href"]]
        onion_domains = []
        for link in raw_links:
            if "redirect_url=" in link:
                parsed = parse_qs(urlparse(link).query)
                if "redirect_url" in parsed:
                    url = parsed["redirect_url"][0]
                else:
                    continue
            else:
                url = link
            parsed_url = urlparse(url)
            domain = parsed_url.scheme + "://" + parsed_url.hostname
            onion_domains.append(domain)
        onion_domains = list(set(onion_domains))[:RESULT_LIMIT]
        log(f"[INFO] Extracted {len(onion_domains)} unique onion URLs.")
        return onion_domains
    except Exception as e:
        log(f"[ERROR] Ahmia fetch failed: {e}")
        return []

# ----------------------------
# Analyze Content + Extract Links
# ----------------------------
def analyze_content(text):
    found_keywords = []
    threat_score = 0
    lower_text = text.lower()
    for kw, weight in KEYWORD_WEIGHTS.items():
        if re.search(kw, lower_text):
            found_keywords.append(kw)
            threat_score += weight
    return found_keywords if found_keywords else None, threat_score

def extract_links(soup):
    links = []
    for a in soup.find_all("a", href=True):
        href = a['href']
        if href.startswith("http"):
            links.append(href)
    return links

# ----------------------------
# Crawl Onion Sites
# ----------------------------
def fetch_url(url):
    for attempt in range(1, 3):
        try:
            log(f"[INFO] Crawling {url} (Attempt {attempt})")
            response = requests.get(url, proxies=PROXIES, timeout=30)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                text = soup.get_text(separator=" ")
                keywords_found, score = analyze_content(text)
                links = extract_links(soup)
                return [url, "200", keywords_found, score, datetime.now(), links, False]
            else:
                return [url, response.status_code, None, 0, datetime.now(), [], False]
        except Exception as e:
            log(f"[WARN] {url} failed: {e}")
            renew_identity()
            time.sleep(random.randint(5, 10))
    return [url, "unreachable", None, 0, datetime.now(), [], True]

def crawl_onion_sites(onion_sites):
    records = []
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = {executor.submit(fetch_url, url): url for url in onion_sites}
        for future in as_completed(futures):
            records.append(future.result())
    df = pd.DataFrame(records, columns=[
        "url", "status", "keywords_found", "threat_score", "crawled_at", "extracted_links", "unreachable"
    ])
    df.to_csv(OUTPUT_DARKWEB, index=False)
    log(f"[+] Dark web analysis saved: {OUTPUT_DARKWEB}")
    return df

# ----------------------------
# WHOIS Enrichment
# ----------------------------
def extract_domain(url):
    try:
        return urlparse(url).netloc.lower()
    except:
        return None

def fetch_whois(domain):
    params = {"apiKey": API_KEY, "domainName": domain, "outputFormat": "JSON"}
    try:
        response = requests.get(API_URL, params=params, timeout=15)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        log(f"[ERROR] WHOIS fetch failed for {domain}: {e}")
    return None

def analyze_whois(domain, data):
    if not data or "WhoisRecord" not in data:
        return {"registrar": "Unknown", "risk_score": 0, "status": "Failed"}
    registrar = data.get("WhoisRecord", {}).get("registrarName", "Unknown")
    risk_score = 0
    if any(free in registrar.lower() for free in FREE_REGISTRARS):
        risk_score += 50
    tld = domain.split('.')[-1]
    if tld in SUSPICIOUS_TLDS:
        risk_score += 30
    return {"registrar": registrar, "risk_score": risk_score, "status": "Success"}

def process_domain(domain, source_onion, keywords, threat_score, unreachable_flag):
    if not domain or ".onion" in domain:
        return {
            "ioc_type": "domain",
            "domain": domain,
            "registrar": "Skipped",
            "risk_score": 0,
            "whois_status": "Skipped",
            "ioc_tags": "darkweb_reference" + (",offline_onion" if unreachable_flag else ""),
            "checked_at": datetime.now(),
            "source_onion": source_onion,
            "keywords_found": keywords,
            "darkweb_threat_score": threat_score
        }
    data = fetch_whois(domain)
    analysis = analyze_whois(domain, data)
    tags = assign_ioc_tags(domain, keywords, analysis["registrar"])
    if unreachable_flag:
        tags += ",offline_onion"
    time.sleep(1)
    return {
        "ioc_type": "domain",
        "domain": domain,
        "registrar": analysis["registrar"],
        "risk_score": analysis["risk_score"],
        "whois_status": analysis["status"],
        "ioc_tags": tags,
        "checked_at": datetime.now(),
        "source_onion": source_onion,
        "keywords_found": keywords,
        "darkweb_threat_score": threat_score
    }

def whois_enrichment(link_map):
    results = []
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = {
            executor.submit(process_domain, domain, source, keywords, score, unreachable): (domain, source)
            for (domain, source, keywords, score, unreachable) in link_map
        }
        for future in as_completed(futures):
            results.append(future.result())
    pd.DataFrame(results).to_csv(OUTPUT_WHOIS, index=False)
    log(f"[+] WHOIS enrichment saved: {OUTPUT_WHOIS}")
    return results

# ----------------------------
# Threat Feed Export
# ----------------------------
def export_threat_feed(results):
    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_FEED_CSV, index=False)
    with open(OUTPUT_FEED_JSON, "w") as f:
        json.dump(results, f, indent=4, default=str)
    log(f"[+] Threat feed exported: {OUTPUT_FEED_CSV} & {OUTPUT_FEED_JSON}")

# ----------------------------
# Generate PDF Report
# ----------------------------
def generate_report(df):
    status_counts = df['whois_status'].value_counts()
    plt.figure(figsize=(6, 4))
    status_counts.plot(kind='bar', color=['green', 'orange', 'red'])
    plt.title('WHOIS Status Distribution')
    plt.savefig(os.path.join(CHART_DIR, "whois_status.png"))
    plt.close()

    plt.figure(figsize=(6, 4))
    df['risk_score'].plot(kind='hist', bins=5, color='blue', edgecolor='black')
    plt.title('Risk Score Distribution')
    plt.savefig(os.path.join(CHART_DIR, "risk_score.png"))
    plt.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Dark Web + WHOIS Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Generated on: {datetime.now()}", ln=True)
    pdf.ln(10)
    pdf.cell(0, 10, f"Total Domains: {len(df)}", ln=True)
    pdf.cell(0, 10, f"High Risk: {len(df[df['risk_score'] > 0])}", ln=True)
    pdf.cell(0, 10, f"Offline Onion Sources: {len(df[df['ioc_tags'].str.contains('offline_onion')])}", ln=True)
    pdf.image(os.path.join(CHART_DIR, "whois_status.png"), x=10, y=None, w=180)
    pdf.image(os.path.join(CHART_DIR, "risk_score.png"), x=10, y=None, w=180)
    pdf.output(REPORT_FILE)
    log(f"[+] PDF Report Generated: {REPORT_FILE}")

# ----------------------------
# HTML Dashboard
# ----------------------------
def generate_dashboard(df):
    fig = px.bar(df, x='ioc_tags', title='IOC Tags Distribution')
    fig.write_html(HTML_DASHBOARD)
    log(f"[+] HTML Dashboard Generated: {HTML_DASHBOARD}")

# ----------------------------
# Pipeline Execution
# ----------------------------
if __name__ == "__main__":
    log("[INFO] Starting advanced pipeline with offline_onion IOC tagging...")
    onion_sites = fetch_dynamic_onion_sites()
    darkweb_df = crawl_onion_sites(onion_sites)

    link_map = []  # (domain, source_onion, keywords, score, unreachable)
    for _, row in darkweb_df.iterrows():
        source_onion = row['url']
        keywords = row['keywords_found']
        score = row['threat_score']
        unreachable = row['unreachable']
        links = eval(row['extracted_links']) if pd.notna(row['extracted_links']) else []
        for link in links:
            domain = extract_domain(link)
            if domain and ".onion" not in domain:
                link_map.append((domain, source_onion, keywords, score, unreachable))

    log(f"[INFO] Total unique surface domains found: {len(link_map)}")

    results = whois_enrichment(link_map)
    export_threat_feed(results)
    df = pd.DataFrame(results)
    generate_report(df)
    generate_dashboard(df)
    log("[+] Advanced pipeline completed successfully.")
