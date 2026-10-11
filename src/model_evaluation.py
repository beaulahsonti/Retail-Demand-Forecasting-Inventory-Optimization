import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
import os

BASELINE_PATH = "models/baseline_predictions.csv"
PROPHET_PATH = "models/prophet_predictions.csv"
LIGHTGBM_PATH = "models/lightgbm_predictions.csv"
OUTPUT_PATH = "models/model_comparison.csv"


def calculate_metrics(actual, prediction):
    mae = mean_absolute_error(actual, prediction)

    rmse = np.sqrt(
        mean_squared_error(actual, prediction)
    )

    return mae, rmse


def main():
    print("Loading model predictions...")

    # -----------------------------
    # Baseline
    # -----------------------------
    baseline = pd.read_csv(BASELINE_PATH)

    baseline_mae, baseline_rmse = calculate_metrics(
        baseline["sales"],
        baseline["prediction"]
    )

    # -----------------------------
    # Prophet
    # -----------------------------
    prophet = pd.read_csv(PROPHET_PATH)

    prophet_mae, prophet_rmse = calculate_metrics(
        prophet["actual"],
        prophet["prediction"]
    )

    # -----------------------------
    # LightGBM
    # -----------------------------
    lightgbm = pd.read_csv(LIGHTGBM_PATH)

    lightgbm_mae, lightgbm_rmse = calculate_metrics(
        lightgbm["sales"],
        lightgbm["prediction"]
    )

    # -----------------------------
    # Comparison table
    # -----------------------------
    results = pd.DataFrame({
        "model": [
            "Baseline (7-day lag)",
            "Prophet",
            "LightGBM"
        ],
        "MAE": [
            baseline_mae,
            prophet_mae,
            lightgbm_mae
        ],
        "RMSE": [
            baseline_rmse,
            prophet_rmse,
            lightgbm_rmse
        ]
    })

    results["MAE"] = results["MAE"].round(4)
    results["RMSE"] = results["RMSE"].round(4)

    print("\n========== MODEL COMPARISON ==========")
    print(results.to_string(index=False))

    os.makedirs("models", exist_ok=True)

    results.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(f"\nComparison saved to: {OUTPUT_PATH}")
    print("Model evaluation completed successfully.")


if __name__ == "__main__":
    main()