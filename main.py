"""
==============================================================================
Project:     Visual Crossing Weather Harvester & Historical ETL Pipeline
File:        main.py
Author:      Yevhen Biezhyn
Description: Unified CLI orchestrator collecting historical meteorological
             time series, computing daily aggregations, and saving structured files.
==============================================================================
"""

import os
import json
import argparse
from typing import List, Dict, Any

from modules.api_client import VisualCrossingClient
from modules.data_processor import export_weather_series_to_txt


def load_target_configurations(config_path: str) -> List[Dict[str, Any]]:
    """Lädt die Liste der Städte und Zielzeiträume."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Konfigurationsdatei '{config_path}' nicht gefunden.")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description="Visual Crossing Weather Harvester CLI",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default=os.getenv("VISUAL_CROSSING_API_KEY"),
        help="Visual Crossing API Key (kann auch über VISUAL_CROSSING_API_KEY gesetzt werden)"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config/targets.json",
        help="Pfad zur JSON-Konfiguration mit Zielstädten und Zeiträumen"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="data",
        help="Zielordner für die generierten .txt-Dateien (Standard: data)"
    )
    args = parser.parse_args()

    print("=" * 78)
    print("  VISUAL CROSSING WEATHER HARVESTER | HISTORICAL ETL PIPELINE")
    print("=" * 78)

    api_key = args.api_key
    if not api_key:
        print("[!] WARNUNG: Kein API-Schlüssel übergeben.")
        print("    Setzen Sie --api-key <KEY> oder die Umgebungsvariable VISUAL_CROSSING_API_KEY.")
        return

    client = VisualCrossingClient(api_key=api_key)
    targets = load_target_configurations(args.config)

    for item in targets:
        city = item["city"]
        intervals = item.get("intervals", [])
        output_file = os.path.join(args.output_dir, f"{city}_weather_data.txt")

        print(f"\n[*] Verarbeite Station: {city} ({len(intervals)} Zeitintervalle)...")

        # Datei zu Beginn für die jeweilige Stadt zurücksetzen
        if os.path.exists(output_file):
            os.remove(output_file)

        total_days = 0
        for interval in intervals:
            start_d = interval["start_date"]
            end_d = interval["end_date"]
            print(f"    - Lade Intervall {start_d} bis {end_d}...")

            days_data = client.fetch_historical_weather(city, start_d, end_d)
            if days_data:
                written = export_weather_series_to_txt(output_file, days_data, append=True)
                total_days += written

        print(f"[+] Fertiggestellt: {city} -> {total_days} Datensätze in '{output_file}' exportiert.")

    print("\n" + "=" * 78)
    print("  DATENERFASSUNG ERFOLGREICH BEENDET.")
    print("=" * 78 + "\n")


if __name__ == "__main__":
    main()
