#!/bin/bash
set -e

echo "[INFO] OSINT Threat Intelligence Container Entry Point"

# Start Tor in the background
echo "[INFO] Starting Tor..."
tor &

sleep 5  # Give Tor some time to bootstrap

MODE=${MODE:-dashboard}

if [ "$MODE" = "dashboard" ]; then
    if [ ! -f "/app/data/unified_threat_dataset.csv" ]; then
        echo "[ERROR] Unified dataset not found in /app/data. Run merge script first."
        exit 1
    fi
    echo "[INFO] Starting Dashboard..."
    python scripts/day11_dashboard.py
elif [ "$MODE" = "pipeline" ]; then
    echo "[INFO] Running Full Pipeline..."
    python scripts/day9_10_pipeline_advanced.py
elif [ "$MODE" = "both" ]; then
    echo "[INFO] Running Pipeline + Dashboard..."
    python scripts/day9_10_pipeline_advanced.py && python scripts/day11_dashboard.py
else
    echo "[ERROR] Unknown MODE: $MODE"
    exit 1
fi
