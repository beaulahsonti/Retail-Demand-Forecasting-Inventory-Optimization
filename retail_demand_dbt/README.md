# Retail Demand Forecasting & Inventory Optimization - dbt

## Overview

This dbt project forms the transformation layer of the Retail Demand Forecasting & Inventory Optimization pipeline.

The project transforms the curated M5 retail sales dataset stored in Snowflake into reusable analytical models for demand analysis, forecasting, and downstream inventory optimization.

## Architecture

Snowflake source data
        |
        v
Staging
        |
        v
Intermediate
        |
        v
Analytical Marts
        |
        v
Forecasting & Inventory Optimization

The dbt project follows a layered architecture:

- Staging - standardizes the curated Snowflake source.
- Intermediate - preserves clean daily-level demand data.
- Marts - produces weekly, monthly, and demand-profile datasets for analysis and modeling.

## Source

The existing Snowflake table:

`RETAIL_DEMAND.PUBLIC.SALES_WITH_CALENDAR`

is registered as a dbt source through `models/staging/sources.yml`.

## Models

### Staging

**`stg_sales_with_calendar`**

Standardizes the Week 1 curated sales-calendar dataset and renames fields into consistent analytical naming conventions.

**Grain:** one item-store-day observation.

### Intermediate

**`int_daily_sales`**

Provides a clean daily-level demand dataset for downstream aggregation and forecasting.

**Grain:** one item-store-day observation.

### Marts

**`fct_weekly_sales`**

Aggregates daily demand into weekly item-store sales.

**Output:** 8,354,260 rows.

**Grain:** one item-store-week.

**`fct_monthly_sales`**

Aggregates daily demand into monthly item-store sales.

**Output:** 1,951,360 rows.

**Grain:** one item-store-month.

**`mart_demand_profile`**

Creates reusable demand characteristics for each item-store sales series, including:

- Average daily demand
- Demand variability
- Peak daily demand
- Active sales days
- Zero-sales days
- Demand activity rate
- Coefficient of variation

This model extends the basic aggregation layer by creating demand features that can support downstream demand segmentation, forecasting, safety-stock analysis, and reorder-point logic.

**Grain:** one item-store sales series.

## Data Quality

The project includes automated dbt tests covering:

- Required-field NULL checks
- Daily item-store grain
- Weekly item-store grain
- Monthly item-store grain
- Demand-profile grain

The complete dbt pipeline was successfully built with:

**11/11 checks passing**

**0 warnings**

**0 errors**

## Documentation

Model and column descriptions are maintained through `schema.yml` files across the staging, intermediate, and mart layers.

dbt documentation and lineage artifacts are generated through:

`dbt docs generate`

## Technology Stack

- Python
- Snowflake
- SQL
- dbt
- M5 Forecasting Dataset

## Current Status

The core Week 2 transformation pipeline is complete and provides a validated analytical foundation for the next stages of the project:

**Exploratory Data Analysis -> Feature Engineering -> Demand Forecasting -> Inventory Optimization**