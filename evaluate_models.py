import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error


def calculate_metrics(actual, predicted):
    actual = np.array(actual)
    predicted = np.array(predicted)

    mae = mean_absolute_error(actual, predicted)

    rmse = np.sqrt(
        mean_squared_error(actual, predicted)
    )

    # Avoid division by zero for MAPE
    non_zero = actual != 0

    if non_zero.sum() > 0:
        mape = np.mean(
            np.abs(
                (actual[non_zero] - predicted[non_zero])
                / actual[non_zero]
            )
        ) * 100
    else:
        mape = np.nan

    return mae, rmse, mape


results = []


# -------------------------------------------------
# 1. BASELINE MODEL
# -------------------------------------------------

baseline_file = "data/processed/baseline_forecast.csv"

baseline = pd.read_csv(
    baseline_file,
    low_memory=False
)

baseline = baseline.dropna(
    subset=["sales", "baseline_forecast"]
)

mae, rmse, mape = calculate_metrics(
    baseline["sales"],
    baseline["baseline_forecast"]
)

results.append({
    "model": "Baseline",
    "MAE": mae,
    "RMSE": rmse,
    "MAPE": mape
})


# -------------------------------------------------
# 2. LIGHTGBM MODEL
# -------------------------------------------------

lightgbm_file = "data/processed/lightgbm_forecast.csv"

lightgbm_df = pd.read_csv(
    lightgbm_file,
    low_memory=False
)

lightgbm_df = lightgbm_df.dropna(
    subset=["sales", "predicted_sales"]
)

mae, rmse, mape = calculate_metrics(
    lightgbm_df["sales"],
    lightgbm_df["predicted_sales"]
)

results.append({
    "model": "LightGBM",
    "MAE": mae,
    "RMSE": rmse,
    "MAPE": mape
})


# -------------------------------------------------
# CREATE EVALUATION TABLE
# -------------------------------------------------

evaluation = pd.DataFrame(results)

evaluation = evaluation.sort_values(
    by="MAE"
)

output_file = "data/processed/model_evaluation.csv"

evaluation.to_csv(
    output_file,
    index=False
)

print("Model evaluation completed.")
print()
print(evaluation)
print()
print("Saved to:", output_file)