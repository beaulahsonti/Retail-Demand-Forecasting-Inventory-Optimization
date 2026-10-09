# Retail Demand Forecasting & Inventory Optimization

An end-to-end retail analytics platform for demand forecasting and inventory planning.

## Project Overview

This project processes retail sales data, engineers time-series features, evaluates multiple forecasting models, and converts demand forecasts into inventory recommendations.

## Architecture

Raw Retail Data
        ↓
Data Preprocessing
        ↓
DuckDB Integration
        ↓
Exploratory Data Analysis
        ↓
Feature Engineering
        ↓
Demand Forecasting
        ↓
Model Evaluation
        ↓
Inventory Optimization
        ↓
Streamlit Dashboard

## Technologies

- Python
- Pandas
- NumPy
- DuckDB
- Scikit-learn
- Prophet
- LightGBM
- Streamlit
- SQL
- dbt
- BigQuery-ready architecture

## Dataset

The project uses an M5-style retail sales dataset containing:

- Daily sales
- Product information
- Store information
- Calendar information
- Event information
- SNAP indicators
- Historical selling prices

Raw dataset files are excluded from Git using `.gitignore`.

## Data Processing

The pipeline includes:

1. Dataset inspection
2. Sales wide-to-long transformation
3. Calendar preprocessing
4. Price preprocessing
5. Sales/calendar/price integration
6. Data validation
7. Exploratory analysis
8. Trend and seasonality analysis
9. Feature engineering

## Forecasting

Three forecasting approaches were evaluated:

- 7-day lag baseline
- Prophet
- LightGBM

### Model Evaluation

| Model | MAE | RMSE |
|---|---:|---:|
| Baseline | 15.5807 | 26.7332 |
| Prophet | 40.4764 | 54.7520 |
| LightGBM | 11.4525 | 19.7259 |

The metrics above correspond to the project's evaluated test splits.

## Inventory Optimization

The project generates:

- Average demand
- Demand variability
- Forecast demand
- Safety stock
- Lead-time demand
- Reorder point
- Recommended inventory
- Inventory priority

The current inventory analysis uses a configurable:

- Lead time: 7 days
- Service-level z-value: 1.65

These are project assumptions and can be changed according to operational requirements.

## Dashboard

The Streamlit dashboard provides:

- Executive KPIs
- Forecast monitoring
- Model performance comparison
- Inventory priority analysis
- Reorder-point analysis
- Inventory alerts
- Item/store filtering
- Inventory recommendations

Run the dashboard with:

```bash
python -m streamlit run app.py