import argparse
import sqlite3
import pandas as pd
import os  # ✅ Fixed missing import
from rich.console import Console
from rich.table import Table

# Initialize Rich console
console = Console()

# ----------------------------
# CLI Argument Parsing
# ----------------------------
parser = argparse.ArgumentParser(description="Search OSINT Threats Database")
parser.add_argument("--keyword", help="Keyword to search in indicator/description")
parser.add_argument("--source", help="Filter by source")
parser.add_argument("--threat_type", help="Filter by threat type")
parser.add_argument("--from-date", help="Start date (YYYY-MM-DD)")
parser.add_argument("--to-date", help="End date (YYYY-MM-DD)")
parser.add_argument("--min-confidence", type=int, help="Minimum confidence score")
parser.add_argument("--sort-by", choices=["date_detected", "confidence"], help="Sort results by this field")
parser.add_argument("--desc", action="store_true", help="Sort descending")
parser.add_argument("--export", choices=["csv", "json"], help="Export results to file")
args = parser.parse_args()

# ----------------------------
# Build SQL Query
# ----------------------------
query = "SELECT id, source, threat_type, indicator, description, date_detected, confidence FROM threats WHERE 1=1"
params = []

if args.keyword:
    query += " AND (indicator LIKE ? OR description LIKE ?)"
    keyword = f"%{args.keyword}%"
    params.extend([keyword, keyword])

if args.source:
    query += " AND source = ?"
    params.append(args.source)

if args.threat_type:
    query += " AND threat_type = ?"
    params.append(args.threat_type)

if args.from_date:
    query += " AND date(date_detected) >= ?"
    params.append(args.from_date)

if args.to_date:
    query += " AND date(date_detected) <= ?"
    params.append(args.to_date)

if args.min_confidence is not None:
    query += " AND confidence >= ?"
    params.append(args.min_confidence)

# Sorting
if args.sort_by:
    query += f" ORDER BY {args.sort_by}"
    if args.desc:
        query += " DESC"
    else:
        query += " ASC"

# ----------------------------
# Execute Query
# ----------------------------
conn = sqlite3.connect("../database/osint_threats.db")
cursor = conn.cursor()

cursor.execute(query, params)
results = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]

df = pd.DataFrame(results, columns=columns)

# ----------------------------
# Display in Terminal
# ----------------------------
if df.empty:
    console.print("[bold yellow]No threats matched your query.[/bold yellow]")
else:
    table = Table(title="🔍 Threat Search Results", show_lines=True)

    for col in columns:
        table.add_column(col.replace("_", " ").title())

    for row in results:
        str_row = [str(item) if item is not None else "-" for item in row]
        table.add_row(*str_row)

    console.print(table)

# ----------------------------
# Export to File (Optional)
# ----------------------------
if args.export:
    os.makedirs("../results", exist_ok=True)
    export_path = f"../results/search_results_day14.{args.export}"

    if args.export == "csv":
        df.to_csv(export_path, index=False)
    elif args.export == "json":
        df.to_json(export_path, orient="records", indent=4)

    console.print(f"[green]✓ Exported to {export_path}[/green]")
