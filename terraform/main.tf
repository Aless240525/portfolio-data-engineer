# 1. Resource Group
resource "azurerm_resource_group" "rg" {
  name     = "rg-${var.project_name}-${var.environment}"
  location = var.location
}

# 2. Azure Data Lake Storage Gen2 (Storage + HNS Enabled)
resource "azurerm_storage_account" "adls" {
  name                     = "st${var.project_name}${var.environment}001"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  is_hns_enabled           = true # Essential for Data Lake Gen2 / Medallion Architecture
}

# Containers for Medallion Architecture
resource "azurerm_storage_data_lake_gen2_filesystem" "bronze" {
  name               = "bronze"
  storage_account_id = azurerm_storage_account.adls.id
}

resource "azurerm_storage_data_lake_gen2_filesystem" "silver" {
  name               = "silver"
  storage_account_id = azurerm_storage_account.adls.id
}

resource "azurerm_storage_data_lake_gen2_filesystem" "gold" {
  name               = "gold"
  storage_account_id = azurerm_storage_account.adls.id
}

# 3. Azure Data Factory (Orchestration)
resource "azurerm_data_factory" "adf" {
  name                = "adf-${var.project_name}-${var.environment}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

# 4. Azure Databricks Workspace (Processing)
resource "azurerm_databricks_workspace" "dbw" {
  name                = "dbw-${var.project_name}-${var.environment}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "premium"
}

# 5. Azure Key Vault (Security)
resource "azurerm_key_vault" "kv" {
  name                = "kv-${var.project_name}-${var.environment}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"
}

# 6. Azure Synapse Analytics (Serving / Data Warehouse)
resource "azurerm_synapse_workspace" "synapse" {
  name                                 = "syn-${var.project_name}-${var.environment}"
  resource_group_name                  = azurerm_resource_group.rg.name
  location                             = azurerm_resource_group.rg.location
  storage_data_lake_gen2_filesystem_id = azurerm_storage_data_lake_gen2_filesystem.gold.id
  sql_administrator_login              = "sqladminuser"
  sql_administrator_login_password     = "Lakehouse12345!" 
}