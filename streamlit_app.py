import streamlit as st


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


