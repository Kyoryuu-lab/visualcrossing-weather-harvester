"""
==============================================================================
Module:      api_client.py
Description: HTTP REST client for Visual Crossing Weather Timeline API.
==============================================================================
"""

import requests
from typing import Optional, List, Dict, Any


class VisualCrossingClient:
    """Verwaltet Abfragen an die Visual Crossing Weather API."""

    BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Ein gültiger Visual Crossing API-Schlüssel ist erforderlich.")
        self.api_key = api_key

    def fetch_historical_weather(self, city: str, start_date: str, end_date: str) -> Optional[List[Dict[str, Any]]]:
        """
        Ruft stündliche Wetterdaten für eine Stadt im Zeitraum [start_date, end_date] ab.
        Datumsformat: YYYY-MM-DD
        """
        url = f"{self.BASE_URL}/{city}/{start_date}/{end_date}"
        params = {
            "unitGroup": "metric",
            "key": self.api_key,
            "include": "hours"
        }

        try:
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                payload = response.json()
                return payload.get("days", [])
            else:
                print(f"[!] API-Fehler {response.status_code} für {city} ({start_date} bis {end_date}): {response.text}")
                return None
        except requests.RequestException as e:
            print(f"[!] Netzwerkfehler beim Abruf für {city}: {e}")
            return None
