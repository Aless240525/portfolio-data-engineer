# Databricks notebook source
from pyspark.sql.functions import col, broadcast, sum, avg, count, desc
from delta.tables import *
from pyspark.sql.functions import current_timestamp

# --- 1. CONFIGURATION ---
storage_account = "datalakehousealessdev"
silver_base = f"abfss://silver@{storage_account}.dfs.core.windows.net"
gold_base = f"abfss://gold@{storage_account}.dfs.core.windows.net"

# Read Silver tables 
df_txn = spark.read.format("delta").load(f"{silver_base}/transacciones")
df_cust = spark.read.format("delta").load(f"{silver_base}/clientes")

print(f"Transactions: {df_txn.count()} | Customers: {df_cust.count()}")

# COMMAND ----------

# --- 2. SKEW ANALYSIS (To visualize the problem) ---
# Count how many transactions each customer has
skew_analysis = df_txn.groupBy("customer_id").count().orderBy(col("count").desc())

print("Top 5 Customers with the most transactions (Possible Skew):")
display(skew_analysis.limit(5))

# COMMAND ----------

# --- 3. GOLD TRANSFORMATION ---

# Apply BROADCAST JOIN to eliminate the impact of Skew
df_gold_joined = df_txn.join(
    broadcast(df_cust), 
    df_txn.customer_id == df_cust.customer_id,
    "inner"
).drop(df_cust.customer_id) \
 .drop("ingestion_ts") \
 .withColumn("ingestion_gold_ts", current_timestamp())

# Create a summary table by Country and Segment
df_gold_kpi = df_gold_joined.groupBy("country", "segment").agg(
    sum("amount").alias("total_sales"),
    avg("amount").alias("avg_ticket"),
    count("transaction_id").alias("txn_count")
).orderBy(col("total_sales").desc())

display(df_gold_kpi)

# COMMAND ----------

# --- 4. WRITING TO GOLD LAYER ---
path_gold_enriched = f"{gold_base}/ventas_enriquecidas"
path_gold_kpi = f"{gold_base}/kpi_ventas_pais"

# 4.1 Save Detailed Table (Transactions with attached customer data)
df_gold_joined.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .save(path_gold_enriched)

# 4.2 Save Aggregated Table (KPIs ready for the Dashboard)
df_gold_kpi.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .save(path_gold_kpi)

print("✅ Gold Layer generated successfully.")

# COMMAND ----------

# --- 5. TABLE REGISTRATION (Legacy Mode / Hive Metastore) ---

# 1. Create the Database (Schema) directly
spark.sql("CREATE DATABASE IF NOT EXISTS gold_db")

# ---------------------------------------------------------
# TABLE 1: The detailed one
# ---------------------------------------------------------
# Register the table inside the 'gold_db' database
spark.sql(f"""
    CREATE TABLE IF NOT EXISTS gold_db.ventas_enriquecidas
    USING DELTA
    LOCATION '{path_gold_enriched}'
""")

# ---------------------------------------------------------
# TABLE 2: The aggregated one (KPIs)
# ---------------------------------------------------------
spark.sql(f"""
    CREATE TABLE IF NOT EXISTS gold_db.kpi_ventas_pais
    USING DELTA
    LOCATION '{path_gold_kpi}'
""")

print("✅ Tables successfully registered in the 'gold_db' database.")