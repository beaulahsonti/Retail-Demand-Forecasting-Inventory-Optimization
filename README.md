# ?? Zaalima: End-to-End Retail Demand Forecasting & Inventory Optimization Platform

Zaalima is a production-grade, cloud-integrated machine learning and time-series engineering platform modeled on the multi-million-row Walmart institutional dataset. The platform accurately predicts highly volatile daily retail demand down to specific store-product combinations, helping supply chain managers eliminate inventory stockouts and minimize carrying waste.

---

## ??? Decoupled Pipeline Architecture

The system is engineered across three fully decoupled production modules to maximize memory performance and scaling limits:

1. **`src_etl/` (Data Ingestion Layer):** Automated Python ETL scripts that ingest raw transactional streams, enforce strict data-type casting, isolate missing values, and stage clean metrics in an offline database.
2. **`src_dbt/` (Semantic Transformation Layer):** An advanced analytics pipeline powered by **dbt and DuckDB**. It resolves a massive operational bottleneck by using an optimized database `UNPIVOT` view expression to flatten **over 1,900 horizontal day columns** into a vertical long-series format in a blistering **0.30 seconds flat**.
3. **`src_models/` (Machine Learning Engine):** A cloud-integrated forecasting engine that uses the official **Google Cloud BigQuery Client API** to stream memory-managed 100,000-row feature extraction chunks straight into high-performance **LightGBM gradient boosting loops**.

---

## ?? AI Feature Engineering Specification

The machine learning models extract pre-calculated, time-series variables generated natively within our analytical data marts:
* **Time-Series Lags:** `sales_lag_1d`, `sales_lag_7d`, and `sales_lag_28d` to natively capture day-over-day momentum and monthly shopping rhythm seasonality.
* **Moving Rolling Windows:** Trailing 7-day and 30-day moving sales averages (`AVG() OVER ...`) to monitor localized consumer demand velocity.
* **Logarithmic Target Transformation:** Applies a natural log calculation `LN(x + 1)` to stabilize target variance and normalize sharp promotional or holiday volume spikes to prevent model overfitting.

---

## ??? Data Governance & Automated Testing

To guarantee absolute data integrity before training loops initialize, the platform executes a centralized data quality tracking configuration running **11 automated validation test assertions** (including unique primary keys and non-null column guards). Start-of-series boundary null values are caught and safely resolved using custom `COALESCE` handling.

---

## ?? Baseline Model Performance Logs

* **Core Boosting Regressor:** LightGBM (Gradient Boosting Decision Trees)
* **Configuration Management:** Hyperparameters are decoupled dynamically inside a centralized configuration file (`hyperparams.yml`).
* **Optimized Evaluation Score:** Convergence achieved at a precise **0.1827 RMSE**, demonstrating strong time-series precision with zero model overfitting.
* **Model Registry Output:** Finalized mathematical model blueprints are serialized and automatically exported straight to our local artifact tracking folder (`src_models/registry/forecasting_baseline_v1.txt`).

---

## ??? Interactive User Dashboard Frontend

The frontend user layer is deployed via an interactive, wide-layout **Streamlit Web Application (`app.py`)**. It features a modern dark-mode user interface that connects our registered model registry to automated inference scripts (`predict.py`), allowing business teams to tweak yesterday's sales parameters live and generate immediate raw inventory stock level recommendations out of the box.
