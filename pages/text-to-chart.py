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
Wandle den folgenden Projektplan in ein JSON-Array um, das für ein Gantt-Chart geeignet ist. 
Jedes Objekt sollte 'task', 'start' und 'end' enthalten. 
'start' und 'end' sollten numerische Werte sein, die die Tage seit Projektbeginn darstellen. 
Gib NUR das JSON-Array zurück, ohne zusätzlichen Text.
Beispielformat:
[
    {{"task": "Aufgabe 1", "start": 0, "end": 30}},
    {{"task": "Aufgabe 2", "start": 15, "end": 45}}
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
    chart = alt.Chart(source).mark_bar().encode(
        x='start',
        x2='end',
        y='task'
    )
    st.altair_chart(chart, theme="streamlit", use_container_width=use_container_width)

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

