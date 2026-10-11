SELECT
    item_id,
    store_id,
    average_demand,
    demand_std,
    forecast_demand,
    safety_stock,
    lead_time_demand,
    reorder_point,
    recommended_inventory,
    inventory_buffer_ratio,
    inventory_priority
FROM {{ source('retail', 'inventory_analysis') }}