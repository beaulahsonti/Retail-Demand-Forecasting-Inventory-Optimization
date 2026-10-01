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

-- ============================================================
-- 12. CHECK SALES VALUES FOR NULL AND NEGATIVE VALUES
-- ============================================================
-- Objective:
-- Check whether the raw sales data contains NULL or negative
-- sales values.
--
-- Why:
-- Sales quantities should not be negative.
-- NULL values indicate missing observations.
--
-- ============================================================

SELECT
    COUNT(*) AS TOTAL_SALES_RECORDS,

    COUNT_IF(SALES IS NULL) AS NULL_SALES,

    COUNT_IF(SALES < 0) AS NEGATIVE_SALES,

    MIN(SALES) AS MIN_SALES,

    MAX(SALES) AS MAX_SALES

FROM RETAIL_DEMAND.PUBLIC.RAW_SALES_TRAIN_VALIDATION
UNPIVOT (
    SALES FOR DAY_ID IN (
        D_1, D_2, D_3, D_4, D_5
    )
);

-- ============================================================
-- 13. GENERATE COMPLETE UNPIVOT COLUMN LIST
-- ============================================================
-- Objective:
-- Generate the complete list of daily sales columns required
-- for the UNPIVOT transformation.
--
-- Expected result:
-- D_1, D_2, D_3, ... D_1913
--
-- Why:
-- The raw M5 sales table stores each day as a separate column.
-- We need the complete list to convert the wide sales data
-- into long format.
-- ============================================================

SELECT
    LISTAGG(COLUMN_NAME, ', ')
        WITHIN GROUP (ORDER BY ORDINAL_POSITION) AS DAY_COLUMNS
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'PUBLIC'
  AND TABLE_NAME = 'RAW_SALES_TRAIN_VALIDATION'
  AND REGEXP_LIKE(COLUMN_NAME, '^D_[0-9]+$');

  -- ============================================================
-- 14. GENERATE FULL UNPIVOT SQL
-- ============================================================

SELECT
    'SELECT ID, ITEM_ID, DEPT_ID, CAT_ID, STORE_ID, STATE_ID, DAY_ID, SALES
FROM RETAIL_DEMAND.PUBLIC.RAW_SALES_TRAIN_VALIDATION
UNPIVOT (
    SALES FOR DAY_ID IN (' ||
    LISTAGG(COLUMN_NAME, ', ')
        WITHIN GROUP (ORDER BY ORDINAL_POSITION)
    || ')
);' AS UNPIVOT_QUERY
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'PUBLIC'
  AND TABLE_NAME = 'RAW_SALES_TRAIN_VALIDATION'
  AND REGEXP_LIKE(COLUMN_NAME, '^D_[0-9]+$');

  -- ============================================================
-- 15. FULL SALES DATA QUALITY CHECK
-- ============================================================
-- Objective:
-- Check NULL, negative, minimum, and maximum sales values
-- across all 1,913 days.
--
-- Why:
-- The previous check covered only D_1 to D_5.
-- This checks the complete sales history.
-- ============================================================

SELECT
    COUNT(*) AS TOTAL_SALES_RECORDS,
    COUNT_IF(SALES IS NULL) AS NULL_SALES,
    COUNT_IF(SALES < 0) AS NEGATIVE_SALES,
    MIN(SALES) AS MIN_SALES,
    MAX(SALES) AS MAX_SALES

FROM RETAIL_DEMAND.PUBLIC.RAW_SALES_TRAIN_VALIDATION

UNPIVOT (
    SALES FOR DAY_ID IN (
        D_1, D_2, D_3
        -- paste the complete D_1 → D_1913 list here
    )
);

SELECT
    'CREATE OR REPLACE TABLE RETAIL_DEMAND.PUBLIC.SALES_LONG AS
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
UNPIVOT INCLUDE NULLS (
    SALES FOR DAY_ID IN (' ||
    LISTAGG(COLUMN_NAME, ', ')
        WITHIN GROUP (ORDER BY ORDINAL_POSITION)
    || ')
);' AS CREATE_LONG_TABLE_QUERY
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'PUBLIC'
  AND TABLE_NAME = 'RAW_SALES_TRAIN_VALIDATION'
  AND REGEXP_LIKE(COLUMN_NAME, '^D_[0-9]+$');

SELECT CURRENT_DATABASE(), CURRENT_SCHEMA(), CURRENT_ROLE();
SHOW TABLES IN SCHEMA RETAIL_DEMAND.PUBLIC;

-- ============================================================
-- 16. TEST LONG-FORMAT SALES TABLE CREATION
-- ============================================================
-- Objective:
-- Verify that the UNPIVOT transformation can be used to create
-- a new long-format table successfully.
--
-- Why:
-- The full transformation contains 1,913 daily columns.
-- We first test the table-creation logic using five days
-- before running the complete transformation.
--
-- ============================================================

CREATE OR REPLACE TABLE RETAIL_DEMAND.PUBLIC.SALES_LONG_TEST AS

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

UNPIVOT INCLUDE NULLS (
    SALES FOR DAY_ID IN (
        D_1,
        D_2,
        D_3,
        D_4,
        D_5
    )
);

SELECT COUNT(*) AS TOTAL_ROWS
FROM RETAIL_DEMAND.PUBLIC.SALES_LONG_TEST;

-- ============================================================
-- 17. GENERATE COMPLETE SALES_LONG CREATION QUERY
-- ============================================================

SELECT
    'CREATE OR REPLACE TABLE RETAIL_DEMAND.PUBLIC.SALES_LONG AS
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
UNPIVOT INCLUDE NULLS (
    SALES FOR DAY_ID IN (' ||
    LISTAGG(
        COLUMN_NAME,
        ', '
    ) WITHIN GROUP (
        ORDER BY ORDINAL_POSITION
    ) ||
    ')
);' AS CREATE_QUERY
FROM RETAIL_DEMAND.INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'PUBLIC'
  AND TABLE_NAME = 'RAW_SALES_TRAIN_VALIDATION'
  AND REGEXP_LIKE(COLUMN_NAME, '^D_[0-9]+$');

  SELECT COUNT(*) AS TOTAL_ROWS
FROM RETAIL_DEMAND.PUBLIC.SALES_LONG;

DECLARE
    DAY_COLUMNS VARCHAR;
    CREATE_SQL VARCHAR;
BEGIN

    SELECT LISTAGG(COLUMN_NAME, ', ')
           WITHIN GROUP (ORDER BY ORDINAL_POSITION)
    INTO :DAY_COLUMNS
    FROM RETAIL_DEMAND.INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 'PUBLIC'
      AND TABLE_NAME = 'RAW_SALES_TRAIN_VALIDATION'
      AND REGEXP_LIKE(COLUMN_NAME, '^D_[0-9]+$');

    CREATE_SQL :=
        'CREATE OR REPLACE TABLE RETAIL_DEMAND.PUBLIC.SALES_LONG AS
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
         UNPIVOT INCLUDE NULLS (
             SALES FOR DAY_ID IN (' || DAY_COLUMNS || ')
         )';

    EXECUTE IMMEDIATE :CREATE_SQL;

END;

SELECT COUNT(*) AS TOTAL_ROWS
FROM RETAIL_DEMAND.PUBLIC.SALES_LONG;

-- ============================================================
-- 18. VERIFY SALES_LONG TRANSFORMATION
-- ============================================================
-- Objective:
-- Confirm that all 1,913 daily columns were converted into
-- rows and that the DAY_ID range is complete.

SELECT
    MIN(DAY_ID) AS FIRST_DAY,
    MAX(DAY_ID) AS LAST_DAY,
    COUNT(DISTINCT DAY_ID) AS UNIQUE_DAYS
FROM RETAIL_DEMAND.PUBLIC.SALES_LONG;

SELECT *
FROM RETAIL_DEMAND.PUBLIC.SALES_LONG
LIMIT 10;


SELECT DISTINCT DAY_ID
FROM RETAIL_DEMAND.PUBLIC.SALES_LONG
LIMIT 10;
SELECT
    D,
    DATE
FROM RETAIL_DEMAND.PUBLIC.RAW_CALENDAR
LIMIT 10;

SELECT
    s.DAY_ID,
    c.DATE,
    c.WEEKDAY,
    c.MONTH,
    c.YEAR
FROM RETAIL_DEMAND.PUBLIC.SALES_LONG AS s
JOIN RETAIL_DEMAND.PUBLIC.RAW_CALENDAR AS c
    ON LOWER(s.DAY_ID) = LOWER(c.D)
LIMIT 10;

SELECT
    COUNT(*) AS UNMATCHED_ROWS
FROM RETAIL_DEMAND.PUBLIC.SALES_LONG AS s
LEFT JOIN RETAIL_DEMAND.PUBLIC.RAW_CALENDAR AS c
    ON LOWER(s.DAY_ID) = LOWER(c.D)
WHERE c.D IS NULL;

-- ============================================================
-- FINAL WEEK 1 TABLE: SALES WITH CALENDAR INFORMATION
-- ============================================================
-- Objective:
-- Combine the transformed long-format sales data with the
-- calendar information so that each sales record has its
-- corresponding actual date and calendar attributes.
--
-- Why:
-- SALES_LONG contains DAY_ID values such as D_1, D_2, etc.
-- RAW_CALENDAR maps these day IDs to actual dates and provides
-- useful time-related features such as weekday, month, year,
-- events, and SNAP indicators.
--
-- The LOWER() function is used because:
-- SALES_LONG.DAY_ID = D_1
-- RAW_CALENDAR.D   = d_1
-- Snowflake string comparisons are case-sensitive.
--
-- Expected row count:
-- 58,327,370

CREATE OR REPLACE TABLE RETAIL_DEMAND.PUBLIC.SALES_WITH_CALENDAR AS
SELECT
    s.ID,
    s.ITEM_ID,
    s.DEPT_ID,
    s.CAT_ID,
    s.STORE_ID,
    s.STATE_ID,
    s.DAY_ID,
    c.DATE,
    s.SALES,
    c.WEEKDAY,
    c.WDAY,
    c.MONTH,
    c.YEAR,
    c.EVENT_NAME_1,
    c.EVENT_TYPE_1,
    c.EVENT_NAME_2,
    c.EVENT_TYPE_2,
    c.SNAP_CA,
    c.SNAP_TX,
    c.SNAP_WI
FROM RETAIL_DEMAND.PUBLIC.SALES_LONG AS s
LEFT JOIN RETAIL_DEMAND.PUBLIC.RAW_CALENDAR AS c
    ON LOWER(s.DAY_ID) = LOWER(c.D);

    SELECT COUNT(*)
FROM RETAIL_DEMAND.PUBLIC.SALES_WITH_CALENDAR;