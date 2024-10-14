import streamlit as st
from openai import OpenAI
import openai
import pandas as pd
import altair as alt
import os
import json
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

if 'ai_api_info' not in st.session_state:
    st.session_state.ai_api_info = ""

#hole dir den ai_key entweder aus der OS Umgebungsvariable oder dem Streamlit Secret Vault
if "AZURE_OPENAI_API_KEY" in os.environ:
    client = openai.AzureOpenAI(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version="2023-03-15-preview",
        azure_endpoint="https://mlu-azure-openai-service-sw.openai.azure.com/"
    )
    openAI_model = "gpt-4o-mini-sw"
    st.session_state.ai_api_info="Azure OpenAI Key - Region Europa"
elif os.getenv('USER') == 'appuser':
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    openAI_model = "gpt-4o-mini"
    st.session_state.ai_api_info="powered by OpenAI"
elif os.getenv('WEBSITE_INSTANCE_ID'):
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    client = openai.AzureOpenAI(
        azure_ad_token_provider=token_provider,
        api_version="2023-03-15-preview",
        azure_endpoint="https://mlu-azure-openai-service-sw.openai.azure.com/"        
    )
    openAI_model = "gpt-4o-mini-sw"
    st.session_state.ai_api_info="Azure OpenAI MI - Region Europa"
else:
    st.session_state.ai_api_info="Kein gültiger API-Schlüssel gefunden."
    raise ValueError("Kein gültiger API-Schlüssel gefunden.")


st.set_page_config(layout="wide")
#debug ob ai_key in streamlit oder Azure gesetzt wurde
#st.write(ai_key)
main_heading=st.title("📊 AI Text-to-Chart Demo")
st.text(st.session_state.ai_api_info)
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
#st.sidebar.title("App-Steuerung")

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
Ergänze fehlende Informationen wie Dauer oder Startzeitpunkt basierend auf den angegebenen Abhängigkeiten und Dauern.
Weise ebenfalls auf mögliche Inkonsistenten im angegebenen Projektplan hin.
Gib das JSON-Array und eine lesbare Rückantwort zurück, die eventuelle Ergänzungen erläutert.
Beispielformat:
JSON:
[
    {{"Aufgabe": "Aufgabe 1", "Start": 0, "Ende": 2, "Abhängigkeiten": []}},
    {{"Aufgabe": "Aufgabe 2", "Start": 1, "Ende": 3, "Abhängigkeiten": [0]}}
]
Antwort:
"Ich habe die Dauer der Aufgabe 'Aufgabe 2' ergänzt, da sie nicht angegeben war."

Hier ist der Plan:

{prompt}
"""}
        ],
        temperature=0.7,
    )
    
    content = response.choices[0].message.content.strip()
    
    try:
        # Versuche, JSON und lesbare Antwort zu extrahieren
        json_start = content.find('[')
        json_end = content.rfind(']') + 1
        if json_start != -1 and json_end != -1:
            json_content = content[json_start:json_end]
            readable_response = content[:json_start].strip() + content[json_end:].strip()
            parsed_data = json.loads(json_content)
            return parsed_data, readable_response
        else:
            raise ValueError("Konnte kein gültiges JSON-Array in der Antwort finden.")
    except json.JSONDecodeError as e:
        st.error(f"JSON Parsing-Fehler: {str(e)}")
        st.error("Rohe API-Antwort:")
        st.code(content, language="json")
    except ValueError as e:
        st.error(str(e))
        st.error("Rohe API-Antwort:")
        st.code(content, language="json")
    except Exception as e:
        st.error(f"Unerwarteter Fehler: {str(e)}")
        st.error("Rohe API-Antwort:")
        st.code(content, language="json")
    
    st.error("Konnte die Daten nicht parsen. Bitte überprüfen Sie die API-Antwort oben.")
    return [], content

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
    
    # Angepasste Palette mit 20 Farben, die sehr helle Töne vermeidet
    angepasste_farben = [
        '#FFB3BA', '#BAFFC9', '#BAE1FF', '#FFD1BA', '#E0BBE4', 
        '#D4F0F0', '#FFC6FF', '#FFD1DC', '#C1FFC1', '#CCE2FF', 
        '#FFD1A1', '#E9D1FF', '#D1FFFD', '#FFD1F5', '#D1FFE3', 
        '#D1E9FF', '#FFDAB9', '#FFE8D1', '#C1D8FF', '#FFCCCB'
    ]
    
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
        color=alt.Color('Aufgabe:N', scale=alt.Scale(range=angepasste_farben), legend=None)
    )

    # Meilensteine als Rauten
    milestones = base.mark_point(shape='diamond', size=100).encode(
        x='Start:Q',
        color=alt.Color('Aufgabe:N', scale=alt.Scale(range=angepasste_farben), legend=None)
    ).transform_filter(alt.datum.Start == alt.datum.Ende)

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
        color='grey',
        strokeWidth=1,
        strokeDash=[2, 2],
        point=alt.OverlayMarkDef(color='grey', shape='triangle-right', size=60)
    ).encode(
        x='von_ende:Q',
        y='von_y:O',
        x2='zu_start:Q',
        y2='zu_y:O'
    )

    chart = (bars + milestones + text).properties(
        width=600,
        height=400
    ).interactive()

    st.altair_chart(chart, theme="streamlit", use_container_width=use_container_width)
    
    # Zeige die sortierten Daten an (optional, für Debugging)
    st.write(df[['Aufgabe', 'Start', 'Ende', 'Abhängigkeiten']])
    #st.write(df)

# Eingabefelder ---------------------------------------------------------------------------------------------------------------------------------------
if 'inputtext' not in st.session_state:
    st.session_state.inputtext = ""

st.session_state.inputtext = st.text_area("Beschreiben Sie Ihr Vorhaben mit Aufgaben und zeitlichem Ablauf", value=st.session_state.inputtext, height=300)

if st.button("Gantt-Chart erstellen"):
    if st.session_state.inputtext:
        with st.spinner("Erstelle Gantt-Chart..."):
            chart_data, readable_response = get_chart_data(st.session_state.inputtext)
            st.divider()
            build_chart(chart_data, True)
            st.text_area("Chatbot Antwort", value=readable_response, height=200)
    else:
        st.warning("Bitte geben Sie zuerst eine Beschreibung Ihres Vorhabens ein.")

