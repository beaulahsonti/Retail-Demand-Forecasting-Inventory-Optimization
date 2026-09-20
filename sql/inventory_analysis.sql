-- ================================================================
-- INVENTORY ANALYSIS
-- Retail Demand Forecasting & Inventory Optimization
-- ================================================================


-- ================================================================
-- QUERY 1: INVENTORY OPTIMIZATION SUMMARY
-- ================================================================

SELECT
    COUNT(*) AS product_store_combinations,
    ROUND(AVG(forecast_demand), 2) AS average_forecast_demand,
    ROUND(AVG(safety_stock), 2) AS average_safety_stock,
    ROUND(AVG(reorder_point), 2) AS average_reorder_point,
    ROUND(AVG(target_inventory), 2) AS average_target_inventory,
    ROUND(MAX(target_inventory), 2) AS maximum_target_inventory
FROM read_csv_auto(
    'reports/inventory_optimization.csv'
);


-- ================================================================
-- QUERY 2: INVENTORY LEVEL DISTRIBUTION
-- ================================================================

SELECT
    inventory_level,
    COUNT(*) AS product_store_combinations,
    ROUND(
        100.0 * COUNT(*) /
        SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM read_csv_auto(
    'reports/inventory_optimization.csv'
)
GROUP BY inventory_level
ORDER BY product_store_combinations DESC;


-- ================================================================
-- QUERY 3: RECOMMENDED ACTION DISTRIBUTION
-- ================================================================

SELECT
    recommended_action,
    COUNT(*) AS product_store_combinations,
    ROUND(
        100.0 * COUNT(*) /
        SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM read_csv_auto(
    'reports/inventory_optimization.csv'
)
GROUP BY recommended_action
ORDER BY product_store_combinations DESC;


-- ================================================================
-- QUERY 4: HIGHEST TARGET INVENTORY
-- ================================================================

SELECT
    item_id,
    store_id,
    ROUND(forecast_demand, 2) AS forecast_demand,
    ROUND(safety_stock, 2) AS safety_stock,
    ROUND(reorder_point, 2) AS reorder_point,
    ROUND(target_inventory, 2) AS target_inventory,
    inventory_level,
    recommended_action
FROM read_csv_auto(
    'reports/inventory_optimization.csv'
)
ORDER BY target_inventory DESC
LIMIT 20;


-- ================================================================
-- QUERY 5: LOWEST TARGET INVENTORY
-- ================================================================

SELECT
    item_id,
    store_id,
    ROUND(forecast_demand, 2) AS forecast_demand,
    ROUND(safety_stock, 2) AS safety_stock,
    ROUND(reorder_point, 2) AS reorder_point,
    ROUND(target_inventory, 2) AS target_inventory,
    inventory_level,
    recommended_action
FROM read_csv_auto(
    'reports/inventory_optimization.csv'
)
ORDER BY target_inventory ASC
LIMIT 20;


-- ================================================================
-- QUERY 6: SAFETY STOCK SUMMARY
-- ================================================================

SELECT
    COUNT(*) AS product_store_combinations,
    ROUND(AVG(safety_stock), 2) AS average_safety_stock,
    ROUND(MIN(safety_stock), 2) AS minimum_safety_stock,
    ROUND(MAX(safety_stock), 2) AS maximum_safety_stock
FROM read_csv_auto(
    'reports/safety_stock.csv'
);


-- ================================================================
-- QUERY 7: HIGHEST SAFETY STOCK REQUIREMENTS
-- ================================================================

SELECT
    item_id,
    store_id,
    ROUND(average_daily_demand, 2) AS average_daily_demand,
    ROUND(demand_std, 2) AS demand_std,
    ROUND(safety_stock, 2) AS safety_stock
FROM read_csv_auto(
    'reports/safety_stock.csv'
)
ORDER BY safety_stock DESC
LIMIT 20;


-- ================================================================
-- QUERY 8: REORDER POINT SUMMARY
-- ================================================================

SELECT
    COUNT(*) AS product_store_combinations,
    ROUND(AVG(reorder_point), 2) AS average_reorder_point,
    ROUND(MIN(reorder_point), 2) AS minimum_reorder_point,
    ROUND(MAX(reorder_point), 2) AS maximum_reorder_point
FROM read_csv_auto(
    'reports/reorder_point.csv'
);


-- ================================================================
-- QUERY 9: REORDER POINT BY INVENTORY LEVEL
-- ================================================================

SELECT
    inventory_level,
    COUNT(*) AS product_store_combinations,
    ROUND(AVG(reorder_point), 2) AS average_reorder_point,
    ROUND(AVG(safety_stock), 2) AS average_safety_stock,
    ROUND(AVG(average_daily_demand), 2) AS average_daily_demand
FROM read_csv_auto(
    'reports/reorder_point.csv'
)
GROUP BY inventory_level
ORDER BY average_reorder_point DESC;


-- ================================================================
-- QUERY 10: INVENTORY DECISION SUMMARY
-- ================================================================

SELECT
    item_id,
    store_id,
    ROUND(forecast_demand, 2) AS forecast_demand,
    ROUND(safety_stock, 2) AS safety_stock,
    ROUND(reorder_point, 2) AS reorder_point,
    ROUND(target_inventory, 2) AS target_inventory,
    inventory_level,
    recommended_action
FROM read_csv_auto(
    'reports/inventory_optimization.csv'
)
ORDER BY
    target_inventory DESC,
    forecast_demand DESC
LIMIT 30;


-- ================================================================
-- INVENTORY ANALYSIS COMPLETE
-- ================================================================