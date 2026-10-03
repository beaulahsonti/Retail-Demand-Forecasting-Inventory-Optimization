-- ============================================================
-- STAGING MODEL: SALES WITH CALENDAR
-- ============================================================
-- Purpose:
-- Standardize the Week 1 curated sales and calendar dataset
-- into a clean staging model for downstream transformations.
--
-- Grain:
-- One row per item-store-day.
-- ============================================================

WITH source_data AS (

    SELECT
        ID,
        ITEM_ID,
        DEPT_ID,
        CAT_ID,
        STORE_ID,
        STATE_ID,
        DAY_ID,
        DATE,
        SALES,
        WEEKDAY,
        WDAY,
        MONTH,
        YEAR,
        EVENT_NAME_1,
        EVENT_TYPE_1,
        EVENT_NAME_2,
        EVENT_TYPE_2,
        SNAP_CA,
        SNAP_TX,
        SNAP_WI

    FROM {{ source('retail_demand', 'sales_with_calendar') }}

)

SELECT
    ID AS sales_id,
    ITEM_ID AS item_id,
    DEPT_ID AS department_id,
    CAT_ID AS category_id,
    STORE_ID AS store_id,
    STATE_ID AS state_id,
    DAY_ID AS day_id,
    DATE AS sales_date,
    SALES AS sales_units,
    WEEKDAY AS weekday_name,
    WDAY AS weekday_number,
    MONTH AS month_number,
    YEAR AS year_number,
    EVENT_NAME_1 AS event_name_1,
    EVENT_TYPE_1 AS event_type_1,
    EVENT_NAME_2 AS event_name_2,
    EVENT_TYPE_2 AS event_type_2,
    SNAP_CA AS snap_ca,
    SNAP_TX AS snap_tx,
    SNAP_WI AS snap_wi

FROM source_data