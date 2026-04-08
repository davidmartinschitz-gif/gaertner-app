import os
import sqlite3

# Absolute Pfade für deine externe SSD (E:)
BASE_DIR = r'E:'
DB_DIR = os.path.join(BASE_DIR, 'Database')
DB_PATH = os.path.join(DB_DIR, 'boden_austria.db')

# Sicherstellen, dass der Ordner auf E: existiert
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)
    print(f"Ordner erstellt: {DB_DIR}")

# Verbindung zur Datenbank herstellen
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Erstellen einer kombinierten Tabelle (Logischer für den Start)
cursor.execute('''CREATE TABLE IF NOT EXISTS boden_daten (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plz TEXT NOT NULL,
    bodentyp TEXT,
    humusgehalt REAL,
    bemerkung TEXT,
    kalkgehalt REAL
)''')

conn.commit()
conn.close()

print(f"ERFOLG: Tabelle 'boden_daten' erweitert unter: {DB_PATH}")