import os
import sqlite3
import subprocess
import fetch_official_data # Importiert dein Download-Skript
import plant_search_module # Importiert die neue Suche

# Pfad zur Datenbank auf deiner SSD
DB_PATH = r'E:\Database\boden_austria.db'

def show_all_entries():
    """Liest und zeigt alle Datensätze aus der SQLite-Datenbank an."""
    if not os.path.exists(DB_PATH):
        print(f"\nFehler: Datenbank unter {DB_PATH} nicht gefunden.")
        return

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    try:
        cursor.execute("SELECT * FROM boden_daten")
        records = cursor.fetchall()
        
        print("\n--- Alle gespeicherten Bodendaten ---")
        if not records:
            print("Noch keine Einträge vorhanden.")
        for row in records:
            print(f"ID: {row[0]} | PLZ: {row[1]} | Typ: {row[2]} | Humus: {row[3]}% | Kalk: {row[4]}%")
    except sqlite3.OperationalError as e:
        print(f"\nFehler beim Lesen der Datenbank: {e}")
    finally:
        connection.close()

def main():
    """Hauptschleife des Gärtner-App Menüs."""
    while True:
        print("\n========================================")
        print("      GÄRTNER-APP HAUPTMENÜ")
        print("========================================")
        print("1. [Boden-Daten] Neuen Eintrag erstellen")
        print("2. [Boden-Daten] Alle Einträge anzeigen")
        print("3. [Klimacheck] Winterhärtezone abfragen")
        print("4. [Pflanz-Check] Suche & Standort-Warnungen")
        print("5. [Historie] Wind- & Umweltdaten (PLZ-Check)") # NEU
        print("6. [Update] Offizielle Listen aktualisieren")
        print("7. Programm beenden")
        print("----------------------------------------")
        
        choice = input("Deine Wahl (1-7): ")

        if choice == '1':
            # Startet das Skript zur Dateneingabe
            subprocess.run(["python", "E:\\Development\\insert_boden_data.py"])
        
        elif choice == '2':
            show_all_entries()
            
        elif choice == '3':
            import climate_module
            climate_module.climate_main()
            
        elif choice == '4':
            # Startet das neue Such-Modul (wir simulieren hier ein Schutzgebiet für die Tests)
            plant_search_module.search_main(is_protection_area=True)
            
        elif choice == '5':
            import history_module
            plz = input("Für welche PLZ soll die Historie geprüft werden? ")
            history_module.show_history_analysis(plz)

        elif choice == '6':
            # Ruft jetzt BEIDE Update-Funktionen nacheinander auf
            fetch_official_data.download_protection_zones()
            fetch_official_data.update_environmental_data()
            
        elif choice == '7':
            print("Programm wird beendet. Frohes Gärtnern!")
            break
        
        else:
            print("Ungültige Eingabe. Bitte wähle 1-6.")

# --- DIESER TEIL IST DER ZÜNDSCHLÜSSEL ---
if __name__ == "__main__":
    main()