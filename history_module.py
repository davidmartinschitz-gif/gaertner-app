import json
import os

DATA_FILE = r'E:\Database\environment_history.json'

def get_environmental_history(zip_code):
    # Falls die Datei existiert (nach einem Update), laden wir sie
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get(zip_code, {"wind": "unbekannt", "drought_years": 0, "heat_index": "normal"})
    
    # Fallback: Wenn noch nie ein Update gemacht wurde (Simulation)
    mock_data = {
        "8160": {"wind": "stark", "drought_years": 3, "heat_index": "hoch"},
        "1010": {"wind": "mittel", "drought_years": 1, "heat_index": "extrem"}
    }
    return mock_data.get(zip_code, {"wind": "unbekannt", "drought_years": 0, "heat_index": "normal"})

def show_history_analysis(zip_code):
    data = get_environmental_history(zip_code)
    print(f"\n" + "~"*40)
    print(f"🌍 UMWELT-HISTORIE ANALYSE: PLZ {zip_code}")
    print(f"~"*40)
    print(f"💨 Wind-Risiko:      {data['wind'].upper()}")
    print(f"🔥 Trocken-Stress:   {data['drought_years']} extreme Jahre")
    print(f"☀️ Hitze-Potenzial:  {data['heat_index'].upper()}")
    print("-" * 40)