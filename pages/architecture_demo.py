import streamlit as st
import graphviz

st.title("AWS Komponenten")

# Ein einfaches Diagramm erstellen
dot = """
digraph G {
    EC2 [label="EC2 Instance", shape=box]
    S3 [label="S3 Bucket", shape=cylinder]
    EC2 -> S3
}
"""

st.graphviz_chart(dot)



st.title("AWS Architektur")

# Ein komplexes Diagramm erstellen
dot = """
digraph G {
    

    subgraph cluster_0 {
        style=filled;
        color=lightgrey;
        node [style=filled,color=white];
        label = "Production Environment";
        
        ELB_Prod [label="Load Balancer", shape=ellipse];
        WebServer1_Prod [label="Web Server 1", shape=box];
        WebServer2_Prod [label="Web Server 2", shape=box];
        AppServer1_Prod [label="App Server 1", shape=box];
        AppServer2_Prod [label="App Server 2", shape=box];
        RDS_Prod [label="RDS Database", shape=cylinder];
        S3_Prod [label="S3 Storage", shape=folder];
        
        ELB_Prod -> WebServer1_Prod;
        ELB_Prod -> WebServer2_Prod;
        WebServer1_Prod -> AppServer1_Prod;
        WebServer2_Prod -> AppServer2_Prod;
        AppServer1_Prod -> RDS_Prod;
        AppServer2_Prod -> RDS_Prod;
        RDS_Prod -> S3_Prod;
    }

    subgraph cluster_1 {
        style=filled;
        color=lightblue;
        node [style=filled,color=white];
        label = "Development Environment";
        
        WebServer1_Dev [label="Web Server 1", shape=box];
        AppServer1_Dev [label="App Server 1", shape=box];
        RDS_Dev [label="RDS Database", shape=cylinder];
        S3_Dev [label="S3 Storage", shape=folder];
        
        
        WebServer1_Dev -> AppServer1_Dev;
        AppServer1_Dev -> RDS_Dev;
        RDS_Dev -> S3_Dev;
    }

    Route53 [label="Route 53 DNS", shape=hexagon];

    Route53 -> ELB_Prod;
    Route53 -> WebServer1_Dev;
}
"""

# Diagramm in Streamlit anzeigen
st.graphviz_chart(dot)


from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import VPC, PrivateSubnet, PublicSubnet, NATGateway
from diagrams.aws.compute import EC2
from diagrams.aws.storage import S3
from diagrams.aws.database import Dynamodb
from diagrams.aws.integration import SQS
from diagrams.aws.security import IAM
from diagrams.aws.management import SystemsManagerParameterStore

with Diagram("AWS Global Region", show=False, direction="TB"):
    s3_source = S3("S3 (Source Bucket)")
    dynamodb = Dynamodb("Amazon DynamoDB")
    ec2_job_sender = EC2("Amazon EC2 (Job Sender)")
    sqs = SQS("Amazon SQS")
    param_store = SystemsManagerParameterStore("Parameter Store")
    iam_roles = IAM("AWS IAM Roles")
    
    with Cluster("VPC"):
        with Cluster("Availability Zone 1"):
            nat_gateway_az1 = NATGateway("NAT Gateway")
            worker_cluster_az1 = EC2("Worker Cluster Instance")
            
        with Cluster("Availability Zone 2"):
            nat_gateway_az2 = NATGateway("NAT Gateway")
            worker_cluster_az2 = EC2("Worker Cluster Instance")

        auto_scaling_group = [worker_cluster_az1, worker_cluster_az2]
    
    s3_destination = S3("S3 (Destination Bucket)")
    
    # Connections
    dynamodb >> s3_source >> ec2_job_sender
    ec2_job_sender >> sqs
    sqs >> auto_scaling_group
    auto_scaling_group >> nat_gateway_az1 >> s3_destination
    auto_scaling_group >> nat_gateway_az2 >> s3_destination

