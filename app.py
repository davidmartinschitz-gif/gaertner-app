import streamlit as st
import sqlite3
import os
import pandas as pd
import json
import time
import h3
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from streamlit_js_eval import get_geolocation
from streamlit_folium import st_folium
import folium

# --- DEINE EIGENEN MODULE ---
import plants_data
import history_module

# --- 1. GLOBALE KONFIGURATION ---
IS_LOCAL = os.path.exists(r"E:\Database")

if IS_LOCAL:
    DB_PATH = r"E:\Database\boden_austria.db"
    ATLAS_PATH = r"E:\Database\ebod_atlas.json"
    ENV_PATH = r"E:\Database\environment_history.json"
    BACKUP_INFO_PATH = r"E:\Database\last_backup.txt"
else:
    DB_PATH = "boden_austria_backup.db"
    ATLAS_PATH = "ebod_atlas_backup.json"
    ENV_PATH = "environment_history_backup.json"
    BACKUP_INFO_PATH = "last_backup.txt"

# --- 2. FUNKTIONS-DEFINITIONEN ---


def get_drive_instance():
    """Erstellt eine Drive-Verbindung. Priorisiert LOKAL (E:), um Secrets-Fehler zu vermeiden."""
    gauth = GoogleAuth()

    # 1. VERSUCH: Lokal (Dein PC)
    if IS_LOCAL:
        try:
            if os.path.exists("client_secrets.json"):
                gauth.LoadClientConfigFile("client_secrets.json")
                if os.path.exists("credentials.json"):
                    gauth.LoadCredentialsFile("credentials.json")

                if gauth.access_token_expired:
                    gauth.LocalWebserverAuth()
                else:
                    gauth.Authorize()
                return GoogleDrive(gauth)
        except Exception as e:
            st.sidebar.error(f"Lokaler Auth-Fehler: {e}")

    # 2. VERSUCH: Cloud-Secrets (Falls vorhanden)
    try:
        if hasattr(st, "secrets") and "google_drive" in st.secrets:
            with open("client_secrets.json", "w") as f:
                f.write(st.secrets["google_drive"]["client_secrets"])
            with open("credentials.json", "w") as f:
                f.write(st.secrets["google_drive"]["credentials"])
            gauth.LoadClientConfigFile("client_secrets.json")
            gauth.LoadCredentialsFile("credentials.json")
            if gauth.access_token_expired:
                gauth.Refresh()
            else:
                gauth.Authorize()
            return GoogleDrive(gauth)
    except:
        pass
    return None


def load_prohibitions():
    """Lädt das Verbotsregister sicher in den Session State."""
    if "prohibitions" not in st.session_state:
        try:
            if os.path.exists("prohibitions.json"):
                with open("prohibitions.json", "r", encoding="utf-8") as f:
                    st.session_state["prohibitions"] = json.load(f)
                if IS_LOCAL:
                    st.sidebar.success("✅ Verbotsregister aktiv")
            else:
                st.session_state["prohibitions"] = {}
        except:
            st.session_state["prohibitions"] = {}


def sync_from_drive():
    """Download-Logik für den Cloud-Start."""
    try:
        drive = get_drive_instance()
        if not drive:
            return False
        files = {
            "boden_austria_backup.db": DB_PATH,
            "ebod_atlas_backup.json": ATLAS_PATH,
        }
        for title, target in files.items():
            file_list = drive.ListFile(
                {"q": f"title = '{title}' and trashed = false"}
            ).GetList()
            if file_list:
                file_list[0].GetContentFile(target)
        return True
    except:
        return False


def upload_all_to_drive():
    """Cloud-Backup vom lokalen System."""
    try:
        drive = get_drive_instance()
        if not drive:
            return False, "❌ Verbindung fehlgeschlagen (Auth fehlt)."
        files_to_sync = {
            "boden_austria_backup.db": DB_PATH,
            "ebod_atlas_backup.json": ATLAS_PATH,
        }
        count = 0
        for title, path in files_to_sync.items():
            if os.path.exists(path):
                file_list = drive.ListFile(
                    {"q": f"title = '{title}' and trashed = false"}
                ).GetList()
                file_drive = (
                    file_list[0] if file_list else drive.CreateFile({"title": title})
                )
                file_drive.SetContentFile(path)
                file_drive.Upload()
                count += 1
        with open(BACKUP_INFO_PATH, "w") as f:
            f.write(pd.Timestamp.now().strftime("%d.%m.%Y %H:%M:%S"))
        return True, f"✅ Backup abgeschlossen ({count} Dateien)."
    except Exception as e:
        return False, f"❌ Cloud-Fehler: {str(e)}"


def check_prohibition(gemeinde_name, pflanze_suche):
    register = st.session_state.get("prohibitions", {})
    if not register:
        return None

    munis = register.get("municipalities", {})
    muni_key = next(
        (
            k
            for k in munis
            if k.strip().lower() in gemeinde_name.lower()
            or gemeinde_name.lower() in k.lower()
        ),
        None,
    )
    if not muni_key:
        return None

    muni_data = munis[muni_key]
    suche = pflanze_suche.lower().strip()

    # 1. Prüfe lokale Sonderregeln
    custom_rules = muni_data.get("custom_rules", {})
    for verbot_name, details in custom_rules.items():
        # LOGIK-FIX: Ist das Suchwort im Namen der Regel?
        if suche in verbot_name.lower():
            return details

    # 2. Prüfe abonnierte globale Gruppen (Hier steckt Thuja oft drin!)
    groups_to_check = muni_data.get("groups", [])
    global_groups = register.get("global_groups", {})

    for group_key in groups_to_check:
        group = global_groups.get(group_key)
        if group:
            for p_entry in group.get("plants", []):
                # LOGIK-FIX: Ist das Suchwort in der Pflanzenliste der Gruppe?
                if suche in p_entry.lower():
                    return {
                        "grund": f"{group.get('name')}: {group.get('grund')}",
                        "quelle": group.get("quelle"),
                    }
    return None


def get_soil_status(plz_input):
    """Boden-Check: 1. SQL (E:), 2. Atlas (RAM), 3. Standard."""
    if os.path.exists(DB_PATH):
        try:
            with sqlite3.connect(DB_PATH) as conn:
                row = conn.execute(
                    "SELECT kalkgehalt FROM boden_daten WHERE plz = ?", (plz_input,)
                ).fetchone()
                if row:
                    return row[0] > 0, "Eigene Messung (SSD)"
        except:
            pass
    if plz_input in ebod_db:
        entry = ebod_db[plz_input]
        kalk = entry.get("kalk", 0) if isinstance(entry, dict) else entry
        return (kalk > 0), "eBOD-Atlas"
    return False, "Standard"


# --- 3. INITIALISIERUNG ---
st.set_page_config(page_title="Gärtner-Master 2026", page_icon="🌱", layout="wide")
load_prohibitions()

# Einmaliger Cloud-Sync (Schutz gegen Dauerschleife)
if not IS_LOCAL and "cloud_synced" not in st.session_state:
    if sync_from_drive():
        st.session_state["cloud_synced"] = True

# Daten laden
PLZ_MAPPING = {}
if os.path.exists("plz_steiermark.json"):
    try:
        with open("plz_steiermark.json", "r", encoding="utf-8") as f:
            PLZ_MAPPING = json.load(f)
    except:
        pass

ebod_db = {}
if os.path.exists(ATLAS_PATH):
    try:
        with open(ATLAS_PATH, "r", encoding="utf-8") as f:
            ebod_db = json.load(f)
    except:
        pass

# --- 4. UI / NAVIGATION ---
st.sidebar.title("🌿 Gärtner-Master")
st.sidebar.info(f"System: {'Workstation (E:)' if IS_LOCAL else 'Cloud-Modus'}")
page = st.sidebar.radio(
    "Menü:", ["Dashboard", "Pflanzen-Experte", "Boden-Verwaltung", "Garten-Karte"]
)

# --- SEITE: DASHBOARD ---
if page == "Dashboard":
    st.title("🌱 Gärtner-Master Dashboard")
    st.info(
        f"**Prozessor:** AMD Ryzen 7 2700X | **Lager:** Kingston HyperX Predator M.2 SSD"
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Lexikon", f"{len(plants_data.PLANTS_REGISTRY)} Einträge")
    with col2:
        st.success("Datenbank bereit" if IS_LOCAL else "Cloud-Spiegel aktiv")
    with col3:
        if os.path.exists(BACKUP_INFO_PATH):
            with open(BACKUP_INFO_PATH, "r") as f:
                st.metric("Letztes Backup", f.read())

    st.divider()
    if st.button("🚀 Jetzt Cloud-Backup starten"):
        erfolg, msg = upload_all_to_drive()
        if erfolg:
            st.success(msg)
        else:
            st.error(msg)

# --- SEITE: PFLANZEN-EXPERTE ---
elif page == "Pflanzen-Experte":
    st.title("🔍 Intelligenter Pflanzen-Check")

    c1, c2 = st.columns(2)
    with c1:
        plz_in = st.text_input("PLZ eingeben:", "8160")
        orte = PLZ_MAPPING.get(plz_in, ["Standard"])
        gemeinde_in = st.selectbox("Ort wählen:", orte)
    with c2:
        query = st.text_input("Pflanze suchen (z.B. Acer oder Thuja):")

    if query:
        st.divider()
        # 1. Verbots-Check (Fuzzy)
        v = check_prohibition(gemeinde_in, query)
        if v:
            st.error(f"### 🚫 PFLANZVERBOT IN {gemeinde_in.upper()}")
            st.warning(f"**Grund:** {v.get('grund')}")

        # 2. Botanische Suche (Latein & Deutsch)
        matches = []
        for p_id, p in plants_data.PLANTS_REGISTRY.items():
            de = str(p.get("de", "")).strip()
            # ACER-FIX: Der Schlüssel in deiner Datei heißt "lat"!
            la = str(p.get("lat", "")).strip()

            if query.lower() in de.lower() or query.lower() in la.lower():
                label = (
                    f"{de.capitalize()} ({la.capitalize()})"
                    if de and la
                    else (de or la).capitalize()
                )
                matches.append((label, p_id))

        if matches:
            sel_tuple = st.selectbox(
                "Genaue Auswahl:", matches, format_func=lambda x: x[0]
            )
            p_id_final = sel_tuple[1]
            st.subheader(f"🌿 Analyse für: {sel_tuple[0]}")

            res_a, res_b = st.columns([2, 1])
            with res_a:
                st.write(plants_data.check_plant(p_id_final, True, plz_in))
            with res_b:
                is_kalk, src = get_soil_status(plz_in)
                st.metric("Boden", "Kalkhaltig" if is_kalk else "Sauer/Neutral")
                st.caption(f"Quelle: {src}")
        else:
            st.info(f"Keine Treffer für '{query}' gefunden.")

# --- SEITE: BODEN-VERWALTUNG ---
elif page == "Boden-Verwaltung":
    st.title("📊 Datenbank-Einsicht")
    if os.path.exists(DB_PATH):
        try:
            with sqlite3.connect(DB_PATH) as conn:
                df = pd.read_sql_query("SELECT * FROM boden_daten", conn)
                st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.warning(f"Tabelle nicht lesbar: {e}")
    else:
        st.info("Keine SQLite-Datenbank auf E: gefunden.")

# --- SEITE: GARTEN-KARTE ---
elif page == "Garten-Karte":
    st.title("🗺️ Standort-Analyse")
    loc = get_geolocation()

    # Sicherer GPS-Check (KeyError Fix)
    if loc and isinstance(loc, dict) and "coords" in loc:
        lat, lon = loc["coords"]["latitude"], loc["coords"]["longitude"]
        st.success("📍 Standort erfasst")
    else:
        lat, lon = 47.19897, 15.64720  # Preding Home-Base
        st.info("🏠 Modus: Home-Base (Warte auf GPS...)")

    try:
        h11 = h3.latlng_to_cell(lat, lon, 11)
    except:
        h11 = h3.geo_to_h3(lat, lon, 11)

    m = folium.Map(location=[lat, lon], zoom_start=18)
    folium.Marker([lat, lon]).add_to(m)
    st_folium(m, width=700, height=450)
