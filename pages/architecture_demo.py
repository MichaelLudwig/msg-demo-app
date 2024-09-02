import streamlit as st
import graphviz

st.title("Architektur")

# Ein einfaches Diagramm erstellen
dot = """
digraph G {
    EC2 [label="EC2 Instance", shape=box]
    S3 [label="S3 Bucket", shape=cylinder]
    EC2 -> S3
}
"""

st.graphviz_chart(dot)

st.title("AWS Architektur: EC2-Instanzen, VPC-Endpunkt, und S3")

# Diagramm erstellen
dot = """
digraph G {
    rankdir=LR;

    subgraph cluster_vpc {
        label = "VPC";
        color = green;

        subgraph cluster_subnet1 {
            label = "Private subnet";
            color = lightblue;
            EC2_1 [label="EC2 Instance", shape=box, style=filled, color=orange];
        }

        subgraph cluster_subnet2 {
            label = "Private subnet";
            color = lightblue;
            EC2_2 [label="EC2 Instance", shape=box, style=filled, color=orange];
        }
    }

}
"""

# Diagramm in Streamlit anzeigen
st.graphviz_chart(dot)


st.title("Komplexe AWS Architektur")

# Ein komplexes Diagramm erstellen
dot = """
digraph G {
    rankdir=LR;

    subgraph cluster_0 {
        style=filled;
        color=lightgrey;
        node [style=filled,color=white];
        label = "Production Environment";
        
        ELB_Prod [label="Load Balancer", shape=ellipse];
        WebServer1_Prod [label="Web Server 1", shape=box];
        WebServer2_Prod [label="Web Server 2", shape=box];
        RDS_Prod [label="RDS Database", shape=cylinder];
        S3_Prod [label="S3 Storage", shape=folder];
        
        ELB_Prod -> WebServer1_Prod;
        ELB_Prod -> WebServer2_Prod;
        WebServer1_Prod -> RDS_Prod;
        WebServer2_Prod -> RDS_Prod;
        RDS_Prod -> S3_Prod;
    }

    subgraph cluster_1 {
        style=filled;
        color=lightblue;
        node [style=filled,color=white];
        label = "Development Environment";
        
        ELB_Dev [label="Load Balancer", shape=ellipse];
        WebServer1_Dev [label="Web Server 1", shape=box];
        WebServer2_Dev [label="Web Server 2", shape=box];
        RDS_Dev [label="RDS Database", shape=cylinder];
        S3_Dev [label="S3 Storage", shape=folder];
        
        ELB_Dev -> WebServer1_Dev;
        ELB_Dev -> WebServer2_Dev;
        WebServer1_Dev -> RDS_Dev;
        WebServer2_Dev -> RDS_Dev;
        RDS_Dev -> S3_Dev;
    }

    Route53 [label="Route 53 DNS", shape=hexagon];

    Route53 -> ELB_Prod;
    Route53 -> ELB_Dev;
}
"""

# Diagramm in Streamlit anzeigen
st.graphviz_chart(dot)
