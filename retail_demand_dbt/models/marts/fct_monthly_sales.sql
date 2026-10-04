-- ============================================================
-- MART MODEL: MONTHLY SALES
-- ============================================================
-- Purpose:
-- Aggregate daily sales into monthly demand at the
-- item-store level.
--
-- Grain:
-- One row per item-store-month.
--
-- Why:
-- Monthly demand provides a higher-level view of sales
-- patterns and supports longer-term forecasting and
-- inventory planning.
-- ============================================================

SELECT
    sales_id,
    item_id,
    department_id,
    category_id,
    store_id,
    state_id,

    DATE_TRUNC('MONTH', sales_date) AS month_start_date,

    MIN(sales_date) AS first_sales_date,
    MAX(sales_date) AS last_sales_date,

    SUM(sales_units) AS monthly_sales_units,
    AVG(sales_units) AS avg_daily_sales_units,
    COUNT(*) AS selling_days

FROM {{ ref('int_daily_sales') }}

GROUP BY
    sales_id,
    item_id,
    department_id,
    category_id,
    store_id,
    state_id,
    DATE_TRUNC('MONTH', sales_date)