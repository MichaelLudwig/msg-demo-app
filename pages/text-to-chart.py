import streamlit as st
from openai import OpenAI


OpenAI.api_key = st.secrets["OPENAI_API_KEY"]
openAI_model = "gpt-4o-mini"

st.set_page_config(layout="wide")
main_heading=st.title("AI Text-Chart Demo")

#--Sidebar ---------------------------------------------------------------------------------------------------------------------------------------
st.sidebar.title("App-Steuerung")

# Chart Logik ---------------------------------------------------------------------------------------------------------------------------------------
def get_chart_56029(use_container_width: bool):

    source = pd.DataFrame([
        {"task": "A", "start": 1, "end": 3},
        {"task": "B", "start": 3, "end": 8},
        {"task": "C", "start": 8, "end": 10}
    ])

    chart = alt.Chart(source).mark_bar().encode(
        x='start',
        x2='end',
        y='task'
    )

    st.altair_chart(chart, theme="streamlit", use_container_width=True)


get_chart_56029(True)

# Eingabefelder ---------------------------------------------------------------------------------------------------------------------------------------
st.session_state.inputtext = st.text_area(f"Prompt zum generieren des Ganttcharts", value=st.session_state.inputtext, height=200)