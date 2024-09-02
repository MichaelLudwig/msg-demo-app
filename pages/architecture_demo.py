import streamlit as st
from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.network import ELB, Route53
from diagrams.aws.database import RDS
from diagrams.aws.storage import S3

st.title("Komplexere AWS Architektur")

# Diagramm erstellen
with Diagram("Web Service Architecture", show=False, outformat="png", filename="complex_aws_architecture"):
    dns = Route53("DNS")
    lb = ELB("Load Balancer")

    with Cluster("Web Servers"):
        web_servers = [EC2("web1"),
                       EC2("web2"),
                       EC2("web3")]

    db = RDS("User Database")
    storage = S3("User Data")

    dns >> lb >> web_servers
    web_servers >> db
    web_servers >> storage

# Bild in Streamlit anzeigen
st.image("complex_aws_architecture.png", caption="Komplexeres AWS Architekturdiagramm")
