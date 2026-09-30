
  
  create view "zaalima_warehouse"."main"."stg_prices__dbt_tmp" as (
    /* 
  Week 2: Day 1-3 Core Data Transformation
  Maps and sanitizes the historical item pricing records from the attached database.
*/

WITH source_prices_matrix AS (
    SELECT 
        LOWER(TRIM(store_id)) AS store_id,
        LOWER(TRIM(item_id)) AS item_id,
        CAST(wm_yr_wk AS INTEGER) AS walmart_year_week,
        CAST(sell_price AS DOUBLE) AS item_sell_price
    FROM src_sqlite.sell_prices
)

SELECT * FROM source_prices_matrix
  );
