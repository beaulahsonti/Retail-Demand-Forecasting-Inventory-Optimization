-- ============================================================
-- MART MODEL: DEMAND PROFILE
-- ============================================================
-- Purpose:
-- Create an item-store level demand profile that summarizes
-- historical demand behavior for downstream forecasting and
-- inventory optimization.
--
-- Grain:
-- One row per item-store sales series.
--
-- Creative/project-quality component:
-- This model moves beyond basic time aggregation by converting
-- historical daily demand into reusable demand characteristics.
-- These features can later support demand segmentation,
-- forecasting, safety-stock analysis, and reorder-point logic.
-- ============================================================

SELECT
    sales_id,
    item_id,
    department_id,
    category_id,
    store_id,
    state_id,

    COUNT(*) AS observation_days,

    SUM(sales_units) AS total_sales_units,

    AVG(sales_units) AS avg_daily_demand,

    STDDEV(sales_units) AS demand_stddev,

    MAX(sales_units) AS peak_daily_demand,

    COUNT_IF(sales_units > 0) AS active_sales_days,

    COUNT_IF(sales_units = 0) AS zero_sales_days,

    ROUND(
        COUNT_IF(sales_units > 0) / NULLIF(COUNT(*), 0),
        4
    ) AS demand_activity_rate,

    ROUND(
        STDDEV(sales_units) / NULLIF(AVG(sales_units), 0),
        4
    ) AS demand_coefficient_of_variation

FROM {{ ref('int_daily_sales') }}

GROUP BY
    sales_id,
    item_id,
    department_id,
    category_id,
    store_id,
    state_id