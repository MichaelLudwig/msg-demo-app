import streamlit as st
import streamlit_app
import pages.architecture_demo as architecture_demo
import pages.azure_openai_api_test as azure_openai_api_test
import pages.watermark_ai as watermark_ai

# Definiere die Seiten
PAGES = {
    "Concept Designer 📝": streamlit_app,
    "Architektur Schaubilder ☁️": architecture_demo,
    "Wasserzeichen ☁️": watermark_ai,
}

st.set_page_config(page_title="Demo Apps", page_icon=":iphone:", layout="wide")

# Seiten-Navigation in der Sidebar
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Gehe zu", list(PAGES.keys()))


main_heading=st.title("Demo Apps")

st.divider()

st.page_link("streamlit_app.py", label="Home", icon="🏠")

st.divider()

st.page_link("pages/architecture_demo.py", label="Architecture Demo", icon="☁️")
st.image("architecture.png", width=300)

st.divider()

st.page_link("pages/charts_demo.py", label="Chart Demo", icon="📊")
st.image("chart.png", width=300)

st.divider()

st.page_link("pages/report_demo.py", label="Report Demo", icon="📝")
st.image("report.png", width=300)

st.divider()

st.page_link("pages/text-to-chart.py", label="AI Text-Chart Demo", icon="📊")
st.image("gantt.png", width=300)

st.divider()

st.page_link("pages/azure-openai-api-test.py", label="Azure OpenAI Chat Demo", icon="🤖")
st.image("AOAI.png", width=300)

st.divider()

st.page_link("pages/watermark-ai.py", label="Wasserzeichen AI", icon="☁️")
#st.image("AOAI.png", width=300)

#st.image("gantt.png", width=300)



