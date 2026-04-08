import os
import sqlite3

# Absolute Pfade für deine externe SSD (E:)
BASE_DIR = r'E:'
DB_DIR = r'E:\Database'
DB_PATH = r'E:\Database\boden_austria.db'

# Sicherstellen, dass der Ordner auf E: existiert
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)
    print(f"Ordner erstellt: {DB_DIR}")

# Verbindung zur Datenbank herstellen
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Tabelle mit ALLEN notwendigen Spalten erstellen
cursor.execute('''
CREATE TABLE IF NOT EXISTS boden_daten (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plz TEXT NOT NULL,
    bodentyp TEXT,
    humusgehalt REAL,
    kalkgehalt REAL,
    bemerkung TEXT
)
''')

conn.commit()
conn.close()

print(f"ERFOLG: Saubere Datenbank (inkl. Kalkgehalt) erstellt unter: {DB_PATH}")