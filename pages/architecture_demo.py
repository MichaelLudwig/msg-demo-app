import streamlit as st
import graphviz

st.title("AWS Architektur")

# Ein einfaches Diagramm erstellen
dot = """
digraph G {
    EC2 [label="EC2 Instance", shape=box]
    S3 [label="S3 Bucket", shape=cylinder]
    EC2 -> S3
}
"""

st.graphviz_chart(dot)

st.graphviz_chart('''
    digraph {
        run -> intr
        intr -> runbl
        runbl -> run
        run -> kernel
        kernel -> zombie
        kernel -> sleep
        
    }
''')
