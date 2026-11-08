"""
==============================================================================
Module:      data_processor.py
Description: Hourly aggregation and text serialization for weather metrics.
==============================================================================
"""

import os
from typing import List, Dict, Any


def calculate_average_wind_speed(day_data: Dict[str, Any]) -> float:
    """Berechnet die durchschnittliche Windgeschwindigkeit aus stündlichen Messungen."""
    hours = day_data.get("hours", [])
    if not hours:
        return round(float(day_data.get("windspeed", 0.0)), 1)

    total_speed = sum(h.get("windspeed", 0.0) for h in hours)
    return round(total_speed / len(hours), 1)


def export_weather_series_to_txt(filepath: str, days_data: List[Dict[str, Any]], append: bool = False) -> int:
    """
    Schreibt Wettertage im Format 'YYYYMMDD Temp Wind' in eine Textdatei.
    Gibt die Anzahl der geschriebenen Datensätze zurück.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    mode = "a" if append else "w"

    written_count = 0
    with open(filepath, mode, encoding="utf-8") as file:
        for day in days_data:
            raw_date = day.get("datetime", "").replace("-", "")
            avg_temp = round(float(day.get("temp", 0.0)), 1)
            avg_wind = calculate_average_wind_speed(day)

            file.write(f"{raw_date} {avg_temp} {avg_wind}\n")
            written_count += 1

    return written_count
