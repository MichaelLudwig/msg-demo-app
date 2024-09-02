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



from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.storage import S3

# Diagramm erstellen und als Bild speichern
with Diagram("AWS Architektur", show=False):
    ec2 = EC2("EC2 Instance")
    s3 = S3("S3 Bucket")
    ec2 >> s3

# Bild in Streamlit anzeigen
st.image("aws_architektur_diagram.png", caption="Meine AWS Architektur")
