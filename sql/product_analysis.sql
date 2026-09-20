-- ================================================================
-- PRODUCT ANALYSIS
-- Retail Demand Forecasting & Inventory Optimization
-- ================================================================


-- ================================================================
-- QUERY 1: PRODUCT PERFORMANCE SUMMARY
-- ================================================================

SELECT
    item_id,
    COUNT(*) AS records,
    SUM(demand) AS total_demand,
    ROUND(AVG(demand), 2) AS average_demand,
    ROUND(STDDEV(demand), 2) AS demand_std,
    MIN(demand) AS minimum_demand,
    MAX(demand) AS maximum_demand
FROM demand_data
GROUP BY item_id
ORDER BY total_demand DESC;


-- ================================================================
-- QUERY 2: PRODUCT RANKING BY TOTAL DEMAND
-- ================================================================

SELECT
    item_id,
    SUM(demand) AS total_demand,
    RANK() OVER (
        ORDER BY SUM(demand) DESC
    ) AS demand_rank
FROM demand_data
GROUP BY item_id
ORDER BY demand_rank;


-- ================================================================
-- QUERY 3: TOP 5 PRODUCTS BY DEMAND
-- ================================================================

SELECT
    item_id,
    SUM(demand) AS total_demand,
    ROUND(AVG(demand), 2) AS average_demand,
    MAX(demand) AS maximum_demand
FROM demand_data
GROUP BY item_id
ORDER BY total_demand DESC
LIMIT 5;


-- ================================================================
-- QUERY 4: LOWEST 5 PRODUCTS BY DEMAND
-- ================================================================

SELECT
    item_id,
    SUM(demand) AS total_demand,
    ROUND(AVG(demand), 2) AS average_demand,
    MAX(demand) AS maximum_demand
FROM demand_data
GROUP BY item_id
ORDER BY total_demand ASC
LIMIT 5;


-- ================================================================
-- QUERY 5: PRODUCT DEMAND BY CATEGORY
-- ================================================================

SELECT
    cat_id,
    item_id,
    SUM(demand) AS total_demand,
    ROUND(AVG(demand), 2) AS average_demand,
    COUNT(*) AS records
FROM demand_data
GROUP BY
    cat_id,
    item_id
ORDER BY
    cat_id,
    total_demand DESC;


-- ================================================================
-- QUERY 6: PRODUCT DEMAND BY DEPARTMENT
-- ================================================================

SELECT
    dept_id,
    item_id,
    SUM(demand) AS total_demand,
    ROUND(AVG(demand), 2) AS average_demand,
    COUNT(*) AS records
FROM demand_data
GROUP BY
    dept_id,
    item_id
ORDER BY
    dept_id,
    total_demand DESC;


-- ================================================================
-- QUERY 7: PRODUCT-STORE PERFORMANCE
-- ================================================================

SELECT
    item_id,
    store_id,
    SUM(demand) AS total_demand,
    ROUND(AVG(demand), 2) AS average_demand,
    ROUND(STDDEV(demand), 2) AS demand_std,
    MAX(demand) AS maximum_demand
FROM demand_data
GROUP BY
    item_id,
    store_id
ORDER BY total_demand DESC
LIMIT 30;


-- ================================================================
-- QUERY 8: PRODUCT DEMAND BY STATE
-- ================================================================

SELECT
    item_id,
    state_id,
    SUM(demand) AS total_demand,
    ROUND(AVG(demand), 2) AS average_demand,
    COUNT(*) AS records
FROM demand_data
GROUP BY
    item_id,
    state_id
ORDER BY
    item_id,
    total_demand DESC;


-- ================================================================
-- QUERY 9: PRODUCT ZERO-DEMAND ANALYSIS
-- ================================================================

SELECT
    item_id,
    COUNT(*) AS total_records,
    SUM(
        CASE
            WHEN demand = 0 THEN 1
            ELSE 0
        END
    ) AS zero_demand_records,
    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN demand = 0 THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS zero_demand_percentage
FROM demand_data
GROUP BY item_id
ORDER BY zero_demand_percentage DESC;


-- ================================================================
-- QUERY 10: HIGHEST DEMAND PRODUCT-STORE COMBINATIONS
-- ================================================================

SELECT
    item_id,
    store_id,
    cat_id,
    dept_id,
    SUM(demand) AS total_demand,
    ROUND(AVG(demand), 2) AS average_demand,
    MAX(demand) AS maximum_demand
FROM demand_data
GROUP BY
    item_id,
    store_id,
    cat_id,
    dept_id
ORDER BY total_demand DESC
LIMIT 20;


-- ================================================================
-- PRODUCT ANALYSIS COMPLETE
-- ================================================================