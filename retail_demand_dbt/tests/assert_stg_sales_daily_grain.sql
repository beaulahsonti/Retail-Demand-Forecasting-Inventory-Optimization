-- ============================================================
-- DATA INTEGRITY TEST: DAILY SALES GRAIN
-- ============================================================
-- Purpose:
-- Verify that each item-store-day observation is unique.
--
-- Expected grain:
-- One row per sales_id + day_id combination.
--
-- Why:
-- sales_id identifies the item-store sales series and therefore
-- repeats across multiple days. The combination of sales_id and
-- day_id should uniquely identify each daily observation.
--
-- Test logic:
-- If this query returns any rows, duplicate item-store-day
-- observations exist and the test should fail.
-- ============================================================

SELECT
    sales_id,
    day_id,
    COUNT(*) AS duplicate_count

FROM {{ ref('stg_sales_with_calendar') }}

GROUP BY
    sales_id,
    day_id

HAVING COUNT(*) > 1