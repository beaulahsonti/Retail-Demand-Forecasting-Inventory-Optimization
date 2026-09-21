# Retail Demand Forecasting & Inventory Optimization

## 1. Project Overview

This project is an end-to-end retail analytics solution designed to forecast product demand and support inventory planning.

The workflow covers:

- Data validation
- Data cleaning
- Exploratory data analysis
- Feature engineering
- Demand forecasting
- Forecast model evaluation
- SQL and DuckDB analytics
- Safety stock calculation
- Reorder point calculation
- Inventory optimization
- Streamlit dashboard development

## 2. Dataset

The project uses sampled M5 retail demand data.

The main fields include:

- id
- item_id
- dept_id
- cat_id
- store_id
- state_id
- demand
- date

The training dataset contains 248,690 records.

The project uses separate raw and processed data locations so that the original dataset is preserved while cleaned data is prepared for analysis and modeling.

## 3. Data Validation and Cleaning

The input data was first validated for:

- Invalid dates
- Negative demand values
- Product counts
- Department counts
- Category counts
- Store counts
- State counts

The validation process confirmed that there were no negative demand values and no invalid dates in the training data.

Cleaned datasets were generated for use in the downstream analysis and forecasting workflow.

## 4. Exploratory Data Analysis

Exploratory analysis was performed using Python, pandas and visualization libraries.

The analysis examined:

- Daily demand trends
- Monthly demand trends
- Demand by category
- Demand by product
- Demand by store
- Demand distribution
- Zero-demand records

The generated visualizations are stored in the project output directories.

## 5. Feature Engineering

Time-series and calendar features were created from the demand history.

Calendar features include:

- Day of week
- Day of month
- Week of year
- Month
- Quarter
- Year
- Weekend indicator

Historical demand features include:

- Lag 1
- Lag 7
- Lag 14
- Lag 28
- Rolling mean 7
- Rolling mean 28
- Rolling standard deviation 7
- Rolling standard deviation 28

These features provide the forecasting models with both calendar information and historical demand patterns.

## 6. Forecasting Dataset

A chronological training and validation split was used because the project is based on time-series forecasting.

The validation period follows the training period rather than using a random split.

This helps evaluate the models on a later time period using historical information available before that period.

## 7. Forecasting Models

Three forecasting approaches were implemented:

### Baseline

A 7-day lag forecasting approach was used as the baseline.

This provides a simple reference point against which the machine-learning and time-series models can be evaluated.

### Prophet

Prophet was implemented for time-series forecasting and evaluated on the validation period.

### LightGBM

LightGBM was implemented using engineered calendar, lag, rolling and categorical features.

Feature importance was also generated to help understand the contribution of the model inputs.

## 8. Model Evaluation

The forecasting models were evaluated using:

- MAE
- RMSE
- WAPE
- sMAPE

The model outputs and comparison results are stored under the reports and forecasts directories.

The comparison allows the forecasting approaches to be evaluated using the same validation period and metrics.

## 9. SQL and DuckDB Analytics

DuckDB was used to create a local analytical database for the project.

SQL analysis was organized into separate scripts for:

- Demand summaries
- Product analysis
- Store analysis
- Forecast analysis
- Inventory analysis

The SQL execution workflow loads the processed demand data and executes the analytical queries against DuckDB.

## 10. Safety Stock

Safety stock was calculated at the product-store level using demand variability, service-level assumptions and lead-time information.

The project uses:

- 95% service level
- 7-day lead time
- Corresponding service-level z-score

The resulting safety-stock calculations are stored in the project reports.

## 11. Reorder Point

The reorder point calculation combines expected demand during lead time with safety stock.

The resulting reorder-point report also provides inventory-level classifications to support inventory planning.

## 12. Inventory Optimization

The inventory optimization workflow combines:

- Forecast demand
- Safety stock
- Reorder point
- Inventory requirements

The workflow produces recommended inventory levels and recommended inventory actions for product-store combinations.

## 13. Dashboard

A Streamlit dashboard was developed to present the project results.

The dashboard brings together:

- Demand analysis
- Forecasting results
- Model comparison
- Inventory metrics
- Safety stock information
- Reorder point information
- Inventory optimization results

This provides a single interface for reviewing the analytical results.

## 14. Project Technologies

The project uses:

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Prophet
- LightGBM
- DuckDB
- SQL
- Streamlit
- Plotly
- Joblib

## 15. Project Workflow

The overall workflow is:

Raw Data  
↓  
Data Validation  
↓  
Data Cleaning  
↓  
Exploratory Data Analysis  
↓  
Feature Engineering  
↓  
Train / Validation Split  
↓  
Baseline Forecast  
↓  
Prophet Forecast  
↓  
LightGBM Forecast  
↓  
Model Evaluation  
↓  
SQL / DuckDB Analytics  
↓  
Safety Stock  
↓  
Reorder Point  
↓  
Inventory Optimization  
↓  
Streamlit Dashboard

## 16. Outputs

The project generates:

- Cleaned datasets
- EDA visualizations
- Feature-engineered datasets
- Forecast predictions
- Forecast evaluation metrics
- Model comparison reports
- Feature importance results
- Safety stock reports
- Reorder point reports
- Inventory optimization reports

## 17. Development Approach

The project was developed as a modular pipeline so that data preparation, analytics, forecasting and inventory calculations are separated into individual components.

This structure makes the workflow easier to test, maintain and extend.

Each major stage produces reusable outputs that are consumed by the next stage of the pipeline.