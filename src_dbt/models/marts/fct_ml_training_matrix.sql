/*
  Week 3: Day 3 Feature Scaling & Label Engineering
  Applies logarithmic target transformation (log1p) to stabilize variance
  and compiles the finalized, high-performance ML model feature training matrix.
*/

WITH predictive_features AS (
    SELECT * FROM {{ ref('fct_predictive_features') }}
),

final_ml_matrix AS (
    SELECT
        -- Core Primary Dimensions
        store_id,
        item_id,
        category_id,
        department_id,
        state_id,
        
        -- Time Horizon Pointers
        walmart_year_week,
        weekday_name,
        weekday_number,
        calendar_month,
        calendar_year,
        
        -- Categorical Context Encodings
        event_primary_name,
        event_primary_type,
        is_snap_eligible_ca,
        is_snap_eligible_tx,
        is_snap_eligible_wi,
        
        -- Historical Time-Series Lags & Rolling Window Matrices
        sales_lag_1d,
        sales_lag_7d,
        sales_lag_28d,
        sales_rolling_avg_7d,
        sales_rolling_avg_30d,
        item_sell_price,

        -- Target Variable Raw Matrix
        daily_sales_units,

        /*
          Logarithmic Target Transformation: ln(x + 1)
          Stabilizes feature variances and normalizes historical demand distortions
          to prevent forecasting model overfitting during training loops next week.
        */
        LOG(daily_sales_units + 1.0) AS log_daily_sales_units

    FROM predictive_features
)

SELECT * FROM final_ml_matrix
