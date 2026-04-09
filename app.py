import streamlit as st
import sqlite3
import os
import pandas as pd
import difflib
import json
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import h3  # Falls noch nicht oben, hier einmalig ergänzen

# 1. Standort-Daten aus dem Gedächtnis oder Home-Base holen
# (Nutze hier die Koordinaten, die wir für Preding fixiert haben)
lat_now, lon_now = 47.19897, 15.64720
import h3

current_hex = h3.latlng_to_cell(lat_now, lon_now, 11)

# 2. JSON-Datenbank laden
if os.path.exists("ebod_atlas_backup.json"):
    with open("ebod_atlas_backup.json", "r", encoding="utf-8") as f:
        ebod_db = json.load(f)
else:
    ebod_db = {}

# 3. Aktuellen Boden-Status im Session State speichern
if current_hex in ebod_db:
    st.session_state.active_soil = ebod_db[current_hex]
else:
    st.session_state.active_soil = None

# --- 1. HYBRID-PFAD-LOGIK ---
# Prüfen, ob wir lokal auf dem PC arbeiten oder in der Cloud
IS_LOCAL = os.path.exists(r"E:\Database")

if IS_LOCAL:
    # Modus: Lokale Workstation (E: Laufwerk)
    DB_PATH = r"E:\Database\boden_austria.db"
    ATLAS_PATH = r"E:\Database\ebod_atlas.json"
    ENV_PATH = r"E:\Database\environment_history.json"
    BACKUP_INFO_PATH = r"E:\Database\last_backup.txt"
else:
    # Modus: Streamlit Cloud (Handy-Betrieb)
    DB_PATH = "boden_austria_backup.db"
    ATLAS_PATH = "ebod_atlas_backup.json"
    ENV_PATH = "environment_history_backup.json"
    BACKUP_INFO_PATH = "last_backup.txt"


# --- 1. HELFER: GOOGLE DRIVE VERBINDUNG ---
def get_drive_instance():
    """Erstellt eine Google Drive Verbindung für Lokal oder Cloud."""
    gauth = GoogleAuth()

    if IS_LOCAL:
        # Lokal: Nutze deine Dateien auf der SSD
        gauth.LoadClientConfigFile("client_secrets.json")
        gauth.LocalWebserverAuth()
        gauth.SaveCredentialsFile("credentials.json")
    else:
        # Cloud: Nutze die Daten aus dem Streamlit-Tresor
        if "google_drive" in st.secrets:
            with open("client_secrets.json", "w") as f:
                f.write(st.secrets["google_drive"]["client_secrets"])
            gauth.LoadClientConfigFile("client_secrets.json")

            from oauth2client.client import GoogleCredentials

            gauth.credentials = GoogleCredentials.from_json(
                st.secrets["google_drive"]["credentials"]
            )
        else:
            st.error("Google Drive Secrets fehlen in Streamlit Cloud!")
            return None

    return GoogleDrive(gauth)


# --- 2. MODULE & INITIALER SYNC ---
import plants_data
import history_module


def sync_from_drive():
    """Lädt die neuesten Daten aus der Cloud auf den PC/Server."""
    try:
        drive = get_drive_instance()
        if not drive:
            return False

        files = {
            "boden_austria_backup.db": DB_PATH,
            "ebod_atlas_backup.json": ATLAS_PATH,
            "environment_history_backup.json": ENV_PATH,
        }

        for title, target in files.items():
            file_list = drive.ListFile(
                {"q": f"title = '{title}' and trashed = false"}
            ).GetList()
            if file_list:
                file_list[0].GetContentFile(target)
        return True
    except Exception as e:
        st.error(f"Download-Fehler: {e}")
        return False


# Automatischer Start-Sync in der Cloud
if not IS_LOCAL:
    sync_from_drive()


# --- 3. BACKUP-LOGIK (UPLOAD) ---
def upload_all_to_drive():
    """Sichert den aktuellen Stand vom PC/Handy in die Google Cloud."""
    try:
        drive = get_drive_instance()
        if not drive:
            return False, "Kein Zugriff auf Google Drive"

        files_to_sync = {
            "boden_austria_backup.db": DB_PATH,
            "ebod_atlas_backup.json": ATLAS_PATH,
            "environment_history_backup.json": ENV_PATH,
        }

        for title, local_path in files_to_sync.items():
            if not os.path.exists(local_path):
                continue

            query = f"title = '{title}' and trashed = false"
            file_list = drive.ListFile({"q": query}).GetList()

            # Entweder existierende Datei updaten oder neue erstellen
            file_drive = (
                file_list[0] if file_list else drive.CreateFile({"title": title})
            )
            file_drive.SetContentFile(local_path)
            file_drive.Upload()

        # Zeitstempel für das UI speichern
        with open(BACKUP_INFO_PATH, "w") as f:
            f.write(pd.Timestamp.now().strftime("%d.%m.%Y %H:%M:%S"))

        return True, "Cloud-Backup erfolgreich erstellt!"

    except Exception as e:
        return False, f"Fehler beim Upload: {str(e)}"


# --- 5. LOGIK-FUNKTIONEN ---
def get_soil_status(plz_input):
    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH)
            row = conn.execute(
                "SELECT kalkgehalt FROM boden_daten WHERE plz = ?", (plz_input,)
            ).fetchone()
            conn.close()
            if row:
                return row[0] > 0, "Eigene Messung"
        except Exception:
            pass

    if os.path.exists(ATLAS_PATH):
        with open(ATLAS_PATH, "r") as f:
            atlas = json.load(f)
            if plz_input in atlas:
                return atlas[plz_input] > 0, "eBOD-Prognose"

    return None, "Keine Daten"


# --- 6. STREAMLIT UI ---
st.set_page_config(page_title="Gärtner-Master 2026", page_icon="🌱", layout="wide")

st.sidebar.title("🌿 Navigation")
page = st.sidebar.radio(
    "Menü:", ["Dashboard", "Pflanzen-Experte", "Boden-Verwaltung", "Garten-Karte"]
)

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
    st.write(
        "Sichere deine lokale Datenbank und den eBOD-Atlas in dein Google Drive Hauptlager."
    )

    if st.button("Jetzt Komplett-Backup auf Google Drive erstellen"):
        with st.spinner("Synchronisiere Datenpakete..."):
            erfolg, nachricht = upload_all_to_drive()
            if erfolg:
                st.success(nachricht)
            else:
                st.error(nachricht)

    if os.path.exists(BACKUP_INFO_PATH):
        with open(BACKUP_INFO_PATH, "r") as f:
            st.caption(f"Letztes erfolgreiches Backup: {f.read()}")

    st.divider()
    st.subheader("System-Details")
    st.write(f"Modus: {'Lokal' if IS_LOCAL else 'Cloud'}")
    st.write(f"Daten-Pfad: `{DB_PATH}`")
    st.write(f"Prozessor: AMD Ryzen 7 2700X | Lager: Intenso SSD")

elif page == "Pflanzen-Experte":
    st.title("🔍 Intelligenter Pflanzen-Check")

    col_a, col_b = st.columns(2)
    with col_a:
        plz = st.text_input("PLZ für Wetter-Check:", value="8160")
    with col_b:
        query = st.text_input("Welche Pflanze möchtest du prüfen?").strip()

    if query:
        # 1. Registry-Mapping aufbauen
        name_to_id = {}
        for p_id, p_info in plants_data.PLANTS_REGISTRY.items():
            name_to_id[p_info["de"]] = p_id
            name_to_id[p_info["lat"]] = p_id

        # 2. Suche nach Übereinstimmungen
        matches = [name for name in name_to_id.keys() if query.lower() in name.lower()]

        if not matches:
            import difflib

            matches = difflib.get_close_matches(
                query, list(name_to_id.keys()), n=3, cutoff=0.4
            )

        if not matches:
            st.error(f"Keine Treffer für '{query}' gefunden.")
        else:
            # Pflanzenauswahl
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

            # --- SPALTE 1: STANDORT ---
            with res_col:
                st.markdown("### 📍 Standort & Recht")
                st.write(plants_data.check_plant(p_id, True))

                # --- SPALTE 2: UMWELT ---
                # --- SPALTE 2: UMWELT & KLIMA ---
            with env_col:
                st.markdown("### 💨 Umwelt & Klima")

                # 1. Wetter-Historie für die PLZ abrufen
                try:
                    env = history_module.get_environmental_history(plz)
                    has_env_data = False

                    # Wind-Check
                    if "wind_resistence" in info:
                        has_env_data = True
                        w_res = info["wind_resistence"]
                        if env["wind"] == "stark" and w_res == "gering":
                            st.warning("⚠️ Zu windig für diese Art!")
                        elif w_res == "hoch":
                            st.success("✅ Windfest")
                        else:
                            st.info(f"ℹ️ Windfestigkeit: {w_res.capitalize()}")

                    # Dürre-Check
                    if "drought_tolerance" in info:
                        has_env_data = True
                        d_tol = info["drought_tolerance"]
                        if env["drought_years"] >= 2 and d_tol == "gering":
                            st.warning("⚠️ Dürregefahr an diesem Standort!")
                        elif d_tol == "hoch":
                            st.success("✅ Klimawandel-Gewinner")
                        else:
                            st.info(f"ℹ️ Dürretoleranz: {d_tol.capitalize()}")

                    # Falls gar nichts in der Datenbank steht:
                    if not has_env_data:
                        st.info(
                            "ℹ️ Keine spezifischen Wind- oder Dürredaten für Malus hinterlegt."
                        )
                        st.caption(
                            f"Wetter-Trend für {plz}: {env['wind'].capitalize()}er Wind, {env['drought_years']} Dürrejahre."
                        )

                except Exception as e:
                    st.error("Wetterdaten konnten nicht geladen werden.")

            # --- SPALTE 3: BODEN (Hybrid-Logik) ---
            with soil_col:
                st.markdown("### 🧪 Boden-Passung")
                boden_typ, kalk_info, quelle_info = None, None, None
                use_wabe = False

                # Prüfen, ob wir die Wabe aus Preding nutzen
                if "active_soil" in st.session_state and st.session_state.active_soil:
                    if plz == "" or plz == "8160":
                        use_wabe = True

                if use_wabe:
                    soil = st.session_state.active_soil
                    boden_typ, kalk_info = soil["bodenart"], soil["kalk"]
                    q_id = (
                        st.session_state.current_hex
                        if "current_hex" in st.session_state
                        else "Garten"
                    )
                    quelle_info = f"Wabe {q_id}"
                    st.success("📍 Waben-Daten aktiv")
                elif plz:
                    has_lime_plz, quelle_info = get_soil_status(plz)
                    boden_typ = "PLZ-Schätzung"
                    kalk_info = "Hoch" if has_lime_plz else "Niedrig"
                    st.info(f"🔎 Schätzung für {plz}")

                if boden_typ:
                    has_lime = "Mittel" in kalk_info or "Hoch" in kalk_info
                    needs_acid = info.get("needs_acid_soil", False)

                    if needs_acid and has_lime:
                        st.error("❌ KALK-KONFLIKT")
                    elif needs_acid and not has_lime:
                        st.success("✅ MOORBEET-CHECK")
                    elif not needs_acid and has_lime:
                        st.success("✅ KALK-TOLERANZ")
                    else:
                        st.success("✅ PASSEND")

                    st.caption(f"Boden: {boden_typ} ({quelle_info})")
    else:
        # Startbildschirm, wenn noch keine Suche läuft
        st.info("Gib oben einen Pflanzennamen ein, um die Analyse zu starten.")

elif page == "Boden-Verwaltung":
    st.title("📊 Boden-Datenbank & Waben-Zentrale")

    st.subheader("🗄️ Historische PLZ-Daten (SQLite)")
    DB_PATH = "bodendaten.db"
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        df_sql = pd.read_sql_query("SELECT * FROM boden_daten", conn)
        conn.close()
        st.dataframe(df_sql, use_container_width=True)
    else:
        st.info("Keine SQLite-Datenbank gefunden.")

    st.divider()

    st.subheader("⬢ Deine Garten-Waben (H3-Index)")
    JSON_PATH = "ebod_atlas_backup.json"

    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            local_db = json.load(f)
        if local_db:
            display_data = [{"Wabe": k, **v} for k, v in local_db.items()]
            st.table(pd.DataFrame(display_data))
        else:
            st.warning("Die JSON-Datei ist leer.")
    else:
        st.error("JSON-Datei nicht gefunden!")

    with st.expander("➕ Neuen Boden-Datensatz anlegen"):
        new_hex = st.text_input("H3-Waben ID", key="new_hex_input")
        if st.button("Speichern", key="save_hex_btn"):
            st.success("Test-Speicherung!")

elif page == "Garten-Karte":
    st.title("🗺️ Dein Garten im Fokus (Preding)")

    # 1. Nur die Speicher-Initialisierung bleibt im "if not in" Block
    if "show_ebod" not in st.session_state:
        st.session_state.show_ebod = False

    # 2. GPS & HOME-BASE: Das muss IMMER laufen (raus aus dem if-Block!)
    HOME_LAT, HOME_LON = 47.19897, 15.64720
    from streamlit_js_eval import get_geolocation

    loc = get_geolocation()

    # Sicherheits-Check: Koordinaten festlegen
    if loc and isinstance(loc, dict) and "coords" in loc:
        lat = loc["coords"]["latitude"]
        lon = loc["coords"]["longitude"]
        st.success("📍 Live-GPS Signal aktiv")
    else:
        lat, lon = HOME_LAT, HOME_LON
        st.info("🏠 Modus: Home-Base (Warte auf GPS...)")

    # 3. Jetzt kommt H3 und der Rest
    import h3

    # ... hier geht dein Code weiter

    hex_id = h3.latlng_to_cell(lat, lon, 11)
    st.session_state.current_hex = hex_id

    st.session_state.show_ebod = st.toggle(
        "📡 eBOD Live-Analyse", value=st.session_state.show_ebod
    )

    if st.session_state.show_ebod:
        st.info(f"Analyse für Wabe: {hex_id}")

    st.divider()

    import folium
    from streamlit_folium import st_folium

    m = folium.Map(location=[lat, lon], zoom_start=18)
    folium.Marker([lat, lon]).add_to(m)

    # Der Folium-Anker
    st_folium(m, width=700, height=450, key="garden_map_final")
