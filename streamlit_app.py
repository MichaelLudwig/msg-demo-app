import streamlit as st
import graphviz

st.page_link("streamlit_app.py", label="Home", icon="🏠")

st.page_link("pages/architecture_demo.py", label="Architecture Demo", icon="☁️")
# Ein einfaches Diagramm erstellen
dot = """
digraph G {
    EC2 [label="EC2 Instance", shape=box]
    S3 [label="S3 Bucket", shape=cylinder]
    EC2 -> S3
}
"""
st.graphviz_chart(dot)


st.page_link("pages/charts_demo.py", label="Chart Demo", icon="📊")
def get_chart_98552(use_container_width: bool):

    source = data.stocks()

    chart = alt.Chart(source).mark_line(point=True).encode(
        x='date:T',
        y='price:Q',
        color='symbol:N'
    )

    st.altair_chart(chart, theme="streamlit", use_container_width=True)


get_chart_98552(True)


st.page_link("pages/report_demo.py", label="Report Demo", icon="📝")

