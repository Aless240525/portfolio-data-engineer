# 🚀 Modern Data Lakehouse Pipeline: Azure End-to-End Solution

![Azure](https://img.shields.io/badge/azure-%230072C6.svg?style=for-the-badge&logo=microsoftazure&logoColor=white)
![Databricks](https://img.shields.io/badge/Databricks-FF3621?style=for-the-badge&logo=databricks&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Power Bi](https://img.shields.io/badge/power_bi-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)

## 📋 Descripción del Proyecto
Este proyecto implementa una solución completa de Ingeniería de Datos tipo **Data Lakehouse** en Microsoft Azure. El objetivo principal es procesar grandes volúmenes de datos transaccionales, resolver problemas de rendimiento (Data Skew) y servir información de valor para el negocio con baja latencia.

La arquitectura sigue las mejores prácticas de la industria ("Medallion Architecture"), garantizando la calidad, seguridad y gobernanza de los datos desde la ingesta hasta la visualización.

---

## 🏗️ Arquitectura de la Solución

<img width="720" height="393" alt="image" src="https://github.com/user-attachments/assets/b379f71e-2b71-4e53-93a9-773d8753df9e" />

El flujo de datos se divide en las siguientes etapas:

1. **Ingesta y Orquestación:** **Azure Data Factory (ADF)** orquesta la copia de datos crudos (CSV/JSON) desde fuentes externas hacia la capa *Bronze* del Data Lake.
2. **Almacenamiento:** **ADLS Gen2** estructurado en capas (Bronze, Silver, Gold).
3. **Procesamiento y Transformación:** - Uso de **Azure Databricks (PySpark)** y **Delta Lake**.
   - **Silver Layer:** Limpieza de datos y Schema Enforcement.
   - **Gold Layer:** Agregaciones de negocio complejas y optimización de JOINS.
4. **Servicio (Serving):** Carga de datos refinados a **Azure Synapse Analytics (Dedicated SQL Pool)**.
5. **Visualización:** Conexión vía DirectQuery desde **Power BI**.
6. **Seguridad:** Gestión de credenciales "Zero-Trust" utilizando **Azure Key Vault**.

---

## 💡 Desafío Técnico: Optimización de Data Skew
Uno de los retos críticos de este pipeline fue el manejo de **Data Skew** (sesgo de datos) durante los Joins de grandes volúmenes entre la tabla de Transacciones y Clientes.

**Solución Implementada:**
- Detección de particiones desbalanceadas en Databricks.
- Implementación de estrategias de **Salting** y **Broadcast Joins** en los Notebooks de la capa Gold.
- **Resultado:** Reducción significativa en el tiempo de ejecución del Job y eliminación de errores por `OOM (Out Of Memory)`.

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología | Uso Principal |
|------------|------------|---------------|
| **Cloud Provider** | Microsoft Azure | Infraestructura base |
| **Compute** | Azure Databricks | Procesamiento ETL con PySpark |
| **Storage** | ADLS Gen2 + Delta Lake | Almacenamiento optimizado y ACID |
| **Orchestrator** | Azure Data Factory | Control de flujo y triggers |
| **Warehouse** | Azure Synapse Analytics | Pool SQL Dedicado para consultas rápidas |
| **Security** | Azure Key Vault | Gestión de secretos y Service Principals |
| **BI** | Power BI | Dashboards y reporte final |

---

## 📂 Estructura del Repositorio
```bash
├── data/                  # Scripts de generación de data dummy (si aplica)
├── notebooks/             # Código PySpark (Databricks)
│   ├── 1_bronze_to_silver.py
│   ├── 2_silver_to_gold_skew_optimization.py  <-- Lógica Anti-Skew
│   └── 3_gold_to_synapse.py
├── pipelines/             # Templates JSON de Azure Data Factory
├── img/                   # Diagramas y capturas
└── README.md              # Documentación
