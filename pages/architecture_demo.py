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



st.title("AWS Architektur: Webservers, Load Balancer, App Tier, und Datenbanken")

# Diagramm erstellen
dot = """
digraph G {
    rankdir=TB;

    subgraph cluster_region {
        label = "Region";
        color = black;
        style = dashed;

        subgraph cluster_autoscaling {
            label = "Auto Scaling Group";
            color = black;
            style = dashed;

            WebServer1 [label="Web Server", shape=box, style=filled, color=orange];
            WebServer2 [label="Web Server", shape=box, style=filled, color=orange];
        }

        subgraph cluster_app_tier {
            label = "App Tier";
            color = black;
            style = dashed;

            AppServer1 [label="App Server", shape=box, style=filled, color=lightblue];
            AppServer2 [label="App Server", shape=box, style=filled, color=lightblue];
        }

        subgraph cluster_db {
            label = "AZ-1";
            color = orange;
            style = dashed;
            DynamoDB [label="Amazon DynamoDB", shape=cylinder, style=filled, color=grey];
        }

        subgraph cluster_db2 {
            label = "AZ-2";
            color = orange;
            style = dashed;
            RDS [label="Amazon RDS", shape=cylinder, style=filled, color=grey];
        }

        S3 [label="Amazon S3 Bucket", shape=folder, style=filled, color=green];
        LoadBalancer [label="Elastic Load Balancer", shape=ellipse, style=filled, color=grey];
        Route53 [label="Amazon Route 53 Hosted Zone", shape=triangle, style=filled, color=black];
        CloudFront [label="Amazon CloudFront", shape=hexagon, style=filled, color=lightblue];

        Route53 -> LoadBalancer;
        LoadBalancer -> WebServer1;
        LoadBalancer -> WebServer2;

        WebServer1 -> AppServer1;
        WebServer2 -> AppServer2;

        AppServer1 -> DynamoDB;
        AppServer2 -> RDS;

        WebServer1 -> S3;
        CloudFront -> S3;
    }

    S3 -> CloudFront;
}
"""

# Diagramm in Streamlit anzeigen
st.graphviz_chart(dot)
