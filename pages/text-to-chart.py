import streamlit as st
from openai import OpenAI
import pandas as pd
import altair as alt
import json

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
openAI_model = "gpt-4o-mini"

st.set_page_config(layout="wide")
main_heading=st.title("AI Text-Chart Demo")
st.info("""
Gib in diesem Textfeld den Ablauf deines Vorhabens an.

Jede Aufgabe sollte mindestens eine Startzeit oder Abhängigkeit zu einem Vorgänger enthalten. Außerdem wird eine Endzeit oder eine Dauer benötigt.

Verwende klare Formulierungen für Abhängigkeiten, z.B. "beginnt nach Abschluss von...", "startet wenn... beendet ist".
Die KI wird fehlende Informationen basierend auf den angegebenen Abhängigkeiten und Dauern bestmöglich ergänzen.
""")

st.success("""
Beispiel:
"Unser App-Entwicklungsprojekt beginnt mit der Marktanalyse, die 2 Monate dauert. 
Anschließend starten wir das Design und Prototyping, das 3 Monate in Anspruch nimmt. 
Die Entwicklung der Kernfunktionen beginnt einen Monat nach Start des Designs und dauert 5 Monate. 
Parallel zur Entwicklung, ab deren Halbzeit, implementieren wir zusätzliche Features über einen Zeitraum von 3 Monaten. 
Die interne Testphase startet, sobald die Kernentwicklung abgeschlossen ist, und läuft 2 Monate. 
Direkt im Anschluss führen wir einen zweimonatigen Closed Beta-Test durch. 
Die Marketingkampagne beginnt 1 Monat vor dem geplanten Launch am Ende des Betatests."
""")



#--Sidebar ---------------------------------------------------------------------------------------------------------------------------------------
st.sidebar.title("App-Steuerung")

# Chart Logik ---------------------------------------------------------------------------------------------------------------------------------------
def get_chart_data(prompt):
    response = client.chat.completions.create(
        model=openAI_model,
        messages=[
            {"role": "system", "content": "Du bist ein Assistent, der Projektpläne in strukturierte Daten umwandelt."},
            {"role": "user", "content": f"""
Wandle den folgenden Projektplan in ein JSON-Array um, das für ein Gantt-Chart mit Abhängigkeiten geeignet ist. 
Jedes Objekt sollte 'Aufgabe', 'Start', 'Ende' und 'Abhängigkeiten' enthalten. 
'Start' und 'Ende' sollten numerische Werte sein, die die Monate seit Projektbeginn darstellen. 
'Abhängigkeiten' sollte ein Array von Indizes der Aufgaben sein, von denen diese Aufgabe abhängt.
Gib NUR das JSON-Array zurück, ohne zusätzlichen Text.
Beispielformat:
[
    {{"Aufgabe": "Aufgabe 1", "Start": 0, "Ende": 2, "Abhängigkeiten": []}},
    {{"Aufgabe": "Aufgabe 2", "Start": 1, "Ende": 3, "Abhängigkeiten": [0]}}
]

Hier ist der Plan:

{prompt}
"""}
        ],
        temperature=0.7,
    )
    
    try:
        return json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        st.error("Fehler beim Parsen der API-Antwort. Bitte versuchen Sie es erneut.")
        return []

def build_chart(data, use_container_width: bool):
    if not data:
        st.warning("Keine gültigen Daten für das Chart vorhanden.")
        return
    
    df = pd.DataFrame(data)
    
    # Sortiere die Aufgaben
    df['hat_abhängigkeiten'] = df['Abhängigkeiten'].apply(lambda x: len(x) > 0)
    df = df.sort_values(['hat_abhängigkeiten', 'Start'])
    
    # Erstelle eine benutzerdefinierte Reihenfolge für die Y-Achse
    df['y_order'] = range(len(df))
    
    # Berechne die maximale Projektdauer
    max_end = df['Ende'].max()
    
    # Basis-Chart für Balken
    base = alt.Chart(df).encode(
        y=alt.Y('y_order:O', axis=alt.Axis(title='Aufgaben'), sort='ascending'),
        x=alt.X('Start:Q', 
                axis=alt.Axis(
                    title='Zeit (Monate)', 
                    values=list(range(int(max_end)+1)),
                    tickMinStep=1,
                    format='d'
                )
        ),
        x2='Ende:Q'
    )

    # Balken für Aufgaben
    bars = base.mark_bar().encode(
        color=alt.Color('Aufgabe:N', legend=None)
    )

    # Texte für Aufgaben
    text = base.mark_text(
        align='left',
        baseline='middle',
        dx=5
    ).encode(
        text='Aufgabe:N'
    )

    # Erstelle eine separate DataFrame für die Abhängigkeiten
    dependencies = []
    for i, row in df.iterrows():
        for dep in row['Abhängigkeiten']:
            dependencies.append({
                'von_aufgabe': df.loc[dep, 'Aufgabe'],
                'zu_aufgabe': row['Aufgabe'],
                'von_ende': df.loc[dep, 'Ende'],
                'zu_start': row['Start'],
                'von_y': df.loc[dep, 'y_order'],
                'zu_y': row['y_order']
            })
    dep_df = pd.DataFrame(dependencies)

    # Pfeile für Abhängigkeiten
    arrows = alt.Chart(dep_df).mark_line(
        color='red',
        strokeWidth=1,
        strokeDash=[2, 2],
        point=alt.OverlayMarkDef(color='red', shape='triangle-right', size=60)
    ).encode(
        x='von_ende:Q',
        y='von_y:O',
        x2='zu_start:Q',
        y2='zu_y:O'
    )

    chart = (bars + text + arrows).properties(
        width=600,
        height=400
    ).interactive()

    st.altair_chart(chart, theme="streamlit", use_container_width=use_container_width)
    
    # Zeige die sortierten Daten an (optional, für Debugging)
    st.write(df[['Aufgabe', 'Start', 'Ende', 'Abhängigkeiten']])

# Eingabefelder ---------------------------------------------------------------------------------------------------------------------------------------
if 'inputtext' not in st.session_state:
    st.session_state.inputtext = ""

st.session_state.inputtext = st.text_area("Beschreiben Sie Ihr Vorhaben mit Aufgaben und zeitlichem Ablauf", value=st.session_state.inputtext, height=200)

if st.button("Gantt-Chart erstellen"):
    if st.session_state.inputtext:
        with st.spinner("Erstelle Gantt-Chart..."):
            chart_data = get_chart_data(st.session_state.inputtext)
            st.divider()
            build_chart(chart_data, True)
    else:
        st.warning("Bitte geben Sie zuerst eine Beschreibung Ihres Vorhabens ein.")

