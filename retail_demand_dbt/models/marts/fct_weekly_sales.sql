-- ============================================================
-- MART MODEL: WEEKLY SALES
-- ============================================================
-- Purpose:
-- Aggregate daily sales into weekly demand at the
-- item-store level.
--
-- Grain:
-- One row per item-store-week.
--
-- Why:
-- Weekly demand provides a more stable time-series signal
-- for downstream forecasting and inventory planning.
-- ============================================================

SELECT
    sales_id,
    item_id,
    department_id,
    category_id,
    store_id,
    state_id,

    DATE_TRUNC('WEEK', sales_date) AS week_start_date,

    MIN(sales_date) AS first_sales_date,
    MAX(sales_date) AS last_sales_date,

    SUM(sales_units) AS weekly_sales_units,
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
    DATE_TRUNC('WEEK', sales_date)