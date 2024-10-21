import streamlit as st




st.set_page_config(page_title="Demo Apps", page_icon=":iphone:")



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

st.page_link("pages/azure-openai-api-test.py", label="Azure OpenAI Chat Demo", icon="🤖")
st.image("AOAI.png", width=300)

st.divider()

st.page_link("pages/watermark-ai.py", label="Wasserzeichen AI", icon="☁️")
#st.image("AOAI.png", width=300)

#st.image("gantt.png", width=300)



