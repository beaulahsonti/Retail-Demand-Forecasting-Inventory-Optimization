
    

    create  table
      "zaalima_warehouse"."main"."fct_daily_retail_sales__dbt_tmp"
  
    
    as (
      /*
  Week 2: Day 4-7 Final Analytics Data Mart
  Unpivots the horizontal daily sales columns and merges dimensions
  from calendar and pricing arrays into a flat, production-ready ML matrix.
*/

WITH unpivoted_sales_matrix AS (
    -- Dynamically unpivot daily columns (d_1, d_2, etc.) into an optimized long-series format
    SELECT 
        store_id,
        item_id,
        -- Corrected raw column mappings matching the warehouse bindings
        cat_id AS category_id,
        dept_id AS department_id,
        state_id,
        CAST(regexp_replace(unpivoted_col_name, '^d_', '') AS INTEGER) AS day_sequence_number,
        CAST(sales_volume AS INTEGER) AS daily_sales_units
    FROM src_sqlite.sales_train_validation
    UNPIVOT (
        sales_volume FOR unpivoted_col_name IN (
            -- Dynamically captures all daily transactional string columns
            COLUMNS(* EXCLUDE (id, item_id, dept_id, cat_id, store_id, state_id))
        )
    )
),

final_joined_analytics_mart AS (
    SELECT 
        -- Core dimensions
        s.store_id,
        s.item_id,
        s.category_id,
        s.department_id,
        s.state_id,
        
        -- Time-series alignments
        c.walmart_year_week,
        c.weekday_name,
        c.weekday_number,
        c.calendar_month,
        c.calendar_year,
        
        -- Categorical event features
        c.event_primary_name,
        c.event_primary_type,
        c.is_snap_eligible_ca,
        c.is_snap_eligible_tx,
        c.is_snap_eligible_wi,
        
        -- Transactional units and yield evaluation fields
        s.daily_sales_units,
        COALESCE(p.item_sell_price, 0.0) AS item_sell_price,
        (s.daily_sales_units * COALESCE(p.item_sell_price, 0.0)) AS daily_gross_revenue_usd
    FROM unpivoted_sales_matrix s
    -- Link directly to your optimized staging views
    INNER JOIN "zaalima_warehouse"."main"."stg_calendar" c 
        ON s.day_sequence_number = CAST(regexp_replace(c.date_day_id, '^d_', '') AS INTEGER)
    LEFT JOIN "zaalima_warehouse"."main"."stg_prices" p 
        ON s.item_id = p.item_id 
        AND s.store_id = p.store_id 
        AND c.walmart_year_week = p.walmart_year_week
)

SELECT * FROM final_joined_analytics_mart
    );
    
  