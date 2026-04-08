import requests
import os
import json

# Pfade auf deiner Intenso SSD
RESTRICTION_PATH = r'E:\Database\official_restrictions.csv'
HISTORY_PATH = r'E:\Database\environment_history.json'
EBOD_PATH = r'E:\Database\ebod_atlas.json'

def download_protection_zones():
    """Lädt offizielle Feuerbrand-Daten (Simulation)."""
    url = "https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv"
    print("\n--- [1/3] Offizielle Verbotszonen (CSV) ---")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(RESTRICTION_PATH, 'wb') as file:
            file.write(response.content)
        print(f"✓ ERFOLG: Liste gespeichert.")
    except Exception as e:
        print(f"❌ FEHLER beim CSV-Download: {e}")

def update_environmental_data():
    """Speichert Windlast- & Umwelt-Historie."""
    print("\n--- [2/3] Windlast- & Umwelt-Paket (JSON) ---")
    # Jetzt mit 4020 (Linz) ergänzt!
    env_data = {
        "8160": {"wind": "stark", "drought_years": 3, "heat_index": "hoch"},
        "8010": {"wind": "mittel", "drought_years": 2, "heat_index": "hoch"},
        "1010": {"wind": "mittel", "drought_years": 1, "heat_index": "extrem"},
        "6020": {"wind": "stark", "drought_years": 0, "heat_index": "normal"},
        "4020": {"wind": "mittel", "drought_years": 0, "heat_index": "mittel"} # Neu!
    }
    try:
        with open(HISTORY_PATH, 'w', encoding='utf-8') as f:
            json.dump(env_data, f, indent=4)
        print(f"✅ ERFOLG: Umwelt-Paket unter {HISTORY_PATH} aktualisiert.")
    except Exception as e:
        print(f"❌ FEHLER beim Speichern: {e}")

def update_ebod_atlas():
    """Speichert den eBOD Boden-Atlas."""
    print("\n--- [3/3] eBOD Boden-Atlas (JSON) ---")
    ebod_data = {
        "8160": 1, "8010": 1, "1010": 1, "4020": 0, 
        "6020": 1, "5020": 1, "9020": 0, "7000": 1
    }
    try:
        with open(EBOD_PATH, 'w', encoding='utf-8') as f:
            json.dump(ebod_data, f, indent=4)
        print(f"✅ ERFOLG: eBOD-Atlas unter {EBOD_PATH} aktualisiert.")
    except Exception as e:
        print(f"❌ FEHLER beim Speichern: {e}")

if __name__ == "__main__":
    download_protection_zones()
    update_environmental_data()
    update_ebod_atlas()