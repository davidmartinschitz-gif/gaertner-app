import os
import sqlite3

# Absolute paths for your external SSD (E:)
BASE_DIR = r'E:'
DB_DIR = os.path.join(BASE_DIR, 'Database')
DB_PATH = r'E:\Database\boden_austria.db'

def insert_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("--- Boden-App Dateneingabe (eBOD Projekt) ---")
    print("Tippe 'exit' bei der PLZ, um das Programm zu beenden.\n")

    while True:
        zip_code = input("PLZ eingeben: ")
        if zip_code.lower() == 'exit':
            break
        
        soil_type = input("Bodentyp (z.B. Braunerde): ")
        
        try:
            humus_content = float(input("Humusgehalt in % (z.B. 2.5): "))
            lime_content = float(input("Kalkgehalt in % (z.B. 1.0): "))
        except ValueError:
            print("Fehler: Bitte Zahlen mit Punkt statt Komma eingeben!")
            continue

        # SQL Insert with English variable names
        cursor.execute('''
            INSERT INTO boden_daten (plz, bodentyp, humusgehalt, kalkgehalt) 
            VALUES (?, ?, ?, ?)
        ''', (zip_code, soil_type, humus_content, lime_content))
        
        conn.commit()
        print("✓ Datensatz erfolgreich auf SSD gespeichert.\n")

    print("\n--- Aktuelle Datenbank-Einträge auf E: ---")
    cursor.execute("SELECT * FROM boden_daten")
    records = cursor.fetchall()

    for row in records:
        print(row)

    conn.close()

if __name__ == "__main__":
    insert_data()