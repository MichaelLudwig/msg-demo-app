import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO
import graphviz
import altair as alt
from vega_datasets import data

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

# Funktion zum Erstellen eines Donut-Charts
def create_donut_chart(percentage):
    if percentage <= 25:
        color = 'red'
    elif percentage <= 50:
        color = 'orange'
    elif percentage <= 75:
        color = '#1f77b4'
    else:
        color = 'green'
    
    fig, ax = plt.subplots()
    ax.pie([percentage, 100 - percentage], 
           labels=['', ''], 
           startangle=90, 
           colors=[color, '#d3d3d3'], 
           wedgeprops={'width': 0.3})
    
    # Prozentsatz in der Mitte des Donuts anzeigen
    ax.text(0, 0, f"{percentage}%", ha='center', va='center', fontsize=20, color=color)
    
    # Chart als Bild in einem BytesIO-Objekt speichern
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)
    return buf

# Streamlit App
st.title("Tabelle mit Fertigstellungsgrad")

# Dummy-Daten
data = [
    {"text": "Lorem ipsum dolor sit amet, consectetur adipiscing. Sed do eiusmod tempor incididunt ut labore et dolore.", "percentage": 15},
]

# Tabelle anzeigen und bearbeiten
for row in data:
    col1, col2 = st.columns([1, 1])

    # Text in der ersten Spalte anzeigen
    col1.write(row["text"])

    
    # Slider zur Anpassung des Prozentsatzes
    row["percentage"] = col1.slider(f"Prozentwert für diesen Eintrag:", min_value=0, max_value=100, value=row["percentage"], step=5)
    
    # Schließen des farbigen Containers
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Donut-Chart in der zweiten Spalte anzeigen
    donut_chart = create_donut_chart(row["percentage"])
    col2.image(donut_chart, use_column_width=True)

