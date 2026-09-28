# BigQuery Data Warehouse Setup

## Cloud Platform

Google Cloud Platform

## Data Warehouse

Google BigQuery

## BigQuery Dataset

retail_demand

## Planned Tables

### calendar
Calendar and date-related information.

### sales
Daily product sales information.

### prices
Weekly product selling price information.

## Architecture

Google Cloud
    ↓
BigQuery
    ↓
retail_demand
    ├── calendar
    ├── sales
    └── prices

## Purpose

BigQuery will be used as the cloud data warehouse
for storing and querying the retail demand forecasting
data.