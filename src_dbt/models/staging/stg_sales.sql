/* 
  Week 2: Day 1-3 Core Data Transformation
  Maps and unpivots the core transactional historical store sales demand matrices.
*/

WITH source_sales_matrix AS (
    SELECT 
        LOWER(TRIM(id)) AS long_series_id,
        LOWER(TRIM(item_id)) AS item_id,
        LOWER(TRIM(dept_id)) AS department_id,
        LOWER(TRIM(cat_id)) AS category_id,
        LOWER(TRIM(store_id)) AS store_id,
        LOWER(TRIM(state_id)) AS state_id,
        -- Select all trailing daily volume matrix strings dynamically
        * EXCLUDE (id, item_id, dept_id, cat_id, store_id, state_id)
    FROM src_sqlite.sales_train_validation
)

SELECT * FROM source_sales_matrix
