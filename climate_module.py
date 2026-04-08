# climate_module.py - Verknüpfung von Klima und Pflanzen
import plants_data # Wir holen uns das Pflanzen-Wissen

# Datenbank für Winterhärtezonen
WHZ_DATA = {
    "9184": 7, # Zone 7
    "8160": 7, # Zone 7
    "1010": 8, # Zone 8
    "6020": 7, # Zone 7
}

def climate_main():
    print("\n" + "="*40)
    print("      KLIMACHECK & PFLANZEN-PROGNOSE")
    print("="*40)
    
    zip_code = input("PLZ eingeben (oder GPS-Sim mit 'G'): ")
    
    # Simulation der GPS-Logik für später
    if zip_code.upper() == 'G':
        print("[GPS-Simulation] Koordinaten ermittelt... PLZ 8160 erkannt.")
        zip_code = "8160"

    current_zone = WHZ_DATA.get(zip_code)

    if current_zone:
        print(f"\nErgebnis für PLZ {zip_code}:")
        print(f"Deine Winterhärtezone ist: {current_zone}")
        
        # Jetzt prüfen wir eine Beispiel-Pflanze aus deiner Liste
        print("\n--- Check der Hecken-Favoriten ---")
        plant_to_check = "Kirschlorbeer" # Test-Pflanze
        
        # Hier rufen wir die Logik aus deinem anderen Modul auf
        # Wir simulieren: Ist es ein Schutzgebiet? (Hier mal True für die Steiermark)
        result = plants_data.check_plant(plant_to_check, is_protection_area=True)
        print(f"Pflanze: {plant_to_check}")
        print(f"Status:  {result}")
        
    else:
        print("\nPLZ noch nicht in der Klima-Datenbank.")

    input("\nDrücke Enter für das Hauptmenü...")