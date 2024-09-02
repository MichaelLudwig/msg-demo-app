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
st.page_link("pages/charts_demo.py", label="Chart Demo", icon="📊")
st.page_link("pages/report_demo.py", label="Report Demo", icon="📝")

