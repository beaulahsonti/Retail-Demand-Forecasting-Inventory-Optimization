/*
  Week 3: Day 1-3 Advanced Feature Engineering Data Mart
  Computes historical time-series lags and mathematical rolling averages
  across product-store combinations to create the final ML training matrix.
*/

WITH core_sales_mart AS (
    SELECT * FROM {{ ref('fct_daily_retail_sales') }}
),

time_series_features AS (
    SELECT
        -- Core Dimensions
        store_id,
        item_id,
        category_id,
        department_id,
        state_id,
        
        -- Time-Series Anchors
        walmart_year_week,
        weekday_name,
        weekday_number,
        calendar_month,
        calendar_year,
        
        -- Event Matrix Features
        event_primary_name,
        event_primary_type,
        is_snap_eligible_ca,
        is_snap_eligible_tx,
        is_snap_eligible_wi,
        
        -- Transactional Targets
        item_sell_price,
        daily_sales_units,
        daily_gross_revenue_usd,

        /* 
          1. Time-Series Lag Variables
          Pulls sales volume metrics from 1 day, 1 week, and 4 weeks ago
        */
        LAG(daily_sales_units, 1) OVER (
            PARTITION BY store_id, item_id 
            ORDER BY walmart_year_week, weekday_number
        ) AS sales_lag_1d,
        
        LAG(daily_sales_units, 7) OVER (
            PARTITION BY store_id, item_id 
            ORDER BY walmart_year_week, weekday_number
        ) AS sales_lag_7d,
        
        LAG(daily_sales_units, 28) OVER (
            PARTITION BY store_id, item_id 
            ORDER BY walmart_year_week, weekday_number
        ) AS sales_lag_28d,

        /* 
          2. Mathematical Rolling Averages
          Computes the mean sales demand over recent 7-day and 30-day windows
        */
        AVG(daily_sales_units) OVER (
            PARTITION BY store_id, item_id 
            ORDER BY walmart_year_week, weekday_number
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS sales_rolling_avg_7d,

        AVG(daily_sales_units) OVER (
            PARTITION BY store_id, item_id 
            ORDER BY walmart_year_week, weekday_number
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
        ) AS sales_rolling_avg_30d

    FROM core_sales_mart
)

SELECT * FROM time_series_features
