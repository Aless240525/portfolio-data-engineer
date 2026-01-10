# 🚀 Modern Data Lakehouse Pipeline: Azure End-to-End Solution

![Azure](https://img.shields.io/badge/azure-%230072C6.svg?style=for-the-badge&logo=microsoftazure&logoColor=white)
![Databricks](https://img.shields.io/badge/Databricks-FF3621?style=for-the-badge&logo=databricks&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Power Bi](https://img.shields.io/badge/power_bi-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)

## 📋 Project Overview
This project implements a complete **Data Lakehouse** solution on Microsoft Azure. The main objective is to build a robust pipeline that processes high volumes of transactional data, resolves critical performance issues (Data Skew), and delivers consolidated business insights with low latency.

The architecture follows industry best practices (**Medallion Architecture**), ensuring data quality, security, and governance from ingestion to visualization.

## 🏗️ Solution Architecture

<img width="1024" height="565" alt="Architecture Diagram" src="https://github.com/user-attachments/assets/8b3ba211-80a6-4d75-bf26-c8478d270269" />

The data flow is divided into the following stages:

1. **Ingestion & Orchestration:** **Azure Data Factory (ADF)** orchestrates the copy of raw data (CSV/JSON) from external sources to the *Bronze* layer of the Data Lake.
2. **Storage:** **ADLS Gen2** structured in layers (Bronze, Silver, Gold).
3. **Processing & Transformation:** Powered by **Azure Databricks (PySpark)** and **Delta Lake**.
   - **Silver Layer:** Data cleaning, deduplication, and Schema Enforcement.
   - **Gold Layer:** Complex business aggregations and **JOIN optimization**.
4. **Serving:** Refined data is loaded into **Azure Synapse Analytics (Dedicated SQL Pool)**.
5. **Visualization:** Connected via DirectQuery using **Power BI**.
6. **Security:** "Zero-Trust" credential management using **Azure Key Vault**.

---

## 💡 Technical Challenge: Handling Data Skew
A critical challenge in this pipeline was managing **Data Skew** during the High-Volume Joins between Transaction and Customer tables.

**Implemented Solution:**
- Detection of unbalanced partitions in Databricks.
- Implementation of **Salting** strategies and **Broadcast Joins** within the Gold layer notebooks.
- **Result:** Significant reduction in Job execution time and elimination of `OOM (Out Of Memory)` errors.

---

## 🛠️ Tech Stack

| Component | Technology | Primary Usage |
|-----------|------------|---------------|
| **Cloud Provider** | Microsoft Azure | Infrastructure backbone |
| **Compute** | Azure Databricks | ETL Processing with PySpark |
| **Storage** | ADLS Gen2 + Delta Lake | Optimized ACID Storage |
| **Orchestrator** | Azure Data Factory | Control flow and triggers |
| **Warehouse** | Azure Synapse Analytics | Dedicated SQL Pool for fast querying |
| **Security** | Azure Key Vault | Secrets and Service Principal management |
| **BI** | Power BI | Dashboards and Reporting |

---

## 📊 Data Visualization (Power BI)
The pipeline concludes by making data available in Azure Synapse Analytics, which is consumed via **DirectQuery** to ensure up-to-date information.

### 🔴 [Live Demo: Interact with the Dashboard Here](https://app.powerbi.com/view?r=eyJrIjoiOWVmNmE4MTktYTJjNS00MWVkLThkMDgtMjYwMjAxODU3YzQ1IiwidCI6IjExY2Y1N2U2LTIyMWQtNDU2My1hNDc1LTk2ODk4YTJjOTE2OSIsImMiOjR9)

<img width="3301" height="1829" alt="image" src="https://github.com/user-attachments/assets/f98dc748-2df6-426a-96f0-06ef6a3f9971" />

*(Dashboard displaying Sales KPIs and distribution analysis by country)*

---

## 📂 Repository Structure
```bash
├── datasets/                  # JSON definitions for ADF Datasets
│   ├── GETCSVFILE.json
│   ├── GETJSONFILE.json
│   ├── target_CSV.json
│   ├── target_json.json
├── linkservices/              # Connection configurations (Linked Services)
│   ├── AzureDataLakeStorage1.json
│   ├── AzureDatabricks1.json
│   └── LS_KeyVault.json
├── notebooks/                 # PySpark Code (Databricks)
│   ├── 01_Bronze_to_Silver.py
│   ├── 02_Silver_to_Gold.py   # <-- Includes Anti-Skew Logic (Salting/Broadcast)
│   └── 03_Gold_to_Synapse.py
├── pipelines/                 # Azure Data Factory Pipelines
│   └── pipeline_adf.json
└── README.md                  # Project Documentation
