resource "azurerm_resource_group" "streamlit-demo" {
  name     = "streamlit-demo-resource-group"
  location = "Sweden Central"  # oder "Sweden North"
}

resource "azurerm_app_service_plan" "streamlit-demo" {
  name                = "streamlit-demo-appservice-plan"
  location            = azurerm_resource_group.streamlit-demo.location
  resource_group_name = azurerm_resource_group.streamlit-demo.name

  os_type             = "Linux"
  sku_name            = "B1"      # Die Größe des Serviceplans
  sku_tier            = "Basic"    # Tier des Serviceplans
  sku_capacity        = 1           # Anzahl der Instanzen
}

resource "azurerm_app_service" "streamlit-demo" {
  name                = "streamlit-demo-streamlit-app"
  location            = azurerm_resource_group.streamlit-demo.location
  resource_group_name = azurerm_resource_group.streamlit-demo.name
  app_service_plan_id = azurerm_app_service_plan.streamlit-demo.id

  app_settings = {
    "WEBSITE_RUN_FROM_PACKAGE" = "1"
  }
}