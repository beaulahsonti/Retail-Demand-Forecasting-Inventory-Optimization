SELECT
    item_id,
    store_id,
    ROUND(AVG(average_demand), 2) AS average_demand,
    ROUND(SUM(forecast_demand), 2) AS forecast_demand,
    ROUND(SUM(safety_stock), 2) AS safety_stock,
    ROUND(SUM(lead_time_demand), 2) AS lead_time_demand,
    ROUND(SUM(reorder_point), 2) AS reorder_point,
    ROUND(SUM(recommended_inventory), 2) AS recommended_inventory,
    inventory_priority
FROM inventory_analysis
GROUP BY
    item_id,
    store_id,
    inventory_priority
ORDER BY reorder_point DESC;