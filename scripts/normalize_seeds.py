import json
from datetime import datetime, timezone, timedelta
import os

EAT = timezone(timedelta(hours=3))
now = datetime.now(EAT).isoformat()

def load(path):
    with open(path) as f:
        return json.load(f)

def deobf(domain):
    return domain.replace("[.]", ".")

surface = load("day3_phishing_scraper/output/surface_seeds.json")
dark = load("day3_phishing_scraper/output/dark_seeds.json")

records = surface + dark
seen = set()
normalized = []

for r in records:
    dom = deobf(r["indicator"]).lower()
    if (dom, r["source"]) in seen:
        continue
    seen.add((dom, r["source"]))

    desc = r.get("context", "")
    kws = []
    if "cbk" in dom or "cbk" in desc.lower():
        kws.append("CBK")
    if "mpesa" in dom.lower() or "m-pesa" in desc.lower():
        kws.append("M-PESA")

    normalized.append({
        "domain": dom,
        "source": r["source"],
        "description": desc,
        "first_seen": now,
        "keywords": kws,
        "risk_score": 70 if kws else 50
    })

os.makedirs("out", exist_ok=True)
with open("out/normalized.json", "w") as f:
    json.dump(normalized, f, indent=2)

print(f"[+] Normalized {len(normalized)} threats -> out/normalized.json")
