SELECT
    model,
    ROUND(MAE, 4) AS mae,
    ROUND(RMSE, 4) AS rmse
FROM model_comparison
ORDER BY mae ASC;