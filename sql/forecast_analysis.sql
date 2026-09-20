-- ================================================================
-- FORECAST ANALYSIS
-- Retail Demand Forecasting & Inventory Optimization
-- ================================================================


-- ================================================================
-- QUERY 1: FORECAST MODEL PERFORMANCE
-- ================================================================

SELECT
    model,
    validation_rows,
    ROUND(MAE, 4) AS MAE,
    ROUND(RMSE, 4) AS RMSE,
    ROUND(WAPE, 2) AS WAPE,
    ROUND(sMAPE, 2) AS sMAPE
FROM read_csv_auto(
    'reports/model_comparison.csv'
)
ORDER BY MAE ASC;


-- ================================================================
-- QUERY 2: LIGHTGBM FORECAST SUMMARY
-- ================================================================

SELECT
    COUNT(*) AS forecast_records,
    COUNT(DISTINCT item_id) AS unique_products,
    COUNT(DISTINCT store_id) AS unique_stores,
    ROUND(SUM(prediction), 2) AS total_forecast_demand,
    ROUND(AVG(prediction), 2) AS average_forecast_demand,
    ROUND(MIN(prediction), 2) AS minimum_forecast,
    ROUND(MAX(prediction), 2) AS maximum_forecast
FROM read_csv_auto(
    'outputs/forecasts/lightgbm_predictions.csv'
);


-- ================================================================
-- QUERY 3: FORECAST BY PRODUCT
-- ================================================================

SELECT
    item_id,
    ROUND(SUM(prediction), 2) AS forecast_demand,
    ROUND(AVG(prediction), 2) AS average_forecast,
    ROUND(MIN(prediction), 2) AS minimum_forecast,
    ROUND(MAX(prediction), 2) AS maximum_forecast
FROM read_csv_auto(
    'outputs/forecasts/lightgbm_predictions.csv'
)
GROUP BY item_id
ORDER BY forecast_demand DESC;


-- ================================================================
-- QUERY 4: FORECAST BY STORE
-- ================================================================

SELECT
    store_id,
    ROUND(SUM(prediction), 2) AS forecast_demand,
    ROUND(AVG(prediction), 2) AS average_forecast,
    ROUND(MIN(prediction), 2) AS minimum_forecast,
    ROUND(MAX(prediction), 2) AS maximum_forecast
FROM read_csv_auto(
    'outputs/forecasts/lightgbm_predictions.csv'
)
GROUP BY store_id
ORDER BY forecast_demand DESC;


-- ================================================================
-- QUERY 5: FORECAST BY PRODUCT AND STORE
-- ================================================================

SELECT
    item_id,
    store_id,
    ROUND(SUM(prediction), 2) AS forecast_demand,
    ROUND(AVG(prediction), 2) AS average_forecast,
    ROUND(MAX(prediction), 2) AS maximum_forecast
FROM read_csv_auto(
    'outputs/forecasts/lightgbm_predictions.csv'
)
GROUP BY
    item_id,
    store_id
ORDER BY forecast_demand DESC
LIMIT 30;


-- ================================================================
-- QUERY 6: DAILY FORECAST DEMAND
-- ================================================================

SELECT
    date,
    ROUND(SUM(prediction), 2) AS total_forecast_demand,
    ROUND(AVG(prediction), 2) AS average_forecast_demand,
    ROUND(MAX(prediction), 2) AS maximum_forecast_demand
FROM read_csv_auto(
    'outputs/forecasts/lightgbm_predictions.csv'
)
GROUP BY date
ORDER BY date;


-- ================================================================
-- QUERY 7: ACTUAL VS FORECAST DEMAND
-- ================================================================

SELECT
    date,
    ROUND(SUM(actual_demand), 2) AS actual_demand,
    ROUND(SUM(prediction), 2) AS predicted_demand,
    ROUND(
        SUM(prediction) - SUM(actual_demand),
        2
    ) AS forecast_error
FROM read_csv_auto(
    'outputs/forecasts/lightgbm_predictions.csv'
)
GROUP BY date
ORDER BY date;


-- ================================================================
-- QUERY 8: PRODUCT FORECAST ERROR
-- ================================================================

SELECT
    item_id,

    ROUND(
        AVG(
            ABS(
                actual_demand - prediction
            )
        ),
        4
    ) AS MAE,

    ROUND(
        SQRT(
            AVG(
                POWER(
                    actual_demand - prediction,
                    2
                )
            )
        ),
        4
    ) AS RMSE,

    ROUND(
        SUM(actual_demand),
        2
    ) AS actual_demand,

    ROUND(
        SUM(prediction),
        2
    ) AS predicted_demand

FROM read_csv_auto(
    'outputs/forecasts/lightgbm_predictions.csv'
)
GROUP BY item_id
ORDER BY MAE ASC;


-- ================================================================
-- QUERY 9: STORE FORECAST ERROR
-- ================================================================

SELECT
    store_id,

    ROUND(
        AVG(
            ABS(
                actual_demand - prediction
            )
        ),
        4
    ) AS MAE,

    ROUND(
        SQRT(
            AVG(
                POWER(
                    actual_demand - prediction,
                    2
                )
            )
        ),
        4
    ) AS RMSE,

    ROUND(
        SUM(actual_demand),
        2
    ) AS actual_demand,

    ROUND(
        SUM(prediction),
        2
    ) AS predicted_demand

FROM read_csv_auto(
    'outputs/forecasts/lightgbm_predictions.csv'
)
GROUP BY store_id
ORDER BY MAE ASC;


-- ================================================================
-- QUERY 10: TOP FORECAST DEMAND COMBINATIONS
-- ================================================================

SELECT
    item_id,
    store_id,
    ROUND(
        SUM(prediction),
        2
    ) AS forecast_demand,

    ROUND(
        AVG(prediction),
        2
    ) AS average_forecast

FROM read_csv_auto(
    'outputs/forecasts/lightgbm_predictions.csv'
)
GROUP BY
    item_id,
    store_id
ORDER BY forecast_demand DESC
LIMIT 20;


-- ================================================================
-- FORECAST ANALYSIS COMPLETE
-- ================================================================