import streamlit as st
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

st.title("AWS Architekturdiagramm")

# Diagramm erstellen
with Diagram("Simple AWS Web Service", show=False, outformat="png", filename="aws_architecture"):
    elb = ELB("Load Balancer")
    ec2 = EC2("Web Server")
    rds = RDS("Database")

    elb >> ec2 >> rds

# Bild in Streamlit anzeigen
st.image("aws_architecture.png", caption="Einfaches AWS Web Service Diagramm")
