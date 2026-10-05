-- ============================================================
-- DATA INTEGRITY TEST: WEEKLY SALES GRAIN
-- ============================================================
-- Expected grain:
-- One row per sales_id + week_start_date.
--
-- Any returned row indicates duplicate weekly observations.
-- ============================================================

SELECT
    sales_id,
    week_start_date,
    COUNT(*) AS duplicate_count

FROM {{ ref('fct_weekly_sales') }}

GROUP BY
    sales_id,
    week_start_date

HAVING COUNT(*) > 1