-- ================================================================
-- RETAIL DEMAND SUMMARY
-- ================================================================
-- Purpose:
-- Analyze overall demand, product demand, store demand,
-- category demand, and monthly demand.
-- ================================================================


-- ================================================================
-- 1. OVERALL DEMAND SUMMARY
-- ================================================================

SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT item_id) AS unique_products,
    COUNT(DISTINCT store_id) AS unique_stores,
    COUNT(DISTINCT cat_id) AS unique_categories,
    MIN(date) AS start_date,
    MAX(date) AS end_date,
    ROUND(SUM(demand), 2) AS total_demand,
    ROUND(AVG(demand), 2) AS average_daily_demand,
    ROUND(MIN(demand), 2) AS minimum_demand,
    ROUND(MAX(demand), 2) AS maximum_demand
FROM read_csv_auto(
    'data/processed/clean_train.csv'
);


-- ================================================================
-- 2. DEMAND BY PRODUCT
-- ================================================================

SELECT
    item_id,
    COUNT(*) AS records,
    ROUND(SUM(demand), 2) AS total_demand,
    ROUND(AVG(demand), 2) AS average_demand,
    ROUND(MIN(demand), 2) AS minimum_demand,
    ROUND(MAX(demand), 2) AS maximum_demand
FROM read_csv_auto(
    'data/processed/clean_train.csv'
)
GROUP BY item_id
ORDER BY total_demand DESC;


-- ================================================================
-- 3. DEMAND BY STORE
-- ================================================================

SELECT
    store_id,
    COUNT(*) AS records,
    ROUND(SUM(demand), 2) AS total_demand,
    ROUND(AVG(demand), 2) AS average_demand,
    ROUND(MIN(demand), 2) AS minimum_demand,
    ROUND(MAX(demand), 2) AS maximum_demand
FROM read_csv_auto(
    'data/processed/clean_train.csv'
)
GROUP BY store_id
ORDER BY total_demand DESC;


-- ================================================================
-- 4. DEMAND BY CATEGORY
-- ================================================================

SELECT
    cat_id,
    COUNT(*) AS records,
    ROUND(SUM(demand), 2) AS total_demand,
    ROUND(AVG(demand), 2) AS average_demand,
    ROUND(MIN(demand), 2) AS minimum_demand,
    ROUND(MAX(demand), 2) AS maximum_demand
FROM read_csv_auto(
    'data/processed/clean_train.csv'
)
GROUP BY cat_id
ORDER BY total_demand DESC;


-- ================================================================
-- 5. DEMAND BY DEPARTMENT
-- ================================================================

SELECT
    dept_id,
    COUNT(*) AS records,
    ROUND(SUM(demand), 2) AS total_demand,
    ROUND(AVG(demand), 2) AS average_demand
FROM read_csv_auto(
    'data/processed/clean_train.csv'
)
GROUP BY dept_id
ORDER BY total_demand DESC;


-- ================================================================
-- 6. DEMAND BY STATE
-- ================================================================

SELECT
    state_id,
    COUNT(*) AS records,
    ROUND(SUM(demand), 2) AS total_demand,
    ROUND(AVG(demand), 2) AS average_demand
FROM read_csv_auto(
    'data/processed/clean_train.csv'
)
GROUP BY state_id
ORDER BY total_demand DESC;


-- ================================================================
-- 7. MONTHLY DEMAND
-- ================================================================

SELECT
    DATE_TRUNC('month', CAST(date AS DATE)) AS month,
    ROUND(SUM(demand), 2) AS total_demand,
    ROUND(AVG(demand), 2) AS average_demand
FROM read_csv_auto(
    'data/processed/clean_train.csv'
)
GROUP BY month
ORDER BY month;


-- ================================================================
-- 8. DAILY DEMAND
-- ================================================================

SELECT
    CAST(date AS DATE) AS demand_date,
    ROUND(SUM(demand), 2) AS total_demand,
    ROUND(AVG(demand), 2) AS average_demand
FROM read_csv_auto(
    'data/processed/clean_train.csv'
)
GROUP BY demand_date
ORDER BY demand_date;


-- ================================================================
-- 9. ZERO-DEMAND ANALYSIS
-- ================================================================

SELECT
    COUNT(*) AS total_records,
    SUM(
        CASE
            WHEN demand = 0 THEN 1
            ELSE 0
        END
    ) AS zero_demand_records,
    ROUND(
        100.0
        * SUM(
            CASE
                WHEN demand = 0 THEN 1
                ELSE 0
            END
        )
        / COUNT(*),
        2
    ) AS zero_demand_percentage
FROM read_csv_auto(
    'data/processed/clean_train.csv'
);


-- ================================================================
-- 10. TOP PRODUCT-STORE COMBINATIONS
-- ================================================================

SELECT
    item_id,
    store_id,
    ROUND(SUM(demand), 2) AS total_demand,
    ROUND(AVG(demand), 2) AS average_demand,
    ROUND(MAX(demand), 2) AS maximum_demand
FROM read_csv_auto(
    'data/processed/clean_train.csv'
)
GROUP BY
    item_id,
    store_id
ORDER BY total_demand DESC
LIMIT 20;