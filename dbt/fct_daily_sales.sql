-- Final daily sales analytical model

SELECT
    date,
    store_id,
    item_id,
    SUM(sales) AS total_sales,
    AVG(sell_price) AS average_price
FROM {{ ref('int_daily_sales') }}
GROUP BY
    date,
    store_id,
    item_id