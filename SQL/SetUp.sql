-- ============================================================
-- 1. VERIFY RAW_CALENDAR ROW COUNT
-- ============================================================
-- Objective:
-- Verify that the calendar dataset was successfully loaded
-- into Snowflake.
--
-- Expected result:
-- 1,969 rows.
--
-- Why:
-- This confirms that the complete calendar dataset was
-- successfully ingested before performing transformations.

SELECT COUNT(*)
FROM RETAIL_DEMAND.PUBLIC.RAW_CALENDAR;


-- ============================================================
-- 2. VERIFY RAW_SALES_TRAIN_VALIDATION ROW COUNT
-- ============================================================
-- Objective:
-- Verify that the M5 sales validation dataset was completely
-- loaded into Snowflake.
--
-- Expected result:
-- 30,490 rows.
--
-- Why:
-- This confirms that the sales data was successfully ingested
-- before beginning data transformation and analysis.

SELECT COUNT(*)
FROM RETAIL_DEMAND.PUBLIC.RAW_SALES_TRAIN_VALIDATION;


-- ============================================================
-- 3. VERIFY RAW_SELL_PRICES ROW COUNT
-- ============================================================
-- Objective:
-- Verify that the complete sell-price dataset was loaded.
--
-- Expected result:
-- 6,841,121 rows.
--
-- Why:
-- The sell-price data will later be joined with the sales data
-- to incorporate pricing information into demand analysis.

SELECT COUNT(*)
FROM RETAIL_DEMAND.PUBLIC.RAW_SELL_PRICES;


-- ============================================================
-- 4. VERIFY RAW_SALES_TRAIN_EVALUATION ROW COUNT
-- ============================================================
-- Objective:
-- Verify that the M5 evaluation sales dataset was successfully
-- loaded into Snowflake.
--
-- Expected result:
-- 30,490 rows.
--
-- Why:
-- This confirms that the evaluation dataset is available for
-- later forecasting and validation tasks.

SELECT COUNT(*)
FROM RETAIL_DEMAND.PUBLIC.RAW_SALES_TRAIN_EVALUATION;


-- ============================================================
-- 5. INSPECT RAW SALES TABLE STRUCTURE
-- ============================================================
-- Objective:
-- Inspect the column names and data types of the raw sales
-- validation table before performing transformations.
--
-- Why:
-- Understanding the schema helps us identify product, store,
-- category, and daily sales fields before restructuring the data.

DESCRIBE TABLE RETAIL_DEMAND.PUBLIC.RAW_SALES_TRAIN_VALIDATION;


-- ============================================================
-- 6. INSPECT SAMPLE SALES RECORDS
-- ============================================================
-- Objective:
-- Examine a small sample of the raw sales data.
--
-- Why:
-- This helps us understand how item, store, and daily sales
-- information are represented in the raw dataset.
--
-- Observation:
-- The sales data is stored in wide format, with daily sales
-- represented by columns such as D_1, D_2, D_3, etc.

SELECT *
FROM RETAIL_DEMAND.PUBLIC.RAW_SALES_TRAIN_VALIDATION
LIMIT 5;


-- ============================================================
-- 7. INSPECT CALENDAR DATA
-- ============================================================
-- Objective:
-- Examine the calendar table to understand how the M5 day
-- identifiers correspond to actual dates.
--
-- Why:
-- The sales table uses D_1, D_2, D_3, etc., while the calendar
-- table provides the corresponding dates and calendar features.
-- This mapping will be required when transforming the sales data
-- into a time-series structure.

SELECT *
FROM RETAIL_DEMAND.PUBLIC.RAW_CALENDAR
LIMIT 10;

-- ============================================================
-- 8. TEST WIDE-TO-LONG SALES TRANSFORMATION
-- ============================================================
-- Objective:
-- Convert the daily sales columns from wide format into rows.
--
-- Why:
-- Time-series analysis requires each observation to have a
-- corresponding time period and sales value.
--
-- The raw M5 data stores each day as a separate column
-- (D_1, D_2, D_3, ...). UNPIVOT converts these columns into
-- two columns: DAY_ID and SALES.

SELECT
    ID,
    ITEM_ID,
    DEPT_ID,
    CAT_ID,
    STORE_ID,
    STATE_ID,
    DAY_ID,
    SALES
FROM RETAIL_DEMAND.PUBLIC.RAW_SALES_TRAIN_VALIDATION
UNPIVOT (
    SALES FOR DAY_ID IN (
        D_1, D_2, D_3, D_4, D_5
    )
)
LIMIT 20;

-- ============================================================
-- 9. FULL WIDE-TO-LONG SALES TRANSFORMATION
-- ============================================================
-- Objective:
-- Convert all daily sales columns from wide format into rows.
--
-- Why:
-- Each D_ column represents one day. Converting these columns
-- into rows creates a time-series structure that is easier to
-- analyze, join with calendar data, and use for forecasting.

SELECT
    ID,
    ITEM_ID,
    DEPT_ID,
    CAT_ID,
    STORE_ID,
    STATE_ID,
    DAY_ID,
    SALES
FROM RETAIL_DEMAND.PUBLIC.RAW_SALES_TRAIN_VALIDATION
UNPIVOT (
    SALES FOR DAY_ID IN (
        D_1, D_2, D_3, D_4, D_5,
        D_6, D_7, D_8, D_9, D_10
    )
)
LIMIT 20;

-- ============================================================
-- 10. CHECK NUMBER OF DAILY SALES COLUMNS
-- ============================================================
-- Objective:
-- Confirm the range of daily sales columns available in the
-- raw validation dataset.
--
-- Why:
-- The M5 sales data stores each day as a separate column.
-- Before creating the full long-format table, we need to
-- confirm the last available day column.

SELECT COUNT(*) AS TOTAL_COLUMNS
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'PUBLIC'
  AND TABLE_NAME = 'RAW_SALES_TRAIN_VALIDATION'
  AND COLUMN_NAME LIKE 'D_%';

  SELECT COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'PUBLIC'
  AND TABLE_NAME = 'RAW_SALES_TRAIN_VALIDATION'
  AND COLUMN_NAME LIKE 'D_%'
ORDER BY ORDINAL_POSITION DESC
LIMIT 5;

SELECT LISTAGG(COLUMN_NAME, ', ')
       WITHIN GROUP (ORDER BY ORDINAL_POSITION) AS DAY_COLUMNS
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'PUBLIC'
  AND TABLE_NAME = 'RAW_SALES_TRAIN_VALIDATION'
  AND REGEXP_LIKE(COLUMN_NAME, '^D_[0-9]+$');

  -- ============================================================
-- 11. CHECK NULL VALUES IN SALES IDENTIFIER COLUMNS
-- ============================================================
-- Objective:
-- Check whether important identifier columns contain NULL
-- values in the raw sales dataset.
--
-- Why:
-- ITEM_ID, STORE_ID, DEPT_ID, CAT_ID, and STATE_ID are required
-- to correctly identify each product and store.
--
-- Expected result:
-- These identifier columns should contain no NULL values.
--
-- ============================================================

SELECT
    COUNT_IF(ID IS NULL)       AS NULL_ID,
    COUNT_IF(ITEM_ID IS NULL)  AS NULL_ITEM_ID,
    COUNT_IF(DEPT_ID IS NULL)  AS NULL_DEPT_ID,
    COUNT_IF(CAT_ID IS NULL)   AS NULL_CAT_ID,
    COUNT_IF(STORE_ID IS NULL) AS NULL_STORE_ID,
    COUNT_IF(STATE_ID IS NULL) AS NULL_STATE_ID
FROM RETAIL_DEMAND.PUBLIC.RAW_SALES_TRAIN_VALIDATION;