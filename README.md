# Retail Demand Forecasting & Inventory Optimization

An end-to-end retail analytics and machine learning project for demand forecasting, inventory planning, and inventory optimization using Python, SQL, DuckDB, Prophet, LightGBM, and Streamlit.

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

### Data Storage

- CSV
- Excel-compatible data processing
- DuckDB database

### Model / Utility

- Joblib
- OpenPyXL

---

## 4. Dataset

The project uses sampled retail demand data based on the M5-style retail forecasting dataset.

### Raw files

```text
data/raw/
├── M5 sampled train.csv
└── M5 sampled test.csv
