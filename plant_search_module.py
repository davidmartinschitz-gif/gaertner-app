# plant_search_module.py - Die Master-Check Zentrale
import plants_data
import history_module
import sqlite3
import os
import difflib

# Pfad zur Datenbank auf deiner Intenso SSD
DB_PATH = r'E:\Database\boden_austria.db'

def check_user_kalk():
    """Prüft in der echten Datenbank auf E:, ob Kalk vorhanden ist."""
    if not os.path.exists(DB_PATH): return False
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.execute("SELECT kalkgehalt FROM boden_daten LIMIT 1")
        row = cursor.fetchone()
        return row and row[0] > 0
    except: return False
    finally: conn.close()

def search_main(is_protection_area=True):
    user_has_lime = check_user_kalk()
    
    # Einmalige Abfrage der PLZ für diesen Such-Durchgang
    print("\n" + "~"*50)
    current_zip = input("Für welche PLZ soll der Master-Check laufen? ").strip()
    env_history = history_module.get_environmental_history(current_zip)
    
    while True:
        print("\n" + "="*50)
        print(f"      MASTER-CHECK: STANDORT {current_zip}")
        print("="*50)
        query = input("Pflanzenname oder '3' für Zurück: ").strip().lower()
        if query == '3': break
        if len(query) < 2: continue

        # 1. Suche & Auswahl (Fuzzy Search)
        matches = [p_id for p_id, info in plants_data.PLANTS_REGISTRY.items() 
                   if query in info['de'].lower() or query in info['lat'].lower()]

        if not matches:
            all_names = []
            name_to_id = {}
            for p_id, info in plants_data.PLANTS_REGISTRY.items():
                all_names.append(info['de'])
                all_names.append(info['lat'])
                name_to_id[info['de']] = p_id
                name_to_id[info['lat']] = p_id

            suggestions = difflib.get_close_matches(query, all_names, n=1, cutoff=0.6)
            if suggestions:
                print(f"Meintest du: {suggestions[0]}?")
                continue
            print("❌ Kein Treffer.")
            continue

        # Wenn mehrere Treffer (z.B. Ahorn), nimm den ersten oder biete Auswahl
        selected_id = matches[0]

        # 2. DIE HARMONISIERUNGS-LOGIK
        info = plants_data.PLANTS_REGISTRY[selected_id]
        print(f"\n" + "*"*45)
        print(f"ANALYSE: {info['de'].upper()} ({info['lat']})")
        print(f"*"*45)
        
        # A) Standort- & Feuerbrand-Check
        print(f"📍 Standort-Regel: {plants_data.check_plant(selected_id, is_protection_area)}")
        
        # B) Boden-Check (Kalk)
        if info.get("needs_acid_soil") and user_has_lime:
            print("❌ BODEN-KONFLIKT: Kalkhaltiger Boden auf E: erkannt! Nicht pflanzen.")
        else:
            print("✅ BODEN-CHECK: Bodenbeschaffenheit ist in Ordnung.")

        # C) Wind-Check
        if env_history['wind'] == 'stark' and info.get('wind_resistence') == 'gering':
            print(f"⚠️ WIND-WARNUNG: PLZ {current_zip} ist stürmisch, Pflanze zu instabil!")
        elif env_history['wind'] == 'stark' and info.get('wind_resistence') == 'hoch':
            print(f"✅ WIND-STABIL: Pflanze hält dem Wind an diesem Standort stand.")
        else:
            print("ℹ️ WIND-INFO: Keine besonderen Wind-Risiken bekannt.")

        # D) Trockenheits-Check
        if env_history['drought_years'] >= 2 and info.get('drought_tolerance') == 'gering':
            print(f"⚠️ TROCKEN-ALARM: Historische Dürregefahr! Pflanze braucht zu viel Wasser.")
        elif info.get('drought_tolerance') == 'hoch':
            print(f"✅ KLIMA-RESILIENZ: Ein echter Klimawandel-Gewinner.")

        print("-" * 50)