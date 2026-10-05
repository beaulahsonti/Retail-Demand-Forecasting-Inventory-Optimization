-- ============================================================
-- DATA INTEGRITY TEST: DEMAND PROFILE GRAIN
-- ============================================================
-- Expected grain:
-- One row per sales_id.
--
-- Any returned row indicates duplicate demand profiles
-- for the same item-store sales series.
-- ============================================================

SELECT
    sales_id,
    COUNT(*) AS duplicate_count

FROM {{ ref('mart_demand_profile') }}

GROUP BY
    sales_id

HAVING COUNT(*) > 1
