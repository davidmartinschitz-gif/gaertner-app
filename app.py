import streamlit as st
import sqlite3
import os
import pandas as pd
import json
import time
import h3
import requests
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from streamlit_js_eval import get_geolocation
from streamlit_folium import st_folium
import folium

# --- DEINE EIGENEN MODULE ---
import plants_data
import history_module

# --- DESIGN & STYLING (Update: Deep Forest & Glassmorphism) ---
st.markdown(
    """
    <style>
    /* 1. Fundament: Der Deep Forest Hintergrundverlauf (Dunkelgrün -> Schwarz) */
    .stApp {
        background: linear-gradient(135deg, #051905 0%, #0c1016 100%);
        color: #ecf0f1;
    }

    /* 2. Glassmorphismus-Effekt für Karten/Metriken (Dashboard) */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 15px !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }

    /* 3. Glassmorphismus für Info-Boxen und Aufklapp-Menüs (Admin/Atlas) */
    .stAlert, .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px;
    }

    /* 4. Konsistentes Styling für Buttons und Eingabefelder */
    .stButton>button { border-radius: 8px; border: 1px solid #4CAF50; background-color: transparent; color: white; transition: 0.3s; }
    .stButton>button:hover { background-color: #4CAF50; color: black; }
    .stTextInput>div>div>input { background-color: rgba(0, 0, 0, 0.3) !important; color: white !important; }
    .stSelectbox>div>div>div { background-color: rgba(0, 0, 0, 0.3) !important; color: white !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

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


import base64


def get_base64_image(image_path):
    import os

    if not os.path.exists(image_path):
        # Falls das Bild nicht gefunden wird, geben wir eine Info aus
        return None
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def add_footer(user_name="David Martinschitz"):
    logo_path = "Screenshot 2026-04-14 130505.jpg"
    img_base64 = get_base64_image(logo_path)

    # HTML Grundgerüst
    footer_style = "position: relative; margin-top: 50px; padding: 20px; text-align: center; border-top: 1px solid rgba(255,255,255,0.1);"

    if img_base64:
        # Wenn Bild vorhanden: Logo + Name
        logo_html = f'<img src="data:image/jpeg;base64,{img_base64}" style="width: 80px; filter: brightness(1.2); margin-bottom: 10px;">'
    else:
        # Fallback: Nur ein dezentes Icon, falls das Bild lokal/cloud fehlt
        logo_html = '<p style="font-size: 2rem;">🌿</p>'

    st.markdown(
        f"""
        <div style="{footer_style}">
            <p style="color: rgba(255,255,255,0.4); font-size: 0.7rem; letter-spacing: 2px; text-transform: uppercase;">Powered by:</p>
            {logo_html}
            <p style="color: #4CAF50; font-weight: bold; font-family: 'Courier New', monospace; margin-top: 5px;">{user_name}</p>
        </div>
    """,
        unsafe_allow_html=True,
    )


def save_to_pending(plz, kalk, typ, humus, note):
    """Speichert Detail-Werte vom Handy in die Veto-Liste."""
    try:
        data = []
        if os.path.exists("pending_changes.json"):
            with open("pending_changes.json", "r") as f:
                data = json.load(f)
        data.append(
            {
                "id": int(time.time()),
                "plz": plz,
                "kalk": kalk,
                "typ": typ,
                "humus": humus,
                "note": note,
            }
        )
        with open("pending_changes.json", "w") as f:
            json.dump(data, f)
        return True
    except:
        return False


def save_to_master(plz, kalk, typ, humus, note):  # note hinzugefügt
    try:
        with sqlite3.connect(DB_PATH) as conn:
            # Hier jetzt mit 5 Spalten inklusive bemerkung
            conn.execute(
                "INSERT INTO boden_daten (plz, kalkgehalt, bodentyp, humusgehalt, bemerkung) VALUES (?, ?, ?, ?, ?)",
                (plz, kalk, typ, humus, note),
            )
        return True
    except:
        return False


# Danach folgt dann dein bestehender Code:
def load_prohibitions(): ...


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
    """Lädt DB und Atlas, mergt aber die Vorschläge (Pending Changes) statt sie zu löschen."""
    try:
        drive = get_drive_instance()
        if not drive:
            return False

        # 1. Master-Daten normal überschreiben (DB & Atlas)
        master_files = {
            "boden_austria_backup.db": DB_PATH,
            "ebod_atlas_backup.json": ATLAS_PATH,
        }
        for title, target in master_files.items():
            file_list = drive.ListFile(
                {"q": f"title = '{title}' and trashed = false"}
            ).GetList()
            if file_list:
                file_list[0].GetContentFile(target)

        # 2. VETO-LISTE MERGEN (Die Lösung für dein Problem)
        title = "pending_changes.json"
        file_list = drive.ListFile(
            {"q": f"title = '{title}' and trashed = false"}
        ).GetList()
        if file_list:
            # Cloud-Daten als Text holen und in Liste umwandeln
            cloud_content = file_list[0].GetContentString()
            cloud_data = json.loads(cloud_content) if cloud_content else []

            # Lokale Daten (vom Handy/PC) laden
            local_data = []
            if os.path.exists("pending_changes.json"):
                with open("pending_changes.json", "r") as f:
                    local_data = json.load(f)

            # Mergen: Nur Einträge hinzufügen, die wir lokal noch nicht haben (ID-Check)
            local_ids = {item["id"] for item in local_data if "id" in item}
            for item in cloud_data:
                if item.get("id") not in local_ids:
                    local_data.append(item)

            # Die kombinierte Liste lokal speichern
            with open("pending_changes.json", "w") as f:
                json.dump(local_data, f)

        return True
    except Exception as e:
        return False


def upload_all_to_drive():
    """Sichert alle lokalen Daten inklusive der Veto-Liste in die Cloud."""
    try:
        drive = get_drive_instance()
        if not drive:
            return False, "❌ Verbindung fehlgeschlagen (Auth fehlt)."

        # NEU: Auch hier die Veto-Datei mitsynchronisieren
        files_to_sync = {
            "boden_austria_backup.db": DB_PATH,
            "ebod_atlas_backup.json": ATLAS_PATH,
            "pending_changes.json": "pending_changes.json",
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
        return True, f"✅ Sync abgeschlossen ({count} Dateien)."
    except Exception as e:
        return False, f"❌ Cloud-Fehler: {str(e)}"


def check_prohibition(gemeinde_name, pflanze_suche):
    register = st.session_state.get("prohibitions", {})
    if not register:
        return None
    munis = register.get("municipalities", {})
    # Sucht den passenden Eintrag, egal ob Groß/Kleinschreibung oder Leerzeichen
    muni_key = next(
        (k for k in munis if k.strip().lower() == gemeinde_name.strip().lower()), None
    )
    if not muni_key:
        return None
    muni_data = munis[muni_key]
    suche = pflanze_suche.lower()

    # 1. Lokale Regeln (z.B. Thuja-Heckenverordnung)
    custom_rules = muni_data.get("custom_rules", {})
    for verbot_name, details in custom_rules.items():
        if suche in verbot_name.lower():  # Logik-Fix: Suche IM Verbotsnamen
            return details

    # 2. Gruppen (z.B. Bebauungsplan)
    groups_to_check = muni_data.get("groups", [])
    global_groups = register.get("global_groups", {})
    for group_key in groups_to_check:
        group = global_groups.get(group_key)
        if group:
            for p_entry in group.get("plants", []):
                if suche in p_entry.lower():
                    return {
                        "status": "verboten",
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
st.set_page_config(
    page_title="Gärtner-Master 2026",
    page_icon="Screenshot 2026-04-14 130505.jpg",  # Hier wird dein Logo zum Tab-Icon
    layout="wide",
)

# Synchronisiert jetzt IMMER beim Starten (auch am PC), um Vorschläge zu finden
if "cloud_synced" not in st.session_state:
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
    st.title("🌿 Gärtner-Master Dashboard")
    # Hardware-Info wurde hier entfernt :)

    # 1. STANDORT-LOGIK (Dynamisch)
    loc = get_geolocation()
    if loc and "coords" in loc:
        lat = loc["coords"]["latitude"]
        lon = loc["coords"]["longitude"]
        status_text = "📍 Standort: Live (GPS)"
    else:
        # Fallback auf Baumschulgasse 2, 8160 Preding
        lat, lon = 47.2001, 15.6515
        status_text = "🏠 Standort: Home-Base (Preding)"

    # 2. WETTER-ABFRAGE basierend auf Koordinaten
    temp = "N/A"
    try:
        w_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        w_res = requests.get(w_url, timeout=5).json()
        w_data = w_res["current_weather"]
        temp = w_data["temperature"]
    except:
        pass

    # 3. STATUS-METRIKEN (Glassmorphism-Design aktiv)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Lokal-Temperatur",
            f"{temp} °C",
            delta=(
                "Frostgefahr!" if isinstance(temp, (int, float)) and temp < 2 else None
            ),
        )
    with col2:
        st.metric("Lexikon", f"{len(plants_data.PLANTS_REGISTRY)} Pflanzen")
    with col3:
        if os.path.exists(BACKUP_INFO_PATH):
            with open(BACKUP_INFO_PATH, "r") as f:
                st.metric("Letztes Backup", f.read())

    st.success(
        "System: Workstation bereit" if IS_LOCAL else "System: Cloud-Spiegel aktiv"
    )
    st.caption(status_text)

    # 4. SYNCHRONISIERUNG
    st.divider()
    if st.button("🔄 Volle Synchronisierung (Cloud ↔ PC)"):
        with st.spinner("Synchronisiere mit Google Drive..."):
            pull_erfolg = sync_from_drive()
            erfolg, msg = upload_all_to_drive()
            if pull_erfolg and erfolg:
                st.success("✅ Synchronisierung abgeschlossen: Vorschläge geladen!")
                st.rerun()
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

            # 1. Daten abrufen
            plant_info = plants_data.PLANTS_REGISTRY[p_id_final]
            is_kalk, src = get_soil_status(plz_in)

            # 2. Anzeige in zwei Spalten
            res_a, res_b = st.columns([2, 1])

            with res_a:
                # Allgemeiner Check (Feuerbrand etc.)
                st.write(plants_data.check_plant(p_id_final, True, plz_in))

                # DER NEUE BODEN-VERGLEICH (Logik-Brücke)
                if plant_info.get("needs_acid_soil") and is_kalk:
                    st.error(
                        "🚨 BODEN-KONFLIKT: Diese Pflanze benötigt sauren Boden (Moorbeet)!"
                    )
                    st.warning(
                        f"Dein Standort ({plz_in}) ist laut {src} kalkhaltig. Ohne Bodenaustausch wird die Pflanze hier kümmern."
                    )
                elif plant_info.get("needs_acid_soil") and not is_kalk:
                    st.success(
                        "✨ Boden-Match: Die Pflanze liebt deinen sauren/neutralen Boden!"
                    )

            with res_b:
                # 1. Boden-Status
                st.metric(
                    "Boden am Standort", "Kalkhaltig" if is_kalk else "Sauer/Neutral"
                )

                # 2. Trockenheitstoleranz
                dt = plant_info.get("drought_tolerance", "k.A.")
                if dt.lower() in ["hoch", "extrem"]:
                    st.metric("Trocken-Toleranz", dt.capitalize(), delta="Klimafit")
                else:
                    st.metric("Trocken-Toleranz", dt.capitalize())

                # 3. Windfestigkeit
                # Nutzt den Schlüssel 'wind_resistence' aus dem Lexikon
                wr = plant_info.get("wind_resistence", "k.A.")
                if wr.lower() == "hoch":
                    st.metric("Windfestigkeit", wr.capitalize(), delta="Sturmfest")
                else:
                    st.metric("Windfestigkeit", wr.capitalize())

                st.caption(f"Quelle: {src}")

# --- SEITE: BODEN-VERWALTUNG ---
elif page == "Boden-Verwaltung":
    st.title("📊 Boden-Management & Analyse")

    search_plz = st.text_input(
        "🔍 Offizielle Boden-Info suchen (PLZ):", placeholder="z.B. 8160"
    )
    if search_plz in ebod_db:
        atlas_info = ebod_db[search_plz]
        st.info(f"**eBOD-Atlas Info für {search_plz}:** {atlas_info}")

    # 1. ADMIN-BEREICH (Sichtbar auf deiner Workstation)
    if IS_LOCAL:
        with st.expander("🛠️ Admin-Panel: Ausstehende Änderungen prüfen", expanded=True):
            if os.path.exists("pending_changes.json"):
                with open("pending_changes.json", "r") as f:
                    pending = json.load(f)

                if not pending:
                    st.write("Keine neuen Vorschläge vorhanden.")
                else:
                    for item in pending:
                        st.info(f"**Vorschlag für PLZ {item.get('plz')}**")
                        col_a, col_b, col_c = st.columns([3, 1, 1])
                        with col_a:
                            st.write(
                                f"Typ: {item.get('typ')} | Kalk: {item.get('kalk')} | Humus: {item.get('humus')}"
                            )
                            st.caption(f"Notiz: {item.get('note', 'Keine Notiz')}")
                        with col_b:
                            if st.button(
                                "✅ Ja", key=f"app_{item.get('id', time.time())}"
                            ):
                                if save_to_master(
                                    item["plz"],
                                    item["kalk"],
                                    item["typ"],
                                    item["humus"],
                                    item.get("note", ""),
                                ):
                                    pending.remove(item)
                                    with open("pending_changes.json", "w") as f:
                                        json.dump(pending, f)

                                    upload_all_to_drive()  # <--- 1. Cloud-Fix nach Annahme
                                    st.rerun()
                        with col_c:
                            if st.button(
                                "❌ Nein", key=f"rej_{item.get('id', time.time())}"
                            ):
                                pending.remove(item)
                                with open("pending_changes.json", "w") as f:
                                    json.dump(pending, f)

                                upload_all_to_drive()  # <--- 2. Cloud-Fix nach Ablehnung
                                st.rerun()

    st.divider()

    # 2. DETAIL-EINGABE (Für PC und Handy)
    st.subheader("➕ Detaillierte Bodenmessung erfassen")
    with st.form("boden_form"):
        c1, c2 = st.columns(2)
        with c1:
            f_plz = st.text_input("PLZ", "8160")
            f_typ = st.selectbox(
                "Bodentyp", ["Lehm", "Sand", "Ton", "Humus", "Schluff"]
            )
        with c2:
            f_kalk = st.text_input("Kalkgehalt (z.B. '7%' oder 'Hoch')", "normal")
            f_humus = st.text_input("Humusgehalt (z.B. '3.5%')", "normal")

        f_note = st.text_input("Interne Anmerkung (z.B. Gasse / Beet)")

        submit = st.form_submit_button("Eintrag senden")

        if submit:
            if not IS_LOCAL:
                # Mobil-Nutzer schreibt in 'pending'
                if save_to_pending(f_plz, f_kalk, f_typ, f_humus, f_note):
                    st.success(
                        "✅ Vorschlag gesendet! Bitte klicke jetzt am Handy auf 'Backup starten'."
                    )
            else:
                # Du am PC schreibst direkt auf Laufwerk E:
                if save_to_master(f_plz, f_kalk, f_typ, f_humus, f_note):
                    st.success(f"✅ Daten direkt auf Kingston SSD (E:) gespeichert.")

    # 3. DATEN-EINSICHT (Master-Tabelle)
    st.subheader("📂 Aktuelle Master-Datenbank")
    if os.path.exists(DB_PATH):
        try:
            with sqlite3.connect(DB_PATH) as conn:
                df = pd.read_sql_query("SELECT * FROM boden_daten", conn)
                st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.info(f"Datenbank ist noch leer oder Tabellenstruktur weicht ab: {e}")


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

# --- GLOBALER FOOTER (Am Ende der Datei) ---
add_footer("David Martinschitz")  # Hier deinen echten Namen eintragen
