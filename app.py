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

# 2. JSON-Datenbank sicher laden
ebod_db = {}
if os.path.exists("ebod_atlas_backup.json"):
    try:
        with open("ebod_atlas_backup.json", "r", encoding="utf-8") as f:
            content = f.read()
            if content.strip():  # Prüfen, ob die Datei nicht leer ist
                ebod_db = json.loads(content)
    except Exception as e:
        st.error(f"Boden-Datenbank konnte nicht geladen werden. Nutze leere Basis.")

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

# Automatisch generiert aus deiner PLZ-Liste
PLZ_MAPPING = {
    "8160": ["Mortantsch", "Naas", "Preding (Weiz)", "Weiz"],
    "8181": ["St. Margarethen an der Raab", "St. Ruprecht an der Raab"],
    "8044": ["Graz", "Kainbach bei Graz"],
    "8054": ["Graz", "Haselsdorf-Tobelbad", "Seiersberg-Pirka"],
    "8504": ["Preding", "Sankt Nikolai im Sausal"],
    "8510": ["Marhof", "Stainz", "Stallhof"],
    # ... du kannst die Liste aus meiner letzten Nachricht hier beliebig erweitern
}


# --- 1. HELFER: GOOGLE DRIVE VERBINDUNG ---
def get_drive_instance():
    """Erstellt eine Google Drive Verbindung für Lokal oder Cloud."""
    gauth = GoogleAuth()

    if IS_LOCAL:
        # Lokal am PC: Nutze die echten Dateien
        gauth.LoadClientConfigFile("client_secrets.json")
        # --- ANGEPASSTER LOGIN-TEIL START ---
        gauth.GetFlow()
        gauth.flow.params.update({"access_type": "offline"})
        gauth.flow.params.update({"prompt": "consent"})
        gauth.LocalWebserverAuth()  # Hier öffnet sich nun der Browser für den Login
        # --- ANGEPASSTER LOGIN-TEIL ENDE ---

        gauth.SaveCredentialsFile("credentials.json")

    else:
        # IN DER CLOUD: Wir erstellen temporäre Dateien aus den Secrets
        if "google_drive" in st.secrets:
            # 1. Die client_secrets "vorgaukeln"
            with open("client_secrets.json", "w") as f:
                f.write(st.secrets["google_drive"]["client_secrets"])

            # 2. Die credentials "vorgaukeln" (behebt den _module Fehler)
            with open("credentials.json", "w") as f:
                f.write(st.secrets["google_drive"]["credentials"])

            # Jetzt laden wir sie ganz normal, als wären sie echte Dateien
            gauth.LoadClientConfigFile("client_secrets.json")
            gauth.LoadCredentialsFile("credentials.json")

            # Token auffrischen, falls nötig
            if gauth.access_token_expired:
                gauth.Refresh()
            else:
                gauth.Authorize()
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


# --- 1. DATEN-BASIS (Am besten ganz oben in der Datei) ---
PLZ_MAPPING = {
    "8160": ["Weiz", "Mortantsch", "Naas", "Krottendorf"],
    "8181": ["St. Ruprecht an der Raab", "St. Margarethen an der Raab"],
    "8044": ["Graz", "Kainbach bei Graz"],
    "8054": ["Graz", "Haselsdorf-Tobelbad", "Seiersberg-Pirka"],
}


# --- NEUE FUNKTION: VERBOTE AUS DRIVE LADEN ---
def load_prohibitions_from_drive():
    """Lädt die zentrale Verbots-Datenbank vom Google Drive."""
    try:
        drive = get_drive_instance()
        if not drive:
            return {}

        # Wir suchen nach der Datei 'prohibitions.json' im Drive
        query = "title = 'prohibitions.json' and trashed = false"
        file_list = drive.ListFile({"q": query}).GetList()

        if file_list:
            # Datei gefunden -> Inhalt herunterladen
            content = file_list[0].GetContentString()
            return json.loads(content)
        else:
            # Falls die Datei noch nicht existiert, leeres Register zurückgeben
            return {}
    except Exception as e:
        st.warning(f"Konnte Verbotsregister nicht laden: {e}")
        return {}


# --- IM DASHBOARD / UI-TEIL ---
# Wir laden die Verbote einmal am Anfang
if "prohibitions" not in st.session_state:
    st.session_state["prohibitions"] = load_prohibitions_from_drive()
# Nur zum Testen - zeigt an, wie viele Regeln geladen wurden
st.write(
    f"DEBUG: Register enthält {len(st.session_state.get('prohibitions', {}))} Gemeinden."
)


# --- DIE PRÜF-LOGIK BEIM SUCHEN ---
def check_prohibition(gemeinde, pflanze_suche):
    """Prüft, ob für die Gemeinde und die Pflanze ein Verbot vorliegt."""
    register = st.session_state.get("prohibitions", {})

    if gemeinde in register:
        gemeinde_regeln = register[gemeinde]
        # Wir prüfen, ob ein Teil des Suchbegriffs in den verbotenen Pflanzen vorkommt
        for verbotene_pflanze, details in gemeinde_regeln.items():
            if verbotene_pflanze.lower() in pflanze_suche.lower():
                return details  # Gibt Grund und Quelle zurück
    return None


def get_soil_status(plz_input):
    """Prüft die Bodenwerte in DB und Atlas."""
    # Check 1: Eigene SQL-Datenbank
    if os.path.exists(DB_PATH):
        try:
            with sqlite3.connect(DB_PATH) as conn:
                row = conn.execute(
                    "SELECT kalkgehalt FROM boden_daten WHERE plz = ?", (plz_input,)
                ).fetchone()
                if row:
                    return row[0] > 0, "Eigene Messung"
        except Exception:
            pass

    # Check 2: eBOD-Atlas (JSON)
    if os.path.exists(ATLAS_PATH):
        try:
            with open(ATLAS_PATH, "r") as f:
                atlas = json.load(f)
                if plz_input in atlas:
                    # Greift auf den Kalk-Wert im JSON zu
                    kalk_wert = atlas[plz_input].get("kalk", 0)
                    return kalk_wert > 0, "eBOD-Prognose"
        except Exception:
            pass

    # Das return muss HIER stehen (innerhalb der Funktion, ganz am Ende)
    return False, "Keine Daten"


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
    # Admin-Bereich in einem Expander verstecken
    with st.expander("☁️ Cloud-Synchronisation & Backup"):
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
        plz_input = st.text_input(
            "PLZ für Wetter-Check:", value="8160", key="plz_input_experte"
        )

        # --- NEU: DIE GEMEINDE-WEICHE ---
        ausgewaehlte_gemeinde = "Standard"
        if plz_input in PLZ_MAPPING:
            ausgewaehlte_gemeinde = st.selectbox(
                f"PLZ {plz_input} ist mehrdeutig. Bitte wähle deinen Ort:",
                options=PLZ_MAPPING[plz_input],
                key="gemeinde_weiche_experte",
            )
        else:
            st.caption(f"📍 Standort fixiert auf PLZ {plz_input}")

    with col_b:
        query = st.text_input(
            "Welche Pflanze möchtest du prüfen?", value="Thuja"
        ).strip()

    # DEBUG INFO (Der Spion)
    anzahl_regeln = len(st.session_state.get("prohibitions", {}))
    st.caption(f"🛡️ Experten-Register geladen für {anzahl_regeln} Gemeinden.")

    if query:
        # 1. Registry-Mapping
        name_to_id = {
            p_info["de"]: p_id for p_id, p_info in plants_data.PLANTS_REGISTRY.items()
        }
        name_to_id.update(
            {
                p_info["lat"]: p_id
                for p_id, p_info in plants_data.PLANTS_REGISTRY.items()
            }
        )

        # 2. Suche
        matches = [name for name in name_to_id.keys() if query.lower() in name.lower()]
        if not matches:
            matches = difflib.get_close_matches(
                query, list(name_to_id.keys()), n=3, cutoff=0.4
            )

        if not matches:
            st.error(f"Keine Treffer für '{query}' gefunden.")
        else:
            selected_name = st.selectbox(
                "Meintest du eine dieser Pflanzen?", matches, key="plant_select"
            )
            p_id = name_to_id[selected_name]

            st.divider()

            # --- PRIO 1: RECHTLICHER CHECK (PROHIBITIONS) ---
            verbot = check_prohibition(ausgewaehlte_gemeinde, selected_name)

            if verbot:
                st.error(f"### 🚫 PFLANZVERBOT IN {ausgewaehlte_gemeinde.upper()}")
                st.markdown(f"**Grund:** {verbot['grund']}")
                st.caption(f"Quelle: {verbot['quelle']}")
                st.warning("Dieser rechtliche Check hat Vorrang!")

            # --- BOTANISCHE ANALYSE ---
            st.subheader(f"Analyse für: {selected_name}")
            res_col, env_col, soil_col = st.columns(3)

            with res_col:
                st.markdown("### 📍 Standort & Recht")
                st.write(plants_data.check_plant(p_id, True, plz_input))

            with env_col:
                st.markdown("### 💨 Umwelt & Klima")
                try:
                    env = history_module.get_environmental_history(plz_input)
                    st.info(
                        f"Wetter-Trend für {plz_input}: {env['wind'].capitalize()}er Wind."
                    )
                except:
                    st.error("Wetterdaten nicht verfügbar.")

            with soil_col:
                st.markdown("### 🧪 Boden-Passung")
                kalk_vorhanden, quelle = get_soil_status(plz_input)
                st.write(
                    f"Boden-Check: {'Kalkhaltig' if kalk_vorhanden else 'Sauer/Neutral'}"
                )
                st.caption(f"Quelle: {quelle}")

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
