# Retail Demand Forecasting & Inventory Optimization

## Project Overview

This project is an end-to-end retail demand forecasting and inventory optimization platform.

The system uses historical retail sales data, product information, calendar events, pricing, and seasonal patterns to forecast future product demand and support inventory replenishment decisions.

## Objective

The main objectives of this project are:

- Analyze historical retail sales data.
- Identify demand trends and seasonal patterns.
- Build time-series forecasting models.
- Predict future product demand.
- Support inventory restocking decisions.
- Provide interactive visualizations for business users.
- Perform what-if analysis for pricing scenarios.

## Dataset

The project uses the **M5 Forecasting Dataset**, which contains hierarchical Walmart retail sales data.

The dataset includes information related to:

- Products
- Departments
- Categories
- Stores
- States
- Daily sales
- Calendar events
- Product prices

## Technology Stack

- Python
- SQL
- Google BigQuery
- dbt
- Prophet
- LightGBM
- Streamlit

## Project Workflow

```text
M5 Retail Dataset
        ↓
Data Ingestion
        ↓
Data Cleaning & Quality Checks
        ↓
BigQuery Data Warehouse
        ↓
dbt Data Transformation
        ↓
Feature Engineering
        ↓
Demand Forecasting
        ↓
Inventory Optimization
        ↓
Streamlit Dashboard
## Forecasting

The project will explore forecasting approaches such as:

- Baseline forecasting
- Prophet
- LightGBM

Model performance will be evaluated using appropriate forecasting metrics.

## Inventory Optimization

Forecasted demand will be used to support:

- Demand planning
- Reorder point calculations
- Safety stock analysis
- Restocking recommendations

## Dashboard

The Streamlit dashboard will allow users to explore:

- Historical sales
- Forecasted demand
- Store and product-level information
- Inventory recommendations
- What-if pricing scenarios

## Project Status

Currently under development.

## Team

Retail Demand Forecasting & Inventory Optimization Project