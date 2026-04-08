import streamlit as st
import sqlite3
import os
import pandas as pd
import difflib
import json

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

def upload_all_to_drive():
    """Synchronisiert alle wichtigen Daten und verhindert Duplikate."""
    try:
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth() 
        drive = GoogleDrive(gauth)

        # Liste aller Dateien, die ins 5-TB-Lager gehören
        files_to_sync = {
            "boden_austria_backup.db": DB_PATH,
            "ebod_atlas_backup.json": ATLAS_PATH,
            "environment_history_backup.json": r'E:\Database\environment_history.json',
            "official_restrictions_backup.csv": r'E:\Database\official_restrictions.csv'
        }

        for title, local_path in files_to_sync.items():
            if not os.path.exists(local_path):
                continue
            
            # 🔍 Suche: Existiert diese Datei bereits im Drive?
            query = f"title = '{title}' and trashed = false"
            file_list = drive.ListFile({'q': query}).GetList()
            
            if file_list:
                # Falls ja: Nutze die existierende Datei (Update)
                file_drive = file_list[0]
                status_msg = "aktualisiert"
            else:
                # Falls nein: Erstelle einen neuen Eintrag
                file_drive = drive.CreateFile({'title': title})
                status_msg = "neu erstellt"
            
            file_drive.SetContentFile(local_path)
            file_drive.Upload()
            print(f"Cloud-Sync: {title} wurde {status_msg}.")
        
        return True, "Alle Systeme (Datenbank, eBOD, Umwelt & Recht) sind jetzt in der Cloud auf dem neuesten Stand."
    except Exception as e:
        return False, f"Synchronisations-Fehler: {str(e)}"

# --- 1. HYBRID-PFAD-LOGIK ---
# Wir prüfen, ob dein Laufwerk E: existiert (dann sind wir bei dir zu Hause)
IS_LOCAL = os.path.exists(r'E:\Database')

if IS_LOCAL:
    # Modus: AMD Ryzen 7 2700X Workstation
    DB_PATH = r'E:\Database\boden_austria.db'
    ATLAS_PATH = r'E:\Database\ebod_atlas.json'
    # Falls history_module den Pfad braucht, definieren wir ihn hier mit
    ENV_PATH = r'E:\Database\environment_history.json'
else:
    # Modus: Streamlit Cloud (Handy-Betrieb)
    # Hier liegen die Dateien direkt im App-Ordner (heruntergeladen aus dem Drive)
    DB_PATH = 'boden_austria_backup.db'
    ATLAS_PATH = 'ebod_atlas_backup.json'
    ENV_PATH = 'environment_history_backup.json'

# --- 2. MODULE IMPORTIEREN ---
import plants_data
import history_module

# --- 3. LOGIK-FUNKTIONEN ---
def get_soil_status(plz_input):
    """Prüft erst eigene Daten (SSD oder Cloud-Mirror), dann den eBOD-Atlas."""
    # Check 1: Eigene Datenbank
    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH)
            row = conn.execute("SELECT kalkgehalt FROM boden_daten WHERE plz = ?", (plz_input,)).fetchone()
            conn.close()
            if row:
                return row[0] > 0, "Eigene Messung"
        except Exception:
            pass # Falls die DB in der Cloud noch nicht bereit ist

    # Check 2: eBOD Atlas (JSON-Datei)
    if os.path.exists(ATLAS_PATH):
        with open(ATLAS_PATH, 'r') as f:
            atlas = json.load(f)
            if plz_input in atlas:
                return atlas[plz_input] > 0, "eBOD-Prognose"
                
    return None, "Keine Daten"

# --- 4. STREAMLIT UI ---
st.set_page_config(page_title="Gärtner-Master 2026", page_icon="🌱", layout="wide")

st.sidebar.title("🌿 Navigation")
page = st.sidebar.radio("Menü:", ["Dashboard", "Pflanzen-Experte", "Boden-Verwaltung"])

if page == "Dashboard":
    st.title("🌱 Gärtner-Master Dashboard")
    st.write("Willkommen in deiner digitalen Garten-Zentrale.")
    
    # Status-Kacheln (Jetzt mit 3 Spalten für mehr Übersicht)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Pflanzen im Lexikon", len(plants_data.PLANTS_REGISTRY))
    with col2:
        st.success("✅ SSD-Datenbank bereit" if os.path.exists(DB_PATH) else "⚠️ Datenbank fehlt")
    with col3:
        st.info("☁️ Cloud-Lager: 5 TB verfügbar")

    st.divider()

    # --- DIE CLOUD-SEKTION (Das ist der neue Teil!) ---
    st.header("💾 Cloud-Synchronisation")
    st.write("Sichere deine lokale Datenbank und den eBOD-Atlas in dein Google Drive Hauptlager.")
    
    if st.button("Jetzt Komplett-Backup auf Google Drive erstellen"):
        with st.spinner("Alle Datenpakete werden geschnürt und synchronisiert..."):
            erfolg, nachricht = upload_all_to_drive() # Hier den neuen Funktionsnamen nutzen
            if erfolg:
                st.success(nachricht)
            else:
                st.error(nachricht)

    st.divider()
    st.subheader("System-Details")
    st.write(f"Lokaler Pfad: `{DB_PATH}`")
    st.write(f"Prozessor: AMD Ryzen 7 2700X | Lager: Intenso SSD")
elif page == "Pflanzen-Experte":
    st.title("🔍 Intelligenter Pflanzen-Check")
    
    col_a, col_b = st.columns(2)
    with col_a:
        plz = st.text_input("PLZ für Wetter-Check:", value="8160")
    with col_b:
        query = st.text_input("Welche Pflanze möchtest du prüfen?")

    if query:
        all_names = []
        name_to_id = {}
        for p_id, info in plants_data.PLANTS_REGISTRY.items():
            all_names.extend([info['de'], info['lat']])
            name_to_id[info['de']] = p_id
            name_to_id[info['lat']] = p_id

        matches = difflib.get_close_matches(query, all_names, n=3, cutoff=0.5)

        if not matches:
            st.error(f"Keine Treffer für '{query}' gefunden.")
        else:
            selected_name = st.selectbox("Meintest du eine dieser Pflanzen?", matches)
            p_id = name_to_id[selected_name]
            info = plants_data.PLANTS_REGISTRY[p_id]
            
            st.divider()
            st.subheader(f"Analyse für: {info['de']} ({info['lat']})")
            
            # Gärtner-Notiz anzeigen
            if "note" in info:
                st.info(f"💡 **Gärtner-Tipp:** {info['note']}")

            if "restriction" in info:
                st.warning(f"⚠️ **Einschränkung:** {info['restriction']}")

            res_col, env_col, soil_col = st.columns(3)
            
            with res_col:
                st.markdown("### 📍 Standort & Recht")
                st.write(plants_data.check_plant(p_id, True))
            
            with env_col:
                st.markdown("### 💨 Umwelt & Klima")
                env = history_module.get_environmental_history(plz)
                has_env_data = False
                
                if "wind_resistence" in info:
                    has_env_data = True
                    w_res = info['wind_resistence']
                    
                    if env['wind'] == 'stark' and w_res == 'gering':
                        st.warning("⚠️ Zu windig für diese Sorte!")
                    elif w_res == 'hoch':
                        st.success("✅ Standfest bei Sturm")
                    else:
                        # Das fängt jetzt 'mittel' ab
                        st.info(f"ℹ️ Windfestigkeit: {w_res.capitalize()}")
                
                if "drought_tolerance" in info:
                    has_env_data = True
                    if env['drought_years'] >= 2 and info['drought_tolerance'] == 'gering':
                        st.warning("⚠️ Dürregefahr! Hoher Wasserbedarf.")
                    elif info['drought_tolerance'] == 'hoch':
                        st.success("✅ Klimawandel-Gewinner")

                if not has_env_data:
                    st.info("ℹ️ Keine spezifischen Wind/Dürre-Daten hinterlegt.")

            with soil_col:
                st.markdown("### 🧪 Boden-Passung")
                has_lime, quelle = get_soil_status(plz)
                
                if has_lime is None:
                    # Hier leuchtet es gelb, wenn keine Daten da sind
                    st.warning(f"⚠️ Keine Bodendaten für PLZ {plz} vorhanden.")
                else:
                    st.caption(f"Quelle: {quelle}")
                    needs_acid = info.get("needs_acid_soil", False)
                    
                    # Szenario 1: Pflanze braucht sauer, Boden hat Kalk
                    if needs_acid and has_lime:
                        st.error("❌ KALK-KONFLIKT: Diese Pflanze braucht sauren Boden (pH 4-5.5). Dein Boden ist zu kalkhaltig.")
                    
                    # Szenario 2: Pflanze braucht sauer, Boden ist kalkfrei
                    elif needs_acid and not has_lime:
                        st.success("✅ MOORBEET-CHECK: Perfekt! Saurer Boden für Moorbeetpflanze.")
                    
                    # Szenario 3: Pflanze braucht KEINEN sauren Boden, Boden hat Kalk (Das ist der neue Punkt!)
                    elif not needs_acid and has_lime:
                        st.success("✅ KALK-TOLERANZ: Diese Pflanze liebt oder toleriert Kalkgehalt.")
                    
                    # Szenario 4: Pflanze braucht KEINEN sauren Boden, Boden ist neutral/sauer
                    else:
                        st.success("✅ BODEN-PASSUNG: Neutraler Boden ist für diese Pflanze ideal.")

elif page == "Boden-Verwaltung":
    st.title("📊 Boden-Datenbank")
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM boden_daten", conn)
        conn.close()
        st.dataframe(df)
        st.bar_chart(df.set_index('plz')['kalkgehalt'])