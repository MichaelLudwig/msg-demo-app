provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "streamlit-demo" {
  name     = "streamlit-demo-resource-group"
  location = "Sweden Central"  # oder "Sweden North"
}

resource "azurerm_service_plan" "streamlit-demo" {
  name                = "streamlit-demo-appservice-plan"
  location            = azurerm_resource_group.streamlit-demo.location
  resource_group_name = azurerm_resource_group.streamlit-demo.name

  sku {
    tier = "Shared"  
    size = "Sd1"    
  }
}

resource "azurerm_app_service" "streamlit-demo" {
  name                = "streamlit-demo-streamlit-app"
  location            = azurerm_resource_group.streamlit-demo.location
  resource_group_name = azurerm_resource_group.streamlit-demo.name
  app_service_plan_id = azurerm_service_plan.streamlit-demo.id

  app_settings = {
    "WEBSITE_RUN_FROM_PACKAGE" = "1"
  }
}