# Claude Sonnet 4.6 generiert 

# Investor Profile, Risikoprofil Fragebogen

# Ergebnis-Kategorien:
#   - Konservativ  (Score  0–12): Sicherheitsorientierter Anleger
#   - Ausgewogen   (Score 13–20): Anleger mit moderatem Risiko
#   - Dynamisch    (Score 21–28): Renditeorientierter Anleger
#   - Aggressiv    (Score 29–32): Hochrisikoanleger

import streamlit as st

# Seiteneinstellungen

st.set_page_config(
    page_title="Investor-Profil",
    page_icon="📊",
    layout="centered",
)


# Benutzerdefiniertes CSS –> macht die App ansprechender

st.markdown(
    """
    <style>
        /* Hintergrundfarbe der gesamten App */
        .stApp { background-color: #f0f4f8; }

        /* Titel-Stil */
        h1 { color: #1a3c5e; font-family: 'Georgia', serif; }

        /* Radio-Button-Gruppe: Karten-Optik */
        div[data-testid="stRadio"] > label {
            background: #ffffff;
            border: 1px solid #d0dce8;
            border-radius: 10px;
            padding: 6px 14px;
            margin-bottom: 4px;
            display: block;
            transition: background 0.2s;
        }
        div[data-testid="stRadio"] > label:hover {
            background: #dbeafe;
        }

        /* Slider-Farbe */
        .stSlider > div { color: #1a3c5e; }

        /* Ergebnis-Box */
        .result-box {
            background: #1a3c5e;
            color: white;
            border-radius: 14px;
            padding: 24px 28px;
            margin-top: 20px;
            font-size: 1.1rem;
            line-height: 1.7;
        }
        .result-box h2 { color: #93c5fd; margin-bottom: 8px; }

        /* Fortschritts-Beschriftung */
        .progress-label {
            font-size: 0.85rem;
            color: #64748b;
            margin-bottom: -8px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# Kopfbereich

st.title("📊 Investor-Profil Fragebogen")
st.markdown(
    """
    Willkommen! Dieser kurze Fragebogen hilft uns, dein persönliches
    **Risikoprofil** zu bestimmen, damit wir dir passende Finanzprodukte
    empfehlen können. Beantworte bitte alle Fragen ehrlich.
    """
)
st.divider()



# Hilfsfunktion: Frage mit Radio-Buttons anzeigen

# Parameter:
#   frage_nr   – Laufende Fragennummer (für die Anzeige)
#   frage_text – Der eigentliche Fragetext
#   optionen   – Liste aus (Anzeigetext, Punktwert)-Paaren
#                Der Punktwert fliesst in den Risiko-Score ein
# Rückgabe:
#   Punktwert der gewählten Antwort (0 wenn noch nichts gewählt)


def zeige_frage(frage_nr, frage_text, optionen):

    # Nur die Anzeige-Texte aus den Optionen herausziehen
    anzeige_texte = [opt[0] for opt in optionen]

    # Frage anzeigen
    st.markdown(f"**Frage {frage_nr}:** {frage_text}")

    # Radio-Buttons anzeigen, keine Vorauswahl (index=None)
    auswahl = st.radio(
        label=f"q{frage_nr}",           # internes Label (nicht sichtbar)
        options=anzeige_texte,
        index=None,                     # Nutzer muss aktiv eine Option wählen
        label_visibility="collapsed",   # Label ausblenden, Frage steht schon oben
        key=f"frage_{frage_nr}",
    )

    # Punktwert der gewählten Antwort suchen und zurückgeben
    if auswahl is not None:
        for text, punkte in optionen:
            if text == auswahl:
                return punkte

    return 0  # noch keine Antwort gegeben → 0 Punkte



# Hilfsfunktion: Slider-Frage anzeigen

# Parameter:
#   frage_nr           – Laufende Fragennummer
#   frage_text         – Der Fragetext
#   min_val            – Minimaler Slider-Wert
#   max_val            – Maximaler Slider-Wert
#   schritt            – Schrittgrösse des Sliders
#   punkte_pro_einheit – Wie viele Risikopunkte pro Einheit des Sliders
# Rückgabe:
#   Berechneter Punktwert (gerundet)

def zeige_slider_frage(frage_nr, frage_text, min_val, max_val, schritt, punkte_pro_einheit):

    # Frage anzeigen
    st.markdown(f"**Frage {frage_nr}:** {frage_text}")

    # Slider anzeigen
    wert = st.slider(
        label=f"slider_{frage_nr}",
        min_value=min_val,
        max_value=max_val,
        step=schritt,
        value=min_val,
        label_visibility="collapsed",
        key=f"slider_frage_{frage_nr}",
    )

    # Punktwert berechnen und zurückgeben
    return round(wert * punkte_pro_einheit)



# Hilfsfunktion: Risikoprofil aus dem Score ermitteln

# Parameter:
#   score – Summe aller Punkte aus dem Fragebogen
# Rückgabe:
#   Tupel aus (Profil-Name, Emoji, Beschreibung)

def bestimme_profil(score):

    if score <= 12:
        # Tiefer Score → sicherheitsorientiert
        return (
            "Konservativ",
            "🛡️",
            "Du legst grossen Wert auf Sicherheit. Verluste bereiten dir grosse "
            "Sorgen. Empfohlen werden Produkte mit geringem Risiko wie "
            "Sparkonten, Staatsanleihen oder konservative Fonds.",
        )
    elif score <= 20:
        # Mittlerer Score → ausgewogen
        return (
            "Ausgewogen",
            "⚖️",
            "Du akzeptierst ein moderates Risiko für eine etwas höhere Rendite. "
            "Gemischte Portfolios aus Aktien und Anleihen passen gut zu dir.",
        )
    elif score <= 28:
        # Hoher Score → dynamisch
        return (
            "Dynamisch",
            "🚀",
            "Du bist renditeorientiert und kannst mit temporären Verlusten umgehen. "
            "Aktien-ETFs, Wachstumsfonds und diversifizierte Aktienportfolios "
            "sind für dich geeignet.",
        )
    else:
        # Sehr hoher Score → aggressiv
        return (
            "Aggressiv",
            "⚡",
            "Du strebst nach maximaler Rendite und nimmst dafür hohes Risiko in Kauf. "
            "Einzelaktien, Krypto oder Hebelprodukte können Teil deines Portfolios "
            "sein – aber sei dir der Verlustrisiken bewusst!",
        )



# FRAGEBOGEN (8 Fragen)


# Zähler für beantwortete Fragen und den Gesamt-Score
beantwortet = 0
gesamt_score = 0


# Frage 1: Anlagehorizont (Slider)

punkte = zeige_slider_frage(
    frage_nr=1,
    frage_text="Wie lange möchtest du dein Geld anlegen? (in Jahren)",
    min_val=1,
    max_val=30,
    schritt=1,
    punkte_pro_einheit=0.13,   # max. ~4 Punkte bei 30 Jahren
)
gesamt_score += punkte
# Slider gilt als beantwortet, wenn er über dem Minimum liegt
if st.session_state.get("slider_frage_1", 1) > 1:
    beantwortet += 1
st.divider()


# Frage 2: Finanzieller Puffer

punkte = zeige_frage(
    frage_nr=2,
    frage_text="Falls du deinen Job verlieren würdest – wie lange könntest du "
               "deinen Lebensstandard halten, ohne das Investitionskapital anzutasten?",
    optionen=[
        ("Weniger als 3 Monate",  0),
        ("3–6 Monate",            1),
        ("6–12 Monate",           3),
        ("Mehr als 12 Monate",    4),
    ],
)
gesamt_score += punkte
if st.session_state.get("frage_2") is not None:
    beantwortet += 1
st.divider()


# Frage 3: Verlusttoleranz

punkte = zeige_frage(
    frage_nr=3,
    frage_text="Stell dir vor, dein Depot verliert innerhalb eines Monats 20 % an Wert. "
               "Was würdest du tun?",
    optionen=[
        ("Sofort alles verkaufen – das ist zu viel für mich.",        0),
        ("Einen Teil verkaufen, um das Risiko zu reduzieren.",        1),
        ("Abwarten und nichts unternehmen.",                          3),
        ("Nachkaufen – das ist eine gute Kaufgelegenheit!",           4),
    ],
)
gesamt_score += punkte
if st.session_state.get("frage_3") is not None:
    beantwortet += 1
st.divider()


# Frage 4: Anlageziel

punkte = zeige_frage(
    frage_nr=4,
    frage_text="Was ist dein primäres Ziel mit dieser Anlage?",
    optionen=[
        ("Kapitalerhalt – ich möchte nichts verlieren.",              0),
        ("Regelmässige Ausschüttungen / passives Einkommen.",         2),
        ("Langfristiger Vermögensaufbau.",                            3),
        ("Maximale Rendite – Risiko ist mir egal.",                   4),
    ],
)
gesamt_score += punkte
if st.session_state.get("frage_4") is not None:
    beantwortet += 1
st.divider()


# Frage 5: Erfahrung mit Finanzprodukten

punkte = zeige_frage(
    frage_nr=5,
    frage_text="Wie viel Erfahrung hast du mit Finanzprodukten?",
    optionen=[
        ("Keine – ich bin absoluter Anfänger.",                  0),
        ("Ich habe ein Sparkonto oder Anlagefonds.",              1),
        ("Ich handle gelegentlich Aktien oder ETFs.",             3),
        ("Ich kenne Optionen, Futures oder andere Derivate.",     4),
    ],
)
gesamt_score += punkte
if st.session_state.get("frage_5") is not None:
    beantwortet += 1
st.divider()


# Frage 6: Anteil des Einkommens

punkte = zeige_frage(
    frage_nr=6,
    frage_text="Welchen Anteil deines monatlichen Einkommens kannst du investieren, "
               "ohne deinen Alltag einzuschränken?",
    optionen=[
        ("Weniger als 5 %",  0),
        ("5–15 %",           1),
        ("15–30 %",          3),
        ("Mehr als 30 %",    4),
    ],
)
gesamt_score += punkte
if st.session_state.get("frage_6") is not None:
    beantwortet += 1
st.divider()


# Frage 7: Emotionale Reaktion auf verlorene Gewinne

punkte = zeige_frage(
    frage_nr=7,
    frage_text="Wie würdest du dich fühlen, wenn deine Anlage 30 % gestiegen ist, "
               "dann aber wieder auf den Ausgangspunkt zurückfällt?",
    optionen=[
        ("Ich wäre sehr frustriert – der Gewinn war real für mich.",   0),
        ("Ich wäre enttäuscht, aber es ist ok.",                       2),
        ("Ärgerlich, aber ich würde es als Lernchance sehen.",         3),
        ("Kein Problem – langfristig wird es wieder steigen.",         4),
    ],
)
gesamt_score += punkte
if st.session_state.get("frage_7") is not None:
    beantwortet += 1
st.divider()


# Frage 8: Strategie-Präferenz

punkte = zeige_frage(
    frage_nr=8,
    frage_text="Welche Strategie klingt für dich attraktiver?",
    optionen=[
        ("Alles sicher anlegen – lieber weniger Rendite, aber keine Verluste.", 0),
        ("Breite Streuung über viele Anlageklassen (ETF-Portfolio).",           2),
        ("Mischung aus sicheren und risikoreichen Anlagen.",                    3),
        ("Gezielt in wenige, hochrentable Titel investieren.",                  4),
    ],
)
gesamt_score += punkte
if st.session_state.get("frage_8") is not None:
    beantwortet += 1
st.divider()


# Fortschrittsanzeige (zeigt wie viele Fragen schon beantwortet sind)

st.markdown(
    f'<p class="progress-label">Fortschritt: {beantwortet} / 8 Fragen beantwortet</p>',
    unsafe_allow_html=True,
)
st.progress(beantwortet / 8)

st.markdown("###")  # etwas Abstand


# Ergebnis-Button

# Wenn der Nutzer klickt, wird der Score ausgewertet und das
# Risikoprofil mit Beschreibung angezeigt.
# Falls noch Fragen offen sind, erscheint eine Warnung.

if st.button("✅ Mein Risikoprofil anzeigen", use_container_width=True):

    if beantwortet < 8:
        # Warnung anzeigen, wenn noch nicht alle Fragen beantwortet wurden
        st.warning(
            f"⚠️  Bitte beantworte alle 8 Fragen. "
            f"Du hast noch {8 - beantwortet} Frage(n) offen."
        )
    else:
        # Profil anhand des Scores bestimmen
        profil_name, emoji, beschreibung = bestimme_profil(gesamt_score)

        # Ergebnis-Box anzeigen
        st.markdown(
            f"""
            <div class="result-box">
                <h2>{emoji} Dein Risikoprofil: {profil_name}</h2>
                <p>{beschreibung}</p>
                <hr style="border-color:#4b7ab5; margin: 14px 0;">
                <p style="font-size:0.9rem; color:#93c5fd;">
                    Dein Score: <strong>{gesamt_score} / 32</strong>
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Score als Fortschrittsbalken visualisieren
        st.markdown("#### Score-Übersicht")
        st.progress(gesamt_score / 32)
        st.caption(
            "0 = sehr konservativ  |  32 = sehr aggressiv  "
            f"|  Dein Wert: {gesamt_score}"
        )
