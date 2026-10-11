SELECT
    model,
    MAE AS mae,
    RMSE AS rmse
FROM {{ source('retail', 'model_comparison') }}