# Retail Demand Forecasting & Inventory Optimization

An end-to-end retail analytics and machine learning project for demand forecasting, inventory planning, and inventory optimization using **Python, SQL, DuckDB, Prophet, LightGBM, and Streamlit**.

---

## 1. Project Overview

Retail businesses need accurate demand forecasts to maintain sufficient inventory while avoiding unnecessary overstock.

This project provides an end-to-end analytical solution that:

- Loads and validates retail demand data
- Cleans and preprocesses the data
- Performs exploratory data analysis
- Creates time-series and lag-based features
- Builds multiple demand forecasting models
- Compares forecasting performance
- Calculates safety stock
- Calculates reorder points
- Produces inventory recommendations
- Performs analytical queries using SQL and DuckDB
- Provides a Streamlit dashboard for interactive analysis

The project is designed as a complete retail demand forecasting and inventory optimization workflow.

---

## 2. Business Objective

The main objective is to use historical retail demand data to:

1. Understand demand patterns.
2. Identify product, category, and store-level demand behavior.
3. Create useful forecasting features.
4. Forecast future demand.
5. Compare different forecasting approaches.
6. Calculate safety stock requirements.
7. Calculate reorder points.
8. Recommend appropriate inventory levels.
9. Provide analytical results through SQL and a dashboard.

---

## 3. Technology Stack

### Programming

- Python 3.9+

### Data Analysis

- Pandas
- NumPy
- SciPy

### Visualization

- Matplotlib
- Seaborn
- Plotly

### Machine Learning

- Scikit-learn
- LightGBM

### Forecasting

- Prophet

### Database / SQL

- DuckDB
- SQL

### Dashboard

- Streamlit

### Utilities

- Joblib
- OpenPyXL

---

## 4. Dataset

The project uses sampled retail demand data based on the M5-style retail forecasting dataset.

### Raw Dataset

```text
data/raw/
├── M5 sampled train.csv
└── M5 sampled test.csv
```

### Dataset Characteristics

The data contains retail demand information across:

- Products
- Departments
- Categories
- Stores
- States
- Dates
- Daily demand

### Main Columns

```text
id
item_id
dept_id
cat_id
store_id
state_id
demand
date
```

---

# 5. Project Workflow

```text
M5 Retail Demand Dataset
          ↓
Data Ingestion
          ↓
Data Validation
          ↓
Data Cleaning & Preprocessing
          ↓
Exploratory Data Analysis
          ↓
Feature Engineering
          ↓
Train / Validation Split
          ↓
Demand Forecasting
          ↓
Baseline Forecasting
          ↓
Prophet Forecasting
          ↓
LightGBM Forecasting
          ↓
Model Evaluation & Comparison
          ↓
Demand Forecast Generation
          ↓
Safety Stock Calculation
          ↓
Reorder Point Calculation
          ↓
Inventory Optimization
          ↓
SQL Analytics using DuckDB
          ↓
Streamlit Dashboard
          ↓
Business Insights
```

---

## 6. Data Ingestion

The project starts by loading the raw retail demand datasets from the `data/raw/` directory.

The ingestion workflow prepares the raw train and test datasets for validation and downstream processing.

### Data Flow

```text
Raw CSV Files
      ↓
Load Dataset
      ↓
Inspect Columns
      ↓
Check Data Types
      ↓
Validate Dates
      ↓
Validate Demand Values
      ↓
Prepare Data for Cleaning
```

---

## 7. Data Validation

The data validation process checks the quality and consistency of the input data.

Validation includes:

- Negative demand checks
- Invalid date checks
- Missing-value checks
- Unique product checks
- Department checks
- Category checks
- Store checks
- State checks
- Date-range validation

The processed training data contains **248,690 records**, while the test/forecast validation data contains **3,640 records**.

---

## 8. Data Cleaning & Preprocessing

The cleaning stage prepares the data for analysis and forecasting.

Main processing steps include:

- Converting date fields to proper date format
- Validating demand values
- Standardizing categorical fields
- Removing invalid records
- Preparing clean train and test datasets

### Processed Files

```text
data/processed/
├── clean_train.csv
├── clean_test.csv
├── model_features.csv
├── forecast_train.csv
└── forecast_validation.csv
```

---

## 9. Exploratory Data Analysis

Exploratory Data Analysis is used to understand historical demand patterns.

The analysis covers:

- Daily demand trends
- Monthly demand trends
- Demand by category
- Demand by product
- Demand by store
- Demand distribution
- Zero-demand behavior
- Product-store demand patterns

### EDA Outputs

```text
outputs/figures/
├── daily_demand_trend.png
├── demand_by_category.png
├── demand_by_product.png
├── demand_by_store.png
├── demand_distribution.png
└── monthly_demand_trend.png
```

### EDA Reports

```text
reports/
├── eda_summary.csv
└── product_store_demand_summary.csv
```

The dataset contains a significant number of zero-demand observations, which is an important characteristic considered during demand analysis.

---

## 10. Feature Engineering

Time-series and lag-based features are created to improve forecasting performance.

### Time Features

```text
day_of_week
day_of_month
week_of_year
month
quarter
year
is_weekend
```

### Lag Features

```text
lag_1
lag_7
lag_14
lag_28
```

### Rolling Features

```text
rolling_mean_7
rolling_mean_28
rolling_std_7
rolling_std_28
```

The feature engineering process produces:

```text
data/processed/model_features.csv
```

---

## 11. Forecast Train / Validation Split

The forecasting dataset is divided into training and validation periods.

### Training Period

```text
2011-01-30 → 2016-02-29
```

### Validation Period

```text
2016-03-01 → 2016-03-28
```

### Dataset Sizes

```text
Total feature rows: 245,050
Training rows:      241,410
Validation rows:      3,640
```

This time-based split is used to evaluate forecasting performance on future observations.

---

# 12. Demand Forecasting

Multiple forecasting approaches are implemented and compared.

```text
Historical Demand
       ↓
Feature Engineering
       ↓
Train Forecasting Models
       ↓
Generate Predictions
       ↓
Evaluate Predictions
       ↓
Compare Models
```

The project includes:

1. Baseline Forecasting
2. Prophet
3. LightGBM

---

## 13. Baseline Forecasting

The baseline model uses the previous 7-day demand as a simple forecasting reference.

### Baseline Results

```text
MAE:   1.0527
RMSE:  1.9956
WAPE:  103.48%
sMAPE: 134.13%
```

Output:

```text
outputs/forecasts/baseline_predictions.csv
reports/baseline_metrics.csv
```

---

## 14. Prophet Forecasting

Prophet is used as a time-series forecasting approach.

The Prophet model is evaluated using the same validation period as the other forecasting approaches.

### Prophet Results

```text
MAE:   0.9238
RMSE:  1.5743
WAPE:  90.81%
sMAPE: 138.91%
```

---

## 15. LightGBM Forecasting

LightGBM is used with engineered time-series and categorical features.

### Model Configuration

```text
Total features:       20
Categorical features: 5
Numerical features:  15
```

### LightGBM Results

```text
MAE:   0.8643
RMSE:  1.5303
WAPE:  84.96%
sMAPE: 137.47%
```

### LightGBM Outputs

```text
outputs/forecasts/lightgbm_predictions.csv

reports/lightgbm_metrics.csv
reports/lightgbm_feature_importance.csv
```

---

## 16. Model Comparison

The forecasting models are evaluated using:

- MAE
- RMSE
- WAPE
- sMAPE

### Model Results

| Model | Validation Rows | MAE | RMSE | WAPE | sMAPE |
|---|---:|---:|---:|---:|---:|
| LightGBM | 3,640 | 0.8643 | 1.5303 | 84.96% | 137.47% |
| Prophet | 3,640 | 0.9238 | 1.5743 | 90.81% | 138.91% |
| Baseline | 3,640 | 1.0527 | 1.9956 | 103.48% | 134.13% |

Comparison output:

```text
reports/model_comparison.csv
```

---

# 17. Safety Stock Calculation

Safety stock is calculated to provide a buffer against demand variability during the lead time.

The implemented inventory workflow uses:

```text
Service Level: 95%
Lead Time:     7 days
Z-Value:       1.645
```

### Safety Stock Summary

```text
Product-store combinations: 130
Average safety stock:        5.21
Maximum safety stock:       30.00
Minimum safety stock:        0.59
```

Output:

```text
reports/safety_stock.csv
```

---

# 18. Reorder Point Calculation

The reorder point determines when inventory should be replenished.

The calculation considers expected demand during lead time together with safety stock.

### Reorder Point Summary

```text
Average reorder point: 10.48
Maximum reorder point: 75.92
Minimum reorder point:  0.66
```

### Inventory Level Distribution

```text
Medium: 57
Low:    48
High:   25
```

Output:

```text
reports/reorder_point.csv
```

---

# 19. Inventory Optimization

The inventory optimization stage combines forecasts and inventory requirements to produce recommended inventory levels.

### Optimization Summary

```text
Product-store combinations: 130
Forecast horizon:             7 days
Average forecast demand:     28.37
Average recommended inventory: 12.31
Average target inventory:    13.06
Maximum target inventory:    75.92
```

### Recommended Actions

```text
Maintain Stock:        57
Maintain Safety Stock: 48
Maintain High Stock:   25
```

Output:

```text
reports/inventory_optimization.csv
```

---

# 20. SQL Analytics with DuckDB

DuckDB is used to perform analytical SQL queries on the processed retail demand and forecasting data.

### Database

```text
data/retail_demand.duckdb
```

### SQL Files

```text
sql/
├── demand_summary.sql
├── product_analysis.sql
├── store_analysis.sql
├── forecast_analysis.sql
└── inventory_analysis.sql
```

### SQL Analytics Include

- Total demand
- Average daily demand
- Product-level demand
- Store-level demand
- Category-level demand
- Forecast performance
- Inventory levels
- Reorder points
- Inventory recommendations

The SQL workflow is executed through:

```text
src/analytics/run_sql.py
```

---

# 21. Streamlit Dashboard

The project includes an interactive Streamlit dashboard for exploring forecasting and inventory results.

### Dashboard

```text
dashboard/app.py
```

### Dashboard Sections

```text
1. Overview
2. Model Performance
3. Forecast Analysis
4. Inventory Optimization
5. Feature Importance
6. Data Summary
```

### Dashboard Workflow

```text
Processed Data
      ↓
Forecast Results
      ↓
Inventory Results
      ↓
SQL Analytics
      ↓
Streamlit Dashboard
      ↓
Interactive Business Analysis
```

The dashboard includes:

- KPI cards
- Forecasting metrics
- Model comparison charts
- Forecast demand charts
- Inventory optimization results
- Feature importance visualization
- Product and store analysis
- Data summary tables
- Interactive Plotly charts

---

# 22. Project Structure

```text
Retail-Demand-Forecasting-Inventory-Optimization/
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── raw/
│   │   ├── M5 sampled train.csv
│   │   └── M5 sampled test.csv
│   │
│   ├── processed/
│   │   ├── clean_train.csv
│   │   ├── clean_test.csv
│   │   ├── model_features.csv
│   │   ├── forecast_train.csv
│   │   └── forecast_validation.csv
│   │
│   └── retail_demand.duckdb
│
├── docs/
│   ├── PROJECT_DOCUMENTATION.md
│   └── RESPONSIVE_KPI_TESTING_2026-09-23.md
│
├── models/
│
├── notebooks/
│
├── outputs/
│   ├── figures/
│   └── forecasts/
│
├── reports/
│   ├── baseline_metrics.csv
│   ├── eda_summary.csv
│   ├── inventory_optimization.csv
│   ├── lightgbm_feature_importance.csv
│   ├── lightgbm_metrics.csv
│   ├── model_comparison.csv
│   ├── product_store_demand_summary.csv
│   ├── reorder_point.csv
│   └── safety_stock.csv
│
├── sql/
│   ├── demand_summary.sql
│   ├── product_analysis.sql
│   ├── store_analysis.sql
│   ├── forecast_analysis.sql
│   └── inventory_analysis.sql
│
├── src/
│   ├── ingestion/
│   ├── cleaning/
│   ├── analytics/
│   ├── forecasting/
│   └── inventory/
│
├── tests/
│
├── .gitignore
├── .python-version
├── README.md
└── requirements.txt
```

---

# 23. Local Environment Setup

Create and activate the Python virtual environment.

### Windows PowerShell

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

---

# 24. Running the Project

### Run Data Processing

The individual scripts inside `src/` can be executed according to the project workflow.

### Run SQL Analytics

```powershell
python src/analytics/run_sql.py
```

### Run Streamlit Dashboard

```powershell
python -m streamlit run dashboard/app.py
```

The dashboard normally opens at:

```text
http://localhost:8501
```

---

# 25. Deployment

The Streamlit dashboard is suitable for deployment using a Python-compatible hosting platform.

The project includes:

```text
.python-version
```

with:

```text
3.9.6
```

This keeps the deployment Python version aligned with the local development environment.

The Streamlit application entry point is:

```text
dashboard/app.py
```

---

# 26. Outputs

The project produces several types of outputs.

### Forecast Outputs

```text
outputs/forecasts/
├── baseline_predictions.csv
└── lightgbm_predictions.csv
```

### Visualization Outputs

```text
outputs/figures/
├── daily_demand_trend.png
├── demand_by_category.png
├── demand_by_product.png
├── demand_by_store.png
├── demand_distribution.png
└── monthly_demand_trend.png
```

### Analytical Reports

```text
reports/
├── baseline_metrics.csv
├── eda_summary.csv
├── inventory_optimization.csv
├── lightgbm_feature_importance.csv
├── lightgbm_metrics.csv
├── model_comparison.csv
├── product_store_demand_summary.csv
├── reorder_point.csv
└── safety_stock.csv
```

---

# 27. Key Project Results

The completed workflow produces:

```text
248,690
Training / processed demand records
```

```text
3,640
Validation forecast records
```

```text
13
Unique products
```

```text
10
Stores
```

```text
130
Product-store inventory combinations
```

The forecasting workflow evaluates three approaches:

```text
Baseline
   ↓
Prophet
   ↓
LightGBM
```

The inventory workflow produces:

```text
Safety Stock
      ↓
Reorder Point
      ↓
Target Inventory
      ↓
Recommended Inventory Action
```

---

# 28. Business Value

The project demonstrates how retail organizations can combine:

```text
Historical Sales Data
        +
Data Analytics
        +
Machine Learning
        +
Time-Series Forecasting
        +
Inventory Planning
        +
SQL Analytics
        +
Interactive Dashboard
```

to support data-driven retail demand and inventory analysis.

The workflow helps analysts and supply-chain teams understand demand patterns, evaluate forecasts, estimate inventory requirements, and review inventory recommendations through a single analytical platform.

---

# 29. Documentation

Detailed project documentation is available in:

```text
docs/PROJECT_DOCUMENTATION.md
```

Responsive dashboard testing notes are available in:

```text
docs/RESPONSIVE_KPI_TESTING_2026-09-23.md
```

---

# 30. Project Status

The project contains an end-to-end workflow covering:

```text
Data Ingestion
      ↓
Data Validation
      ↓
Data Cleaning
      ↓
EDA
      ↓
Feature Engineering
      ↓
Forecasting
      ↓
Model Evaluation
      ↓
Safety Stock
      ↓
Reorder Point
      ↓
Inventory Optimization
      ↓
SQL Analytics
      ↓
Streamlit Dashboard
      ↓
Deployment
```

The project is structured so that each stage produces reusable data, reports, forecasts, or dashboard inputs for the next stage.
