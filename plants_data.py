# plants_data.py - Das ultimative Profi-Lexikon (Stand April 2026)

PLANTS_REGISTRY = {
    # --- 1. ALLEEBÄUME & GROSSBÄUME (Klimafit & Stadtfest) ---
    "acer_campestre": {
        "de": "Feldahorn", "lat": "Acer campestre", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Extrem klimaresistent, sehr wertvoll für Insekten.",
    },
    "acer_campestre_elsrijk": {
        "de": "Feldahorn 'Elsrijk'", "lat": "Acer campestre 'Elsrijk'", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Perfekt für schmale, geschnittene Hecken im städtischen Bereich.",
    },
    "acer_monspessulanum": {
        "de": "Französischer Ahorn / Burgenland-Ahorn", "lat": "Acer monspessulanum", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "extrem",
        "note": "Der klimafiteste heimische Ahorn, ideal für das Grazer Becken.",
    },
    "acer_platanoides_globosum": {
        "de": "Kugel-Ahorn", "lat": "Acer platanoides 'Globosum'", "native": True,
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Idealer Hausbaum, kompakt bleibend.",
    },
    "aesculus_hippocastanum": {
        "de": "Rosskastanie", "lat": "Aesculus hippocastanum", "native": True,
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Klassischer Biergartenbaum, leider oft Miniermottenbefall.",
    },
    "alnus_glutinosa": {
        "de": "Schwarz-Erle", "lat": "Alnus glutinosa", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "gering",
        "note": "Perfekt für feuchte Standorte und Bachufer in der Obersteiermark.",
    },
    "betula_pendula": {
        "de": "Hängebirke", "lat": "Betula pendula", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Pionierbaum, hoher Wasserverbrauch.",
    },
    "catalpa_bignonioides": {
        "de": "Gewöhnlicher Trompetenbaum", "lat": "Catalpa bignonioides",
        "needs_acid_soil": False, "wind_resistence": "gering", "drought_tolerance": "mittel",
        "note": "Große blätter (Windfang!), schöne Blüte.",
    },
    "catalpa_bignonioides_nana": {
        "de": "Kugel-Trompetenbaum", "lat": "Catalpa bignonioides 'Nana'",
        "needs_acid_soil": False, "wind_resistence": "gering", "drought_tolerance": "mittel",
        "note": "Beliebter Hausbaum, bildet von Natur aus eine dichte Kugelkrone.",
    },
    "celtis_australis": {
        "de": "Südlicher Zürgelbaum", "lat": "Celtis australis",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Der ultimative Klimabaum für die Stadt, sehr hitzefest.",
    },
    "fagus_sylvatica": {
        "de": "Rotbuche", "lat": "Fagus sylvatica", "native": True,
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Heimischer Waldbaum, verträgt keine Staunässe.",
    },
    "fagus_sylvatica_purpurea": {
        "de": "Blutbuche", "lat": "Fagus sylvatica f. purpurea", "native": True,
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Dunkelrotes Laub, sehr langlebig.",
    },
    "fraxinus_ornus": {
        "de": "Manna-Esche / Blumen-Esche", "lat": "Fraxinus ornus", "native": True,
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "hoch",
        "note": "Duftende weiße Blüten, sehr trockenheitsresistent.",
    },
    "ginkgo_biloba": {
        "de": "Ginkgo", "lat": "Ginkgo biloba",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Lebendes Fossil, sehr resistent gegen Abgase.",
    },
    "gleditsia_triacanthos": {
        "de": "Lederhülsenbaum", "lat": "Gleditsia triacanthos",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "hoch",
        "note": "Filigranes Laub, extrem trockenheitsverträglich.",
    },
    "gymnocladus_dioicus": {
        "de": "Geweihbaum", "lat": "Gymnocladus dioicus",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Bizarre Wintergestalt, sehr robuster Stadtbaum.",
    },
    "liquidambar_styraciflua": {
        "de": "Amberbaum", "lat": "Liquidambar styraciflua",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Beste Herbstfärbung im Sortiment.",
    },
    "liriodendron_tulipifera": {
        "de": "Tulpenbaum", "lat": "Liriodendron tulipifera",
        "needs_acid_soil": True, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Großer Parkbaum mit markanten tulpenförmigen Blüten.",
    },
    "ostrya_carpinifolia": {
        "de": "Europäische Hopfenbuche", "lat": "Ostrya carpinifolia", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Hopfenförmige Früchte, sehr robust gegen Trockenheit.",
    },
    "parrotia_persica": {
        "de": "Eisenholzbaum", "lat": "Parrotia persica",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Absolut klimafit, bizarre Wuchsform im Alter.",
    },
    "parrotia_persica_vanessa": {
        "de": "Säulen-Eisenholzbaum", "lat": "Parrotia persica 'Vanessa'",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Schmaler Wuchs, extrem klimaresistent.",
    },
    "paulownia_tomentosa": {
        "de": "Blauglockenbaum", "lat": "Paulownia tomentosa",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "hoch",
        "note": "Extrem schnellwachsend, braucht viel Platz.",
    },
    "platanus_hispanica": {
        "de": "Ahornblättrige Platane", "lat": "Platanus x hispanica",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Der ultimative Stadtbaum, extrem robust gegen Abgase und Hitze.",
    },
    "quercus_cerris": {
        "de": "Zerreiche", "lat": "Quercus cerris", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Hitzekünstler der Zukunft, sehr wichtig für trockene steirische Lagen.",
    },
    "quercus_phellos": {
        "de": "Weidenblättrige Eiche", "lat": "Quercus phellos",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Filigranes Laub, sehr widerstandsfähig.",
    },
    "quercus_robur": {
        "de": "Stieleiche", "lat": "Quercus robur", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Tiefwurzler, extrem windfest, ökologisch unersetzbar.",
    },
    "robinia_pseudoacacia_umbraculifera": {
        "de": "Kugel-Robinie", "lat": "Robinia pseudoacacia 'Umbraculifera'",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "hoch",
        "note": "Dornenlos, ideal für schmale Straßen und kleine Gärten.",
    },
    "salix_alba_tristis": {
        "de": "Trauerweide", "lat": "Salix alba 'Tristis'", "native": True,
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "gering",
        "note": "Braucht viel Platz und Wassernähe.",
    },
    "sophora_japonica": {
        "de": "Japanischer Schnurbaum", "lat": "Sophora japonica",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "hoch",
        "note": "Wunderschöne Spätblüte im August, Bienenweide.",
    },
    "sorbus_aria": {
        "de": "Echte Mehlbeere", "lat": "Sorbus aria", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Heimisch, sehr robust gegen Wind und Trockenheit.",
    },
    "sorbus_domestica": {
        "de": "Speierling", "lat": "Sorbus domestica", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Seltener Wildobstbaum, sehr langlebig und wertvolles Holz.",
    },
    "sorbus_torminalis": {
        "de": "Elsbeere", "lat": "Sorbus torminalis", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Kostbares Holz, ökologisch wertvoll, klimafit.",
    },
    "tilia_cordata": {
        "de": "Winterlinde", "lat": "Tilia cordata", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Wertvollster Bienenbaum im Sommer.",
    },
    "tilia_tomentosa": {
        "de": "Silber-Linde", "lat": "Tilia tomentosa",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Hitzeverträglichste Linde, gut gegen Blattläuse.",
    },
    "ulmus_resista": {
        "de": "Resista-Ulme", "lat": "Ulmus 'Resista'",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Resistent gegen das Ulmensterben, sehr windfest.",
    },
    "zelkova_serrata": {
        "de": "Japanische Zelkove", "lat": "Zelkova serrata",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Schöner Ersatz für die Ulme, tolle Rinde.",
    },

    # --- 2. OBST- & NUTZBÄUME ---
    "castanea_sativa": {
        "de": "Esskastanie", "lat": "Castanea sativa", "needs_acid_soil": True,
        "wind_resistence": "mittel", "drought_tolerance": "hoch",
        "note": "Wärmeliebend, wertvolle Nutzpflanze. Mag keinen Kalk!",
    },
    "corylus_avellana_contorta": {
        "de": "Korkenzieher-Hasel", "lat": "Corylus avellana 'Contorta'", "native": True,
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Skurrile, gedrehte Zweige, toller Winterschmuck.",
    },
    "corylus_colurna": {
        "de": "Baum-Hasel", "lat": "Corylus colurna", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Sehr tiefe Wurzeln, extrem standfest bei Sturm.",
    },
    "cydonia_oblonga": {
        "de": "Quitte", "lat": "Cydonia oblonga", "fire_blight_risk": True,
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Traditionelles Obstgehölz. ACHTUNG: Extrem feuerbrandanfällig!",
    },
    "diospyros_kaki": {
        "de": "Kaki / Persimone", "lat": "Diospyros kaki",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Exotische Frucht, braucht geschützten sonnigen Standort.",
    },
    "ficus_carica": {
        "de": "Echte Feige", "lat": "Ficus carica",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "hoch",
        "note": "In Weinbaulagen (Südsteiermark) mittlerweile problemlos winterhart.",
    },
    "juglans_regia": {
        "de": "Echte Walnuss", "lat": "Juglans regia", "native": True,
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Großer Schattenbaum mit Nutzwert.",
    },
    "mespilus_germanica": {
        "de": "Echte Mispel", "lat": "Mespilus germanica", "fire_blight_risk": True,
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "hoch",
        "note": "Steirisches Traditionsobst ('Haspel'), dekorative Blüte und Herbstfärbung.",
    },
    "morus_alba": {
        "de": "Weiße Maulbeere", "lat": "Morus alba",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "hoch",
        "note": "Essbare Früchte, sehr langlebig.",
    },
    "prunus_armeniaca": {
        "de": "Marille", "lat": "Prunus armeniaca",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "hoch",
        "note": "Spätfrostgefährdet, braucht warme Standorte.",
    },
    "prunus_avium": {
        "de": "Säulenkirsche", "lat": "Prunus avium",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Platzsparender Obstbaum.",
    },
    "prunus_domestica": {
        "de": "Hauszwetschke", "lat": "Prunus domestica", "native": True,
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Traditionelles österreichisches Obstgehölz.",
    },
    "pyrus_communis": {
        "de": "Kultur-Birne", "lat": "Pyrus communis", "fire_blight_risk": True,
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "In der Steiermark (PLZ 8) meldepflichtig bei Feuerbrand!",
    },
    "vitis_vinifera": {
        "de": "Weinrebe", "lat": "Vitis vinifera", "native": True,
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "hoch",
        "note": "Steirisches Kulturgut. Braucht viel Sonne und Kalk.",
    },

    # --- 3. NADELGEHÖLZE & CONIFEREN ---
    "cupressocyparis_leylandii": {
        "de": "Leyland-Zypresse", "lat": "Cupressocyparis leylandii",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "restriction": "Extrem schnellwachsend, braucht regelmäßigen Schnitt.",
    },
    "juniperus_communis": {
        "de": "Gemeiner Wacholder", "lat": "Juniperus communis", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Immergrün, heimisch, sehr robust.",
    },
    "juniperus_horizontalis_blue_chip": {
        "de": "Kriechwacholder 'Blue Chip'", "lat": "Juniperus horizontalis 'Blue Chip'",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Stahlblaue Nadeln, flach kriechend, perfekt für Böschungen.",
    },
    "microbiota_decussata": {
        "de": "Sibirischer Fächerwacholder", "lat": "Microbiota decussata",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Extrem frosthart, färbt sich im Winter bronzefarben.",
    },
    "picea_abies_nidiformis": {
        "de": "Nest-Fichte", "lat": "Picea abies 'Nidiformis'", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Wächst nestartig flach, sehr langsamwüchsig.",
    },
    "pinus_mugo_mughus": {
        "de": "Latsche / Bergkiefer", "lat": "Pinus mugo var. mughus", "native": True,
        "needs_acid_soil": False, "wind_resistence": "extrem", "drought_tolerance": "hoch",
        "note": "Überlebt im Hochgebirge wie im Steingarten.",
    },
    "pinus_sylvestris": {
        "de": "Waldkiefer / Föhre", "lat": "Pinus sylvestris", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Heimisch, kommt mit kargsten Böden zurecht.",
    },
    "platycladus_orientalis": {
        "de": "Orientalischer Lebensbaum", "lat": "Platycladus orientalis",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Hitzeverträglicher als die Thuja occidentalis.",
    },
    "taxus_baccata": {
        "de": "Eibe", "lat": "Taxus baccata", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "restriction": "Ganze Pflanze (außer Samenmantel) EXTREM GIFTIG.",
    },
    "taxus_baccata_fastigiata": {
        "de": "Säuleneibe", "lat": "Taxus baccata 'Fastigiata'",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Langsam wachsend, sehr langlebig.",
    },
    "taxus_baccata_repandens": {
        "de": "Kissen-Eibe", "lat": "Taxus baccata 'Repandens'", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "restriction": "Giftig! Sehr schattenverträglich.",
    },
    "taxus_media_hicksii": {
        "de": "Becher-Eibe", "lat": "Taxus x media 'Hicksii'",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "restriction": "Ganze Pflanze EXTREM GIFTIG. Beste Hecken-Eibe, wächst straff aufrecht.",
    },
    "thuja_brabant": {
        "de": "Abendländischer Lebensbaum 'Brabant'", "lat": "Thuja occidentalis 'Brabant'",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "gering",
        "restriction": "Schnellwachsend, hoher Wasserbedarf.",
    },
    "thuja_smaragd": {
        "de": "Smaragd-Thuja", "lat": "Thuja occidentalis 'Smaragd'",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "gering",
        "restriction": "Ökologisch geringer Wert, Staunässe-empfindlich.",
    },

    # --- 4. BLÜTENSTRÄUCHER & ZIERGEHÖLZE ---
    "acer_palmatum": {
        "de": "Japanischer Ahorn", "lat": "Acer palmatum",
        "needs_acid_soil": False, "wind_resistence": "gering", "drought_tolerance": "gering",
        "note": "Empfindlich gegen Spätfrost und pralle Mittagssonne.",
    },
    "acer_tataricum": {
        "de": "Steppen-Ahorn", "lat": "Acer tataricum",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "hoch",
        "note": "Hitzeverträglich, sehr schöne Herbstfärbung.",
    },
    "amelanchier_lamarckii": {
        "de": "Felsenbirne", "lat": "Amelanchier lamarckii", "fire_blight_risk": True,
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Essbare Früchte, spektakuläre Herbstfärbung. Feuerbrand-Wirt!",
    },
    "berberis_thunbergii_atropurpurea": {
        "de": "Blutberberitze", "lat": "Berberis thunbergii 'Atropurpurea'",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "restriction": "Dornig, ökologisch wertvoll als Vogelschutzgehölz.",
    },
    "buddleja_alternifolia": {
        "de": "Hänge-Sommerflieder", "lat": "Buddleja alternifolia",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "hoch",
        "note": "Frosthärter als der normale Sommerflieder.",
    },
    "buddleja_davidii": {
        "de": "Sommerflieder", "lat": "Buddleja davidii",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "hoch",
        "restriction": "Invasive Tendenz, Rückschnitt im Frühjahr zwingend.",
    },
    "cercis_siliquastrum": {
        "de": "Judasbaum", "lat": "Cercis siliquastrum",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "hoch",
        "note": "Stammblüher! Wunderschöne rosa Blüten direkt am Holz.",
    },
    "cornus_controversa": {
        "de": "Etagen-Hartriegel", "lat": "Cornus controversa",
        "needs_acid_soil": True, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Spektakulärer Wuchs in horizontalen Etagen.",
    },
    "cornus_kousa": {
        "de": "Blumen-Hartriegel", "lat": "Cornus kousa",
        "needs_acid_soil": True, "wind_resistence": "gering", "drought_tolerance": "mittel",
        "note": "Exotische Blüten und essbare (faserige) Früchte.",
    },
    "cornus_kousa_chinensis": {
        "de": "Chinesischer Blumenhartriegel", "lat": "Cornus kousa var. chinensis",
        "needs_acid_soil": True, "wind_resistence": "gering", "drought_tolerance": "mittel",
        "note": "Große weiße Brakteen, essbare Früchte.",
    },
    "cornus_mas": {
        "de": "Kornelkirsche", "lat": "Cornus mas", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Wichtigster Frühblüher für Bienen, essbare Früchte.",
    },
    "cornus_sanguinea": {
        "de": "Roter Hartriegel", "lat": "Cornus sanguinea", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Intensive rote Zweigfärbung im Winter.",
    },
    "cornus_stolonifera_flaviramea": {
        "de": "Gelber Hartriegel", "lat": "Cornus stolonifera 'Flaviramea'",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Auffällige gelbe Rinde im Winter.",
    },
    "cotinus_coggygria": {
        "de": "Perückenstrauch", "lat": "Cotinus coggygria",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Bizarre Fruchtstände, die wie Perücken wirken.",
    },
    "crataegus_monogyna": {
        "de": "Weißdorn", "lat": "Crataegus monogyna", "native": True, "fire_blight_risk": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Bestes Vogelschutzgehölz. Achtung: Hauptwirt für Feuerbrand!",
    },
    "davidia_involucrata": {
        "de": "Taschentuchbaum", "lat": "Davidia involucrata",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Rarität: Blüten hängen wie weiße Taschentücher herab.",
    },
    "deutzia_scabra": {
        "de": "Hoher Maiblumenstrauch", "lat": "Deutzia scabra",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Anspruchsloser Blütenstrauch.",
    },
    "elaeagnus_ebbingei": {
        "de": "Wintergrüne Ölweide", "lat": "Elaeagnus ebbingei",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Extrem hitzefest, duftende Blüten im Herbst.",
    },
    "euonymus_europaeus": {
        "de": "Pfaffenkäppchen", "lat": "Euonymus europaeus", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "restriction": "Giftig! Markante Früchte im Herbst.",
    },
    "fargesia_murielae": {
        "de": "Schirmbambus", "lat": "Fargesia murielae",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Horstbildend (keine Ausläufer), immergrün.",
    },
    "forsythia_intermedia": {
        "de": "Forsythie", "lat": "Forsythia x intermedia",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Der klassische Frühlingsbote, goldgelbe Blüte.",
    },
    "hamamelis_intermedia": {
        "de": "Zaubernuss", "lat": "Hamamelis x intermedia",
        "needs_acid_soil": True, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Blüht im Januar/Februar, oft duftend.",
    },
    "hibiscus_syriacus": {
        "de": "Garten-Eibisch", "lat": "Hibiscus syriacus",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Spätblüher im August/September.",
    },
    "hippophae_rhamnoides": {
        "de": "Sanddorn", "lat": "Hippophae rhamnoides", "native": True,
        "needs_acid_soil": False, "wind_resistence": "extrem", "drought_tolerance": "hoch",
        "note": "Vitaminreiche Früchte, braucht kalkhaltigen Boden.",
    },
    "hippophae_rhamnoides_pollmix": {
        "de": "Sanddorn (männlich)", "lat": "Hippophae rhamnoides 'Pollmix'", "native": True,
        "needs_acid_soil": False, "wind_resistence": "extrem", "drought_tolerance": "hoch",
        "note": "Bester Befruchter, extrem windfest (Dünenpflanze).",
    },
    "hydrangea_arborescens": {
        "de": "Wald-Hortensie", "lat": "Hydrangea arborescens",
        "needs_acid_soil": True, "wind_resistence": "mittel", "drought_tolerance": "gering",
        "note": "Sorte 'Annabelle' ist sehr beliebt, braucht viel Wasser.",
    },
    "hydrangea_macrophylla": {
        "de": "Bauernhortensie", "lat": "Hydrangea macrophylla",
        "needs_acid_soil": True, "wind_resistence": "mittel", "drought_tolerance": "gering",
        "note": "Klassische Hortensie, braucht Winterschutz.",
    },
    "hydrangea_paniculata": {
        "de": "Rispenhortensie", "lat": "Hydrangea paniculata",
        "needs_acid_soil": True, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Viel sonnenverträglicher als andere Hortensien.",
    },
    "ilex_aquifolium": {
        "de": "Europäische Stechpalme", "lat": "Ilex aquifolium", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "restriction": "Giftige Beeren, stachelige Blätter.",
    },
    "ilex_crenata": {
        "de": "Japanische Stechpalme", "lat": "Ilex crenata",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Bester Ersatz für Buchsbaum.",
    },
    "koelreuteria_paniculata": {
        "de": "Blasenbaum", "lat": "Koelreuteria paniculata",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "hoch",
        "note": "Gelbe Blüten im Juli, sehr dekorative Blasenfrüchte.",
    },
    "kolkwitzia_amabilis": {
        "de": "Perlmuttstrauch", "lat": "Kolkwitzia amabilis",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "hoch",
        "note": "Überreiche rosa Blüte, sehr anspruchslos.",
    },
    "magnolia_kobus": {
        "de": "Kobushi-Magnolie", "lat": "Magnolia kobus",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Eine der frosthärtesten Magnolien überhaupt.",
    },
    "magnolia_soulangeana": {
        "de": "Tulpen-Magnolie", "lat": "Magnolia x soulangeana",
        "needs_acid_soil": True, "wind_resistence": "gering", "drought_tolerance": "mittel",
        "note": "Prachtvoller Solitärbaum.",
    },
    "magnolia_stellata": {
        "de": "Stern-Magnolie", "lat": "Magnolia stellata",
        "needs_acid_soil": True, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Früheste Magnolie, bleibt kompakt.",
    },
    "malus": {
        "de": "Zierapfel", "lat": "Malus", "fire_blight_risk": True,
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Überreiche Blüte und kleiner Fruchtschmuck. Feuerbrand-Wirt!",
    },
    "malus_domestica": {
        "de": "Säulenapfel", "lat": "Malus domestica", "fire_blight_risk": True,
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Ideal für kleine Gärten und Kübel. Feuerbrand-Wirt!",
    },
    "philadelphus_coronarius": {
        "de": "Bauernjasmin", "lat": "Philadelphus coronarius",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Starker, angenehmer Duft.",
    },
    "physocarpus_opulifolius": {
        "de": "Fasanenspiere", "lat": "Physocarpus opulifolius",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Extrem robust, tolle Rindenstruktur.",
    },
    "physocarpus_opulifolius_diabolo": {
        "de": "Dunkelrote Fasanenspiere", "lat": "Physocarpus opulifolius 'Diabolo'",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Bietet tollen Farbkontrast (fast schwarz), extrem frosthart.",
    },
    "potentilla_fruticosa": {
        "de": "Fünffingerstrauch", "lat": "Potentilla fruticosa",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Extrem lange Blütezeit, sehr pflegeleicht.",
    },
    "prunus_mahaleb": {
        "de": "Steinweichsel", "lat": "Prunus mahaleb", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Heimisch, duftende Blüten, extrem trockenheitsfest.",
    },
    "prunus_serrulata": {
        "de": "Japanische Zierkirsche", "lat": "Prunus serrulata",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Symbol für den Frühling, keine essbaren Früchte.",
    },
    "prunus_spinosa": {
        "de": "Schlehe", "lat": "Prunus spinosa", "native": True, "fire_blight_risk": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Dornig, wertvoll für Vögel. Feuerbrand-Wirt!",
    },
    "pyracantha_coccinea": {
        "de": "Feuerdorn", "lat": "Pyracantha coccinea", "fire_blight_risk": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Immergrün, dornig, bunter Fruchtschmuck. Feuerbrand-Wirt!",
    },
    "rhododendron": {
        "de": "Rhododendron", "lat": "Rhododendron",
        "needs_acid_soil": True, "wind_resistence": "mittel", "drought_tolerance": "gering",
        "note": "Braucht saures Moorbeet (pH 4-5).",
    },
    "rhus_typhina": {
        "de": "Essigbaum", "lat": "Rhus typhina",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "hoch",
        "note": "Wunderschöne Färbung, Achtung: bildet Ausläufer!",
    },
    "ribes_alpinum": {
        "de": "Alpen-Johannisbeere", "lat": "Ribes alpinum", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Sehr schattenverträglich.",
    },
    "ribes_idaeus": {
        "de": "Himbeere", "lat": "Ribes idaeus", "native": True,
        "needs_acid_soil": True, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Ernte von Sommer bis Herbst je nach Sorte.",
    },
    "ribes_sanguineum": {
        "de": "Blut-Johannisbeere", "lat": "Ribes sanguineum",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Reiner Zierstrauch mit prächtiger Blüte.",
    },
    "rosa": {
        "de": "Strauchrose", "lat": "Rosa", "fire_blight_risk": True,
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Auf ADR-Prädikat achten. Feuerbrand-Wirt!",
    },
    "rosa_canina": {
        "de": "Hundsrose", "lat": "Rosa canina", "native": True, "fire_blight_risk": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Wichtige hagebutten-Quelle. Feuerbrand-Wirt!",
    },
    "rubus_sectio_rubus": {
        "de": "Brombeere", "lat": "Rubus sectio Rubus", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Wüchsig, braucht Rankhilfe.",
    },
    "salix_purpurea": {
        "de": "Purpur-Weide", "lat": "Salix purpurea", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Bienenweide, sehr gut für Uferbefestigung.",
    },
    "sambucus_nigra": {
        "de": "Schwarzer Holunder", "lat": "Sambucus nigra", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Blüten und Beeren sind vielseitig nutzbar.",
    },
    "spiraea_japonica_little_princess": {
        "de": "Zwerg-Spiere", "lat": "Spiraea japonica 'Little Princess'",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Kompakter Kleinstrauch, ideal für Einfassungen.",
    },
    "spiraea_vanhouttei": {
        "de": "Prachtspiere", "lat": "Spiraea x vanhouttei", "fire_blight_risk": True,
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Schneeweiße Blütenkaskaden im Mai. Feuerbrand-Wirt!",
    },
    "syringa_meyeri": {
        "de": "Zwerg-Flieder", "lat": "Syringa meyeri",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Perfekt für kleine Gärten und Kübel.",
    },
    "syringa_vulgaris": {
        "de": "Edelflieder", "lat": "Syringa vulgaris",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Der klassische Duftstrauch Mai-Juni.",
    },
    "tamarix_tetrandra": {
        "de": "Frühlings-Tamariske", "lat": "Tamarix tetrandra",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Filigraner Wuchs, salzverträglich, sehr hitzefest.",
    },
    "tetradium_daniellii": {
        "de": "Bienenbaum / Samtesche", "lat": "Tetradium daniellii",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Die ultimative Bienenweide im Spätsommer.",
    },
    "viburnum_carlesii": {
        "de": "Duft-Schneeball", "lat": "Viburnum carlesii",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Sensationeller Duft im Frühjahr.",
    },
    "viburnum_lantana": {
        "de": "Wolliger Schneeball", "lat": "Viburnum lantana", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Sehr trockenheitsresistent.",
    },
    "viburnum_opulus": {
        "de": "Gewöhnlicher Schneeball", "lat": "Viburnum opulus", "native": True,
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "gering",
        "note": "Liebt feuchtere Standorte.",
    },
    "weigela_florida": {
        "de": "Weigelie", "lat": "Weigela florida",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Blütenwunder im Vorsommer.",
    },

    # --- 5. HECKENPFLANZEN ---
    "buxus_sempervirens": {
        "de": "Buchsbaum", "lat": "Buxus sempervirens",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "restriction": "Starker Befall durch Buchsbaumzünsler möglich.",
    },
    "carpinus_betulus": {
        "de": "Hainbuche", "lat": "Carpinus betulus", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Sehr robust, wertvoll für Vögel.",
    },
    "carpinus_betulus_fastigiata": {
        "de": "Säulenhainbuche", "lat": "Carpinus betulus 'Fastigiata'", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Ideal für schmale Alleen oder als architektonisches Element.",
    },
    "carpinus_betulus_lucas": {
        "de": "Säulenhainbuche 'Lucas'", "lat": "Carpinus betulus 'Lucas'", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Noch schmaler als 'Fastigiata', idealer Sichtschutz für kleine Gärten.",
    },
    "cornus_alba_sibirica": {
        "de": "Purpur-Hartriegel", "lat": "Cornus alba 'Sibirica'",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Leuchtend rote Zweige im Winter, sehr dekorativ in lockeren Hecken.",
    },
    "ligustrum_vulgare": {
        "de": "Liguster", "lat": "Ligustrum vulgare", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Besonders robust, ökologisch wertvoll.",
    },
    "ligustrum_vulgare_atrovirens": {
        "de": "Wintergrüner Liguster", "lat": "Ligustrum vulgare 'Atrovirens'", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Die preiswerte, heimische Alternative zu Kirschlorbeer.",
    },
    "lonicera_nitida": {
        "de": "Immergrüne Heckenkirsche", "lat": "Lonicera nitida",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Sehr schnittverträglicher, niedriger Heckenersatz.",
    },
    "photinia_fraseri_red_robin": {
        "de": "Glanzmispel 'Red Robin'", "lat": "Photinia x fraseri 'Red Robin'", "fire_blight_risk": True,
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Immergrün mit leuchtend rotem Austrieb. Feuerbrand-Wirt!",
    },
    "prunus_laurocerasus": {
        "de": "Kirschlorbeer", "lat": "Prunus laurocerasus",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "restriction": "Giftig, breitet sich in Wäldern aus (problematisch).",
    },
    "prunus_lusitanica": {
        "de": "Portugiesischer Kirschlorbeer", "lat": "Prunus lusitanica",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Hitzefester und eleganter als der herkömmliche Kirschlorbeer.",
    },
    "prunus_lusitanica_angustifolia": {
        "de": "Portugiesischer Kirschlorbeer (Sorte)", "lat": "Prunus lusitanica 'Angustifolia'",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Eleganter als der normale Kirschlorbeer, sehr hitzefest (pannonisch erprobt).",
    },

    # --- 6. BLÜTENSTAUDEN & ALPINSTAUDEN ---
    "achillea_millefolium": {
        "de": "Schafgarbe", "lat": "Achillea millefolium", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Heilpflanze, sehr trockenheitsresistent.",
    },
    "aconitum_napellus": {
        "de": "Blauer Eisenhut", "lat": "Aconitum napellus", "native": True,
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "gering",
        "restriction": "EXTREM GIFTIG! Nicht in Reichweite von Kindern pflanzen.",
    },
    "actaea_simplex": {
        "de": "Garten-Silberkerze", "lat": "Actaea simplex",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "gering",
        "note": "Duftende Spätblüher für halbschattige Lagen.",
    },
    "anemone_hupehensis": {
        "de": "Herbst-Anemone", "lat": "Anemone hupehensis",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Lange Blütezeit bis in den Spätherbst.",
    },
    "armeria_maritima": {
        "de": "Grasnelke", "lat": "Armeria maritima",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Salzverträglich! Ideal für Beete an straßenseitigen Zäunen.",
    },
    "aster_novi_belgii": {
        "de": "Glattblatt-Aster", "lat": "Symphyotrichum novi-belgii",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Wichtige späte Nahrungsquelle für Bienen.",
    },
    "astilbe": {
        "de": "Prachtspiere", "lat": "Astilbe",
        "needs_acid_soil": True, "wind_resistence": "gering", "drought_tolerance": "gering",
        "note": "Prächtige Blütenwedel für schattige, feuchte Standorte.",
    },
    "astrantia_major": {
        "de": "Sterndolde", "lat": "Astrantia major", "native": True,
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "gering",
        "note": "Filigrane Wildstaude für halbschattige Plätze.",
    },
    "aubrieta": {
        "de": "Blaukissen", "lat": "Aubrieta",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Klassische Polsterstaude für Steinmauern.",
    },
    "campanula": {
        "de": "Glockenblume", "lat": "Campanula", "native": True,
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Zahlreiche heimische Arten vorhanden.",
    },
    "carlina_acaulis": {
        "de": "Silberdistel", "lat": "Carlina acaulis", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Steirische Charakterpflanze, sehr dekorativ im trockenen Zustand.",
    },
    "coreopsis": {
        "de": "Mädchenauge", "lat": "Coreopsis",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "hoch",
        "note": "Dauerblüher für vollsonnige Beete.",
    },
    "delphinium": {
        "de": "Rittersporn", "lat": "Delphinium",
        "needs_acid_soil": False, "wind_resistence": "gering", "drought_tolerance": "mittel",
        "restriction": "Giftig. Braucht viele Nährstoffe und Stützen.",
    },
    "echinacea_purpurea": {
        "de": "Purpur-Sonnenhut", "lat": "Echinacea purpurea",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "hoch",
        "note": "Magnet für Bienen und Schmetterlinge.",
    },
    "echinops_ritro": {
        "de": "Kugeldistel", "lat": "Echinops ritro",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Trockenheitsresistent, sehr dekorative blaue Köpfe.",
    },
    "erica_carnea": {
        "de": "Schneeheide / Winterheide", "lat": "Erica carnea", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Wichtige frühe Bienenweide, blüht oft schon im Schnee.",
    },
    "gaura_lindheimeri": {
        "de": "Prachtkerze", "lat": "Gaura lindheimeri",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "hoch",
        "note": "Leichte Staude, braucht durchlässigen Boden.",
    },
    "gentiana_acaulis": {
        "de": "Stängelloser Enzian", "lat": "Gentiana acaulis", "native": True,
        "needs_acid_soil": True, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Alpiner Klassiker, braucht kalkarmen Boden und gute Drainage.",
    },
    "helenium": {
        "de": "Sonnenbraut", "lat": "Helenium",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Prachtvolle Spätsommerstaude für volle Sonne.",
    },
    "helleborus_niger": {
        "de": "Christrose", "lat": "Helleborus niger", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Blüht im tiefsten Winter.",
    },
    "hemerocallis": {
        "de": "Taglilie", "lat": "Hemerocallis",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Essbare Blüten, sehr langlebig und pflegeleicht.",
    },
    "heuchera": {
        "de": "Purpurglöckchen", "lat": "Heuchera",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Enorme Farbvielfalt beim Laub.",
    },
    "iris_barbata": {
        "de": "Schwertlilie", "lat": "Iris barbata",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "hoch",
        "note": "Braucht vollsonnige Plätze und trockene Rhizome.",
    },
    "kniphofia": {
        "de": "Fackellilie", "lat": "Kniphofia",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Exotische Optik, braucht Winterschutz bei Staunässe.",
    },
    "lavandula_angustifolia": {
        "de": "Lavendel", "lat": "Lavandula angustifolia",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Braucht kargen Boden und jährlichen Rückschnitt.",
    },
    "lavandula_angustifolia_hidcote": {
        "de": "Lavendel 'Hidcote Blue'", "lat": "Lavandula angustifolia",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Tiefblaue Sorte, sehr kompakt und winterhart.",
    },
    "leontopodium_alpinum": {
        "de": "Edelweiß", "lat": "Leontopodium alpinum", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Symbolpflanze der Alpen, braucht kalkhaltigen Schotter.",
    },
    "leucanthemum_superbum": {
        "de": "Garten-Margerite", "lat": "Leucanthemum x superbum",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Klassiker für den Bauerngarten.",
    },
    "lupinus": {
        "de": "Lupine", "lat": "Lupinus",
        "needs_acid_soil": True, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Stickstoffsammler, verbessert den Boden.",
    },
    "nepeta_faassenii": {
        "de": "Katzenminze", "lat": "Nepeta x faassenii",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "hoch",
        "note": "Dauerblüher, wirkt anziehend auf Katzen.",
    },
    "paeonia_lactiflora": {
        "de": "Pfingstrose", "lat": "Paeonia lactiflora",
        "needs_acid_soil": False, "wind_resistence": "gering", "drought_tolerance": "mittel",
        "note": "Extrem langlebig, mag keine Umpflanzung.",
    },
    "papaver_orientale": {
        "de": "Türkenmohn", "lat": "Papaver orientale",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Zieht nach der Blüte komplett ein.",
    },
    "perovskia_atriplicifolia": {
        "de": "Blauraute", "lat": "Perovskia atriplicifolia",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "hoch",
        "note": "Spätsommerblüher, sehr trockenheitsresistent.",
    },
    "phlox_paniculata": {
        "de": "Hohe Flammenblume", "lat": "Phlox paniculata",
        "needs_acid_soil": False, "wind_resistence": "gering", "drought_tolerance": "mittel",
        "note": "Klassische Beetstaude mit starkem Duft.",
    },
    "phlox_subulata": {
        "de": "Polster-Phlox", "lat": "Phlox subulata",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Farbenfroher Bodendecker für das Frühjahr.",
    },
    "physostegia_virginiana": {
        "de": "Gelenkblume", "lat": "Physostegia virginiana",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Interessante Blütenform, sehr standfest.",
    },
    "pulsatilla_vulgaris": {
        "de": "Küchenschelle", "lat": "Pulsatilla vulgaris", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "restriction": "Giftig. Steht unter Naturschutz.",
    },
    "rudbeckia_fulgida": {
        "de": "Sonnenhut", "lat": "Rudbeckia fulgida var. sullivantii",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Dauerblüher in leuchtendem Gelb, sehr robust.",
    },
    "salvia_nemorosa": {
        "de": "Gartensalbei", "lat": "Salvia nemorosa",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "hoch",
        "note": "Absoluter Insektenmagnet, Rückschnitt nach erster Blüte.",
    },
    "salvia_nemorosa_caradonna": {
        "de": "Steppensalbei 'Caradonna'", "lat": "Salvia nemorosa",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Dunkelviolette Stängel, sehr modern in der Gestaltung.",
    },
    "saxifraga_arendsii": {
        "de": "Moos-Steinbrech", "lat": "Saxifraga x arendsii", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Bildet dichte Polster, ideal für Steingärten und Grabbepflanzungen.",
    },
    "sedum": {
        "de": "Fetthenne", "lat": "Sedum",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Überlebt extreme Trockenheit auf Dächern und Mauern.",
    },
    "sedum_telephium": {
        "de": "Hohe Fetthenne", "lat": "Sedum telephium",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Wichtige Nahrungsquelle für späte Schmetterlinge.",
    },
    "solidago": {
        "de": "Goldrute", "lat": "Solidago",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Spätblühend, ökologisch wertvoll aber teils invasiv.",
    },
    "verbascum": {
        "de": "Königskerze", "lat": "Verbascum", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Zweijährig, sät sich gerne selbst aus.",
    },

    # --- 7. BODENDECKER, FARNE & KLETTERPFLANZEN ---
    "alchemilla_mollis": {
        "de": "Frauenmantel", "lat": "Alchemilla mollis",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Robustester Bodendecker, fängt Tautropfen dekorativ auf.",
    },
    "bergenia_cordifolia": {
        "de": "Bergenie", "lat": "Bergenia cordifolia",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Wintergrünes Laub, extrem anspruchslos.",
    },
    "brunnera_macrophylla": {
        "de": "Kaukasus-Vergissmeinnicht", "lat": "Brunnera macrophylla",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Hervorragender Blattschmuck für den Schatten.",
    },
    "carex_morrowi_ice_dance": {
        "de": "Japan-Segge 'Ice Dance'", "lat": "Carex morrowi",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Wintergrünes Gras, das im Schatten hell leuchtet.",
    },
    "cyclamen_purpurascens": {
        "de": "Europäisches Alpenveilchen", "lat": "Cyclamen purpurascens", "native": True,
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "gering",
        "note": "Heimisch in steirischen Buchenwäldern, liebt Humus und Schatten.",
    },
    "dryas_octopetala": {
        "de": "Silberwurz", "lat": "Dryas octopetala", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Alpiner Bodendecker, sehr langlebig.",
    },
    "dryopteris_filix_mas": {
        "de": "Wurmfarn", "lat": "Dryopteris filix-mas", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Der Klassiker unter den Farnen, extrem winterhart und robust.",
    },
    "epimedium": {
        "de": "Elfenblume", "lat": "Epimedium",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Bester Bodendecker für den trockenen Schatten unter Bäumen.",
    },
    "geranium": {
        "de": "Storchschnabel", "lat": "Geranium", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Vielseitigster Bodendecker für Sonne und Schatten.",
    },
    "geranium_rozanne": {
        "de": "Storchschnabel 'Rozanne'", "lat": "Geranium 'Gerwat'",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Der Weltmeister unter den Bodendeckern: Blüht von Juni bis November.",
    },
    "hedera_helix": {
        "de": "Efeu", "lat": "Hedera helix", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Immergrüner Kletterkünstler, ökologisch sehr wertvoll.",
    },
    "hosta": {
        "de": "Funkie", "lat": "Hosta",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "gering",
        "note": "Königin der Schattenpflanzen, schneckenanfällig.",
    },
    "hydrangea_petiolaris": {
        "de": "Kletterhortensie", "lat": "Hydrangea petiolaris",
        "needs_acid_soil": True, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "note": "Perfekt für schattige Nordwände.",
    },
    "iberis_sempervirens": {
        "de": "Schleifenblume", "lat": "Iberis sempervirens",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Immergrüner Kissenbildner.",
    },
    "lonicera_pileata": {
        "de": "Heckenmyrte", "lat": "Lonicera pileata",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Robuster Bodendecker, auch für Böschungen.",
    },
    "mentha": {
        "de": "Teppich-Minze", "lat": "Mentha",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Duftender Bodendecker, kann wuchern.",
    },
    "pachysandra_terminalis": {
        "de": "Ysandre / Schattengrün", "lat": "Pachysandra terminalis",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Das 'Arbeitstier' unter den Bodendeckern für tiefen Schatten.",
    },
    "parthenocissus_tricuspidata": {
        "de": "Wilder Wein", "lat": "Parthenocissus tricuspidata",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Selbstklimmende Fassadenbegrünung.",
    },
    "sempervivum_tectorum": {
        "de": "Echte Hauswurz", "lat": "Sempervivum tectorum", "native": True,
        "needs_acid_soil": False, "wind_resistence": "extrem", "drought_tolerance": "extrem",
        "note": "Überlebt auf nacktem Stein, absolut unzerstörbar.",
    },
    "stachys_byzantina": {
        "de": "Woll-Ziest", "lat": "Stachys byzantina",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "hoch",
        "note": "Kuschelig weiches Laub, sehr trockenresistent.",
    },
    "vinca_minor": {
        "de": "Immergrün", "lat": "Vinca minor", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Anspruchsloser Bodendecker für Halbschatten.",
    },
    "viola_odorata": {
        "de": "Duftveilchen", "lat": "Viola odorata", "native": True,
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Verbreitet sich durch Ameisen im Garten.",
    },
    "waldsteinia_ternata": {
        "de": "Golderdbeere", "lat": "Waldsteinia ternata",
        "needs_acid_soil": False, "wind_resistence": "hoch", "drought_tolerance": "mittel",
        "note": "Dichter, robuster Bodendecker, blüht gelb.",
    },
    "wisteria_sinensis": {
        "de": "Blauregen", "lat": "Wisteria sinensis",
        "needs_acid_soil": False, "wind_resistence": "mittel", "drought_tolerance": "mittel",
        "restriction": "Starker Schlinger, braucht sehr stabile Kletterhilfen.",
    },
}


def check_plant(plant_id, is_protection_area, plz=""):
    info = PLANTS_REGISTRY.get(plant_id)
    if not info:
        return "Fehler: Pflanze nicht gefunden."

    name_display = f"{info['de']} ({info['lat']})"
    lat_name = info.get("lat", "").lower()

    # --- 1. MODERNE FEUERBRAND-LOGIK (Stand 2026) ---
    if is_protection_area and info.get("fire_blight_risk"):
        if str(plz).startswith("8"):
            # AUSNAHME: Malus (Apfel/Zierapfel) & Pyrus (Birne) sind wieder erlaubt
            # Nur Cotoneaster, Crataegus und Pyracantha bleiben strikt verboten
            if "malus" in lat_name or "pyrus" in lat_name:
                return f"⚠️ HINWEIS: '{name_display}' ist ein Feuerbrand-Wirt. Pflanzung in der Steiermark erlaubt, aber meldepflichtig bei Befall!"

            # Die echte Verbotsliste (Kernliste)
            return f"🚫 PFLANZVERBOT: '{name_display}' ist in der Steiermark aufgrund der Feuerbrand-Verordnung (Kernliste) untersagt!"

        return f"⚠️ GEFAHR: '{name_display}' ist ein Feuerbrand-Wirt!"

    # Check 2: Einschränkungen/Hinweise
    if "restriction" in info:
        return f"ℹ️ INFO: {info['restriction']}"

    return "✅ Geeignet: Keine spezifischen Pflanzverbote bekannt."


def get_restricted_plants(is_protection_area):
    res = []
    for p_id, info in PLANTS_REGISTRY.items():
        if (
            is_protection_area and info.get("fire_blight_risk")
        ) or "restriction" in info:
            res.append(f"- {info['de']} ({info['lat']})")
    return res