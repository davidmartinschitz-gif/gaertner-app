import streamlit as st
import sqlite3
import os
import pandas as pd
import difflib
import json
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

# --- 1. HYBRID-PFAD-LOGIK ---
# Prüfen, ob wir lokal auf dem PC arbeiten oder in der Cloud
IS_LOCAL = os.path.exists(r'E:\Database')

if IS_LOCAL:
    # Modus: Lokale Workstation (E: Laufwerk)
    DB_PATH = r'E:\Database\boden_austria.db'
    ATLAS_PATH = r'E:\Database\ebod_atlas.json'
    ENV_PATH = r'E:\Database\environment_history.json'
    BACKUP_INFO_PATH = r'E:\Database\last_backup.txt'
else:
    # Modus: Streamlit Cloud (Handy-Betrieb)
    DB_PATH = 'boden_austria_backup.db'
    ATLAS_PATH = 'ebod_atlas_backup.json'
    ENV_PATH = 'environment_history_backup.json'
    BACKUP_INFO_PATH = 'last_backup.txt'

# --- 2. CLOUD-SYNCHRONISIERUNG (DOWNLOAD) ---
def sync_from_drive():
    """Lädt die Dateien aus Google Drive in den Cloud-Speicher der App."""
    if IS_LOCAL:
        return True
    
    try:
        # Client Secrets aus Streamlit Secrets erstellen
        if not os.path.exists("client_secrets.json"):
            with open("client_secrets.json", "w") as f:
                f.write(st.secrets["google_drive"]["client_secrets"])
        
        gauth = GoogleAuth()
        # Automatisierte Anmeldung in der Cloud via credentials.json
        gauth.LoadCredentialsFile("credentials.json")
        if gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()

        gauth.SaveCredentialsFile("credentials.json")
        
        drive = GoogleDrive(gauth)
        
        # Dateien zum Herunterladen
        files = {
            "boden_austria_backup.db": DB_PATH,
            "ebod_atlas_backup.json": ATLAS_PATH,
            "environment_history_backup.json": ENV_PATH
        }
        
        for title, target in files.items():
            file_list = drive.ListFile({'q': f"title = '{title}' and trashed = false"}).GetList()
            if file_list:
                file_list[0].GetContentFile(target)
        return True
    except Exception as e:
        st.error(f"Cloud-Synchronisierungsfehler: {str(e)}")
        return False

# Initialer Sync beim Start in der Cloud
if not IS_LOCAL:
    sync_from_drive()

# --- 3. MODULE IMPORTIEREN ---
import plants_data
import history_module

# --- 4. BACKUP-LOGIK (UPLOAD) ---
def upload_all_to_drive():
    """Synchronisiert Daten und erzwingt ein dauerhaftes Ticket für die Cloud."""
    try:
        gauth = GoogleAuth()
        if IS_LOCAL:
            # Erzwingt, dass Google uns ein Refresh-Token gibt
            gauth.LocalWebserverAuth(auth_params={'access_type': 'offline', 'approval_prompt': 'force'})
            gauth.SaveCredentialsFile("credentials.json")
        else:
            gauth.LoadCredentialsFile("credentials.json")
            if gauth.access_token_expired:
                gauth.Refresh()
            else:
                gauth.Authorize()
            
        drive = GoogleDrive(gauth)

        # (Der restliche Upload-Teil bleibt gleich...)
        files_to_sync = {
            "boden_austria_backup.db": DB_PATH,
            "ebod_atlas_backup.json": ATLAS_PATH,
            "environment_history_backup.json": ENV_PATH
        }

        for title, local_path in files_to_sync.items():
            if not os.path.exists(local_path): continue
            query = f"title = '{title}' and trashed = false"
            file_list = drive.ListFile({'q': query}).GetList()
            file_drive = file_list[0] if file_list else drive.CreateFile({'title': title})
            file_drive.SetContentFile(local_path)
            file_drive.Upload()
        
        with open(BACKUP_INFO_PATH, 'w') as f:
            f.write(pd.Timestamp.now().strftime('%d.%m.%Y %H:%M:%S'))
            
        return True, "Ticket erneuert und Backup erstellt!"
    except Exception as e:
        return False, f"Fehler: {str(e)}"

# --- 5. LOGIK-FUNKTIONEN ---
def get_soil_status(plz_input):
    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH)
            row = conn.execute("SELECT kalkgehalt FROM boden_daten WHERE plz = ?", (plz_input,)).fetchone()
            conn.close()
            if row:
                return row[0] > 0, "Eigene Messung"
        except Exception:
            pass

    if os.path.exists(ATLAS_PATH):
        with open(ATLAS_PATH, 'r') as f:
            atlas = json.load(f)
            if plz_input in atlas:
                return atlas[plz_input] > 0, "eBOD-Prognose"
                
    return None, "Keine Daten"

# --- 6. STREAMLIT UI ---
st.set_page_config(page_title="Gärtner-Master 2026", page_icon="🌱", layout="wide")

st.sidebar.title("🌿 Navigation")
page = st.sidebar.radio("Menü:", ["Dashboard", "Pflanzen-Experte", "Boden-Verwaltung"])

if page == "Dashboard":
    st.title("🌱 Gärtner-Master Dashboard")
    st.write("Willkommen in deiner digitalen Garten-Zentrale.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Pflanzen im Lexikon", len(plants_data.PLANTS_REGISTRY))
    with col2:
        status_text = "✅ SSD-Datenbank bereit" if IS_LOCAL else "✅ Cloud-Mirror aktiv"
        if not os.path.exists(DB_PATH):
            status_text = "⚠️ Datenbank fehlt"
        st.success(status_text)
    with col3:
        st.info("☁️ Cloud-Lager: 5 TB verfügbar")

    st.divider()

    st.header("💾 Cloud-Synchronisation")
    st.write("Sichere deine lokale Datenbank und den eBOD-Atlas in dein Google Drive Hauptlager.")
    
    if st.button("Jetzt Komplett-Backup auf Google Drive erstellen"):
        with st.spinner("Synchronisiere Datenpakete..."):
            erfolg, nachricht = upload_all_to_drive()
            if erfolg:
                st.success(nachricht)
            else:
                st.error(nachricht)

    if os.path.exists(BACKUP_INFO_PATH):
        with open(BACKUP_INFO_PATH, 'r') as f:
            st.caption(f"Letztes erfolgreiches Backup: {f.read()}")

    st.divider()
    st.subheader("System-Details")
    st.write(f"Modus: {'Lokal' if IS_LOCAL else 'Cloud'}")
    st.write(f"Daten-Pfad: `{DB_PATH}`")
    st.write(f"Prozessor: AMD Ryzen 7 2700X | Lager: Intenso SSD")

elif page == "Pflanzen-Experte":
    # (Restlicher Code für Pflanzen-Experte bleibt identisch)
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
                        st.warning("⚠️ Zu windig!")
                    elif w_res == 'hoch':
                        st.success("✅ Standfest")
                    else:
                        st.info(f"ℹ️ Windfestigkeit: {w_res.capitalize()}")
                
                if "drought_tolerance" in info:
                    has_env_data = True
                    if env['drought_years'] >= 2 and info['drought_tolerance'] == 'gering':
                        st.warning("⚠️ Dürregefahr!")
                    elif info['drought_tolerance'] == 'hoch':
                        st.success("✅ Klimawandel-Gewinner")

                if not has_env_data:
                    st.info("ℹ️ Keine spezifischen Wind/Dürre-Daten.")

            with soil_col:
                st.markdown("### 🧪 Boden-Passung")
                has_lime, quelle = get_soil_status(plz)
                if has_lime is None:
                    st.warning(f"⚠️ Keine Bodendaten für PLZ {plz}.")
                else:
                    st.caption(f"Quelle: {quelle}")
                    needs_acid = info.get("needs_acid_soil", False)
                    if needs_acid and has_lime:
                        st.error("❌ KALK-KONFLIKT")
                    elif needs_acid and not has_lime:
                        st.success("✅ MOORBEET-CHECK")
                    elif not needs_acid and has_lime:
                        st.success("✅ KALK-TOLERANZ")
                    else:
                        st.success("✅ BODEN-PASSUNG")

elif page == "Boden-Verwaltung":
    st.title("📊 Boden-Datenbank")
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM boden_daten", conn)
        conn.close()
        st.dataframe(df)
        st.bar_chart(df.set_index('plz')['kalkgehalt'])