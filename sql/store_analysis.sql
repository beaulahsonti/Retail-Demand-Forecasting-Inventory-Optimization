-- ================================================================
-- STORE ANALYSIS
-- Retail Demand Forecasting & Inventory Optimization
-- ================================================================


-- ================================================================
-- QUERY 1: STORE PERFORMANCE SUMMARY
-- ================================================================

SELECT
    store_id,
    state_id,
    COUNT(*) AS records,
    SUM(demand) AS total_demand,
    ROUND(AVG(demand), 2) AS average_demand,
    ROUND(STDDEV(demand), 2) AS demand_std,
    MIN(demand) AS minimum_demand,
    MAX(demand) AS maximum_demand
FROM demand_data
GROUP BY
    store_id,
    state_id
ORDER BY total_demand DESC;


-- ================================================================
-- QUERY 2: STORE RANKING BY TOTAL DEMAND
-- ================================================================

SELECT
    store_id,
    state_id,
    SUM(demand) AS total_demand,
    RANK() OVER (
        ORDER BY SUM(demand) DESC
    ) AS demand_rank
FROM demand_data
GROUP BY
    store_id,
    state_id
ORDER BY demand_rank;


-- ================================================================
-- QUERY 3: TOP STORES BY DEMAND
-- ================================================================

SELECT
    store_id,
    state_id,
    SUM(demand) AS total_demand,
    ROUND(AVG(demand), 2) AS average_demand,
    MAX(demand) AS maximum_demand
FROM demand_data
GROUP BY
    store_id,
    state_id
ORDER BY total_demand DESC
LIMIT 5;


-- ================================================================
-- QUERY 4: LOWEST STORES BY DEMAND
-- ================================================================

SELECT
    store_id,
    state_id,
    SUM(demand) AS total_demand,
    ROUND(AVG(demand), 2) AS average_demand,
    MAX(demand) AS maximum_demand
FROM demand_data
GROUP BY
    store_id,
    state_id
ORDER BY total_demand ASC
LIMIT 5;


-- ================================================================
-- QUERY 5: STORE DEMAND BY CATEGORY
-- ================================================================

SELECT
    store_id,
    cat_id,
    SUM(demand) AS total_demand,
    ROUND(AVG(demand), 2) AS average_demand,
    COUNT(*) AS records
FROM demand_data
GROUP BY
    store_id,
    cat_id
ORDER BY
    store_id,
    total_demand DESC;


-- ================================================================
-- QUERY 6: STORE DEMAND BY DEPARTMENT
-- ================================================================

SELECT
    store_id,
    dept_id,
    SUM(demand) AS total_demand,
    ROUND(AVG(demand), 2) AS average_demand,
    COUNT(*) AS records
FROM demand_data
GROUP BY
    store_id,
    dept_id
ORDER BY
    store_id,
    total_demand DESC;


-- ================================================================
-- QUERY 7: STORE DEMAND BY STATE
-- ================================================================

SELECT
    state_id,
    store_id,
    SUM(demand) AS total_demand,
    ROUND(AVG(demand), 2) AS average_demand,
    COUNT(*) AS records
FROM demand_data
GROUP BY
    state_id,
    store_id
ORDER BY
    state_id,
    total_demand DESC;


-- ================================================================
-- QUERY 8: STORE ZERO-DEMAND ANALYSIS
-- ================================================================

SELECT
    store_id,
    state_id,
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
GROUP BY
    store_id,
    state_id
ORDER BY zero_demand_percentage DESC;


-- ================================================================
-- QUERY 9: DAILY STORE DEMAND
-- ================================================================

SELECT
    date,
    store_id,
    SUM(demand) AS total_demand,
    ROUND(AVG(demand), 2) AS average_demand
FROM demand_data
GROUP BY
    date,
    store_id
ORDER BY
    date,
    store_id;


-- ================================================================
-- QUERY 10: HIGHEST DEMAND PRODUCT-STORE COMBINATIONS
-- ================================================================

SELECT
    store_id,
    item_id,
    cat_id,
    dept_id,
    SUM(demand) AS total_demand,
    ROUND(AVG(demand), 2) AS average_demand,
    MAX(demand) AS maximum_demand
FROM demand_data
GROUP BY
    store_id,
    item_id,
    cat_id,
    dept_id
ORDER BY total_demand DESC
LIMIT 20;


-- ================================================================
-- STORE ANALYSIS COMPLETE
-- ================================================================