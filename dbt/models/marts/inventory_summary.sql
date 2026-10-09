SELECT
    item_id,
    store_id,
    average_demand,
    forecast_demand,
    safety_stock,
    lead_time_demand,
    reorder_point,
    recommended_inventory,
    inventory_priority
FROM {{ ref('stg_inventory') }}
ORDER BY reorder_point DESC