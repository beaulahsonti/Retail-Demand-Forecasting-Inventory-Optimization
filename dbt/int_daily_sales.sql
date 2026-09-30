-- Intermediate model combining sales, calendar, and prices

SELECT
    s.*,
    c.date,
    c.wm_yr_wk,
    c.month,
    c.year,
    p.sell_price
FROM {{ ref('stg_sales') }} AS s
LEFT JOIN {{ ref('stg_calendar') }} AS c
    ON s.d = c.d
LEFT JOIN {{ ref('stg_prices') }} AS p
    ON s.store_id = p.store_id
    AND s.item_id = p.item_id
    AND c.wm_yr_wk = p.wm_yr_wk