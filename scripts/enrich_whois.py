import json
from datetime import datetime, timezone, timedelta
import whois

EAT = timezone(timedelta(hours=3))

with open("out/normalized.json") as f:
    data = json.load(f)

for entry in data:
    try:
        w = whois.whois(entry["domain"])
        # Handle lists and missing values gracefully
        created = None
        if isinstance(w.creation_date, list) and w.creation_date:
            created = w.creation_date[0]
        elif isinstance(w.creation_date, datetime):
            created = w.creation_date
        entry["whois_created"] = created.isoformat() if created else None
        entry["whois_registrar"] = getattr(w, "registrar", None)
    except Exception as e:
        entry["whois_created"] = None
        entry["whois_registrar"] = None

# Save enriched file
with open("out/enriched.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"[+] Enriched {len(data)} threats -> out/enriched.json")
