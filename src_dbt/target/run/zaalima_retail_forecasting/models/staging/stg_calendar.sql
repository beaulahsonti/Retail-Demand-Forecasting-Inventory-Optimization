
  
  create view "zaalima_warehouse"."main"."stg_calendar__dbt_tmp" as (
    /* 
  Week 2: Day 1-3 Core Data Transformation
  Transforms the calendar records cleanly from the attached SQLite database source.
*/

WITH source_calendar_matrix AS (
    SELECT 
        LOWER(TRIM(d)) AS date_day_id,
        CAST(wm_yr_wk AS INTEGER) AS walmart_year_week,
        LOWER(TRIM(weekday)) AS weekday_name,
        CAST(wday AS INTEGER) AS weekday_number,
        CAST(month AS INTEGER) AS calendar_month,
        CAST(year AS INTEGER) AS calendar_year,
        LOWER(TRIM(event_name_1)) AS event_primary_name,
        LOWER(TRIM(event_type_1)) AS event_primary_type,
        CAST(snap_ca AS BOOLEAN) AS is_snap_eligible_ca,
        CAST(snap_tx AS BOOLEAN) AS is_snap_eligible_tx,
        CAST(snap_wi AS BOOLEAN) AS is_snap_eligible_wi
    FROM src_sqlite.calendar
)

SELECT * FROM source_calendar_matrix
  );
