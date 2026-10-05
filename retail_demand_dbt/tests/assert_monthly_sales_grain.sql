-- ============================================================
-- DATA INTEGRITY TEST: MONTHLY SALES GRAIN
-- ============================================================
-- Expected grain:
-- One row per sales_id + month_start_date.
--
-- Any returned row indicates duplicate monthly observations.
-- ============================================================

SELECT
    sales_id,
    month_start_date,
    COUNT(*) AS duplicate_count

FROM {{ ref('fct_monthly_sales') }}

GROUP BY
    sales_id,
    month_start_date

HAVING COUNT(*) > 1