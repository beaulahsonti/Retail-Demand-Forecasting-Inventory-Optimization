-- ============================================================
-- INTERMEDIATE MODEL: DAILY SALES
-- ============================================================
-- Purpose:
-- Prepare a clean daily-level sales dataset from the staging
-- layer for downstream weekly/monthly aggregations.
--
-- Grain:
-- One row per item-store-day observation.
--
-- This model intentionally keeps the data at daily grain.
-- Aggregation into weekly and monthly views will happen in
-- downstream mart models.
-- ============================================================

SELECT
    sales_id,
    item_id,
    department_id,
    category_id,
    store_id,
    state_id,
    day_id,
    sales_date,
    sales_units,
    weekday_name,
    weekday_number,
    month_number,
    year_number,
    event_name_1,
    event_type_1,
    event_name_2,
    event_type_2,
    snap_ca,
    snap_tx,
    snap_wi

FROM {{ ref('stg_sales_with_calendar') }}