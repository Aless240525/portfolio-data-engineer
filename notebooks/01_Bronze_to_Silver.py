# Databricks notebook source
from pyspark.sql.functions import col, to_date, to_timestamp, current_timestamp
from delta.tables import *

# 1. Path Configuration
storage_account = "datalakehousealessdev"
bronze_base = f"abfss://bronze@{storage_account}.dfs.core.windows.net"
silver_base = f"abfss://silver@{storage_account}.dfs.core.windows.net"

# Specific file paths 
path_txn_bronze = f"{bronze_base}/test_1/transacciones_skewed.csv"
path_cust_bronze = f"{bronze_base}/test_1/maestro_clientes.json"

# Destination Paths (Delta Tables)
path_txn_silver = f"{silver_base}/transacciones"
path_cust_silver = f"{silver_base}/clientes"

# COMMAND ----------

# --- 2. CUSTOMERS (JSON)  ---
print("Processing Customers...")

# Read JSON 
df_cust_raw = spark.read.format("json") \
    .option("inferSchema", "true") \
    .load(path_cust_bronze)

# Silver Transformation
df_cust_silver = df_cust_raw.select(
    col("customer_id").cast("string"),
    col("name"),
    col("email"),
    col("country"),
    col("segment"),
    current_timestamp().alias("ingestion_ts")
)

# Upsert (Merge) for Customers
if DeltaTable.isDeltaTable(spark, path_cust_silver):
    delta_cust = DeltaTable.forPath(spark, path_cust_silver)
    delta_cust.alias("tgt").merge(
        df_cust_silver.alias("src"),
        "tgt.customer_id = src.customer_id"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
else:
    df_cust_silver.write.format("delta").mode("overwrite").save(path_cust_silver)

# --- 3. TRANSACTIONS (CSV) ---
print("Processing Transactions...")
df_txn_raw = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load(path_txn_bronze)

# Silver Transformation
df_txn_silver = df_txn_raw.select(
    col("transaction_id").cast("string"),
    col("customer_id").cast("string"),
    col("amount").cast("double"),
    to_timestamp(col("transaction_date")).alias("transaction_date"),
    col("store_id").cast("integer"),
    current_timestamp().alias("ingestion_ts")
)

# Upsert (Merge) for Transactions
if DeltaTable.isDeltaTable(spark, path_txn_silver):
    delta_txn = DeltaTable.forPath(spark, path_txn_silver)
    delta_txn.alias("tgt").merge(
        df_txn_silver.alias("src"),
        "tgt.transaction_id = src.transaction_id"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
else:
    df_txn_silver.write.format("delta").mode("overwrite").save(path_txn_silver)

print("✅ Load to Silver completed successfully!")