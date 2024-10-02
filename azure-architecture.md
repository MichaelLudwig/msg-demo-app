```mermaid
graph TD;
    subgraph VNet1["Virtual Network"]
        Subnet1["Subnet 1: App Service Integration"]
        Subnet2["Subnet 2: Private Endpoint"]
    end

    AppService["Azure App Service"] --> Subnet1
    OpenAI["Azure OpenAI Service"] --> Subnet2

    VNet1 --> PrivateEndpoint["Private Endpoint"]
    PrivateEndpoint --> OpenAI

    AppService --> VNet1
