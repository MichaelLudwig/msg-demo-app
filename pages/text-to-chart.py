import streamlit as st
from openai import OpenAI
import pandas as pd
import altair as alt
import json

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
openAI_model = "gpt-4o-mini"

st.set_page_config(layout="wide")
main_heading=st.title("AI Text-Chart Demo")

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
    
    source = pd.DataFrame(data)
    
    # Basis-Chart für Balken
    base = alt.Chart(source).encode(
        y=alt.Y('Aufgabe:N', sort='-x'),
        x=alt.X('Start:Q', axis=alt.Axis(title='Zeit (Monate)')),
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

    # Pfeile für Abhängigkeiten
    arrows = alt.Chart(source).mark_line(
        color='red',
        strokeWidth=1,
        strokeDash=[2, 2],
        point=alt.OverlayMarkDef(color='red', shape='triangle-right')
    ).encode(
        x='Ende:Q',
        y='Aufgabe:N',
        detail='Aufgabe:N',
        href='Abhängigkeiten:N'
    ).transform_lookup(
        lookup='Abhängigkeiten',
        from_=alt.LookupData(source, 'Aufgabe', ['Start', 'Aufgabe'])
    )

    chart = (bars + text + arrows).properties(
        width=600,
        height=400
    ).interactive()

    st.altair_chart(chart, theme="streamlit", use_container_width=use_container_width)
    st.write(data)

# Eingabefelder ---------------------------------------------------------------------------------------------------------------------------------------
if 'inputtext' not in st.session_state:
    st.session_state.inputtext = ""

st.session_state.inputtext = st.text_area("Beschreiben Sie Ihr Vorhaben mit Aufgaben und zeitlichem Ablauf", value=st.session_state.inputtext, height=300)

if st.button("Gantt-Chart erstellen"):
    if st.session_state.inputtext:
        with st.spinner("Erstelle Gantt-Chart..."):
            chart_data = get_chart_data(st.session_state.inputtext)
            st.divider()
            build_chart(chart_data, True)
    else:
        st.warning("Bitte geben Sie zuerst eine Beschreibung Ihres Vorhabens ein.")

