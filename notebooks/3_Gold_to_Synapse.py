# Databricks notebook source
# =========================================================================
# FINAL SYNAPSE LOAD SCRIPT 
# =========================================================================

# -------------------------------------------------------------------------
# 1. RETRIEVE CREDENTIALS FROM KEY VAULT
# -------------------------------------------------------------------------

secret_scope = "key-vault-secret-scope"

try:
    # A. Retrieve Key1 from Storage
    storage_key = dbutils.secrets.get(scope=secret_scope, key="datalake-access-key1")
    
    # B. Retrieve Service Principal credentials
    sp_client_id = dbutils.secrets.get(scope=secret_scope, key="sp-client-id")
    sp_secret    = dbutils.secrets.get(scope=secret_scope, key="sp-secret-value")
    
    print("✅ All credentials successfully retrieved from Key Vault.")

except Exception as e:
    print("❌ Error: Could not retrieve a secret.")
    print("Verify that the name 'datalake-access-key1' is correct in Azure Key Vault.")
    raise e

# -------------------------------------------------------------------------
# 2. ENVIRONMENT CONFIGURATION
# -------------------------------------------------------------------------
storage_account      = "datalakehousealessdev"
synapse_service_name = "synapse-proyecto-alessandro"
synapse_database     = "sqlpool01"
container_gold       = "gold"

# 3. INJECT KEY INTO SPARK CONFIGURATION
spark.conf.set(
    f"fs.azure.account.key.{storage_account}.dfs.core.windows.net", 
    storage_key
)

# 4. PREPARE SYNAPSE CONNECTION
jdbc_url = f"jdbc:sqlserver://{synapse_service_name}.sql.azuresynapse.net:1433;database={synapse_database};authentication=ActiveDirectoryServicePrincipal"

# Temporary Staging Folder
temp_dir = f"abfss://{container_gold}@{storage_account}.dfs.core.windows.net/synapse_staging_temp"

# -------------------------------------------------------------------------
# 5. WRITE FUNCTION
# -------------------------------------------------------------------------
def write_to_synapse(df, table_name):
    print(f"⏳ Creating/Loading table '{table_name}' in Synapse...")
    
    (df.write
    .format("com.databricks.spark.sqldw")
    .option("url", jdbc_url)
    .option("dbTable", table_name)
    .option("tempDir", temp_dir)
    .option("forwardSparkAzureStorageCredentials", "true")
    # Pass the secure credentials retrieved above
    .option("user", sp_client_id)
    .option("password", sp_secret)
    .mode("overwrite")
    .save()
    )
    print(f"✅ Table '{table_name}' ready.")

# -------------------------------------------------------------------------
# 6. PROCESS EXECUTION
# -------------------------------------------------------------------------
base_path   = f"abfss://{container_gold}@{storage_account}.dfs.core.windows.net"

path_sales = f"{base_path}/ventas_enriquecidas"
path_kpi   = f"{base_path}/kpi_ventas_pais"

print("📖 Reading Delta data...")
df_sales = spark.read.format("delta").load(path_sales)
df_kpi   = spark.read.format("delta").load(path_kpi)

# Write to Synapse
write_to_synapse(df_sales, "Gold_Sales_Detail")  # Renamed for English consistency
write_to_synapse(df_kpi,   "Gold_KPI_Sales")

print("\n🚀 PROCESS FINISHED SUCCESSFULLY!")