from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "forecast_validation.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "forecasts"
REPORT_DIR = PROJECT_ROOT / "reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def wape(actual, predicted):
    """Weighted Absolute Percentage Error."""
    denominator = np.abs(actual).sum()

    if denominator == 0:
        return np.nan

    return np.abs(actual - predicted).sum() / denominator * 100


def smape(actual, predicted):
    """Symmetric Mean Absolute Percentage Error."""
    denominator = np.abs(actual) + np.abs(predicted)

    valid = denominator != 0

    if valid.sum() == 0:
        return np.nan

    return (
        np.mean(
            2
            * np.abs(actual[valid] - predicted[valid])
            / denominator[valid]
        )
        * 100
    )


def main():

    print("=" * 70)
    print("BASELINE DEMAND FORECAST")
    print("=" * 70)

    # Load validation data
    df = pd.read_csv(INPUT_FILE)

    df["date"] = pd.to_datetime(df["date"])

    # 7-day lag becomes the baseline prediction
    df["prediction"] = df["lag_7"]

    # Remove any remaining missing baseline values
    df = df.dropna(
        subset=["demand", "prediction"]
    ).copy()

    actual = df["demand"].to_numpy()
    predicted = df["prediction"].to_numpy()

    # ---------------------------------------------------------
    # Evaluation metrics
    # ---------------------------------------------------------

    mae = mean_absolute_error(
        actual,
        predicted
    )

    rmse = np.sqrt(
        mean_squared_error(
            actual,
            predicted
        )
    )

    wape_score = wape(
        actual,
        predicted
    )

    smape_score = smape(
        actual,
        predicted
    )

    # ---------------------------------------------------------
    # Print results
    # ---------------------------------------------------------

    print("\nBaseline: 7-day lag demand")

    print(f"\nValidation rows: {len(df):,}")

    print("\nBaseline metrics:")
    print(f"MAE:   {mae:.4f}")
    print(f"RMSE:  {rmse:.4f}")
    print(f"WAPE:  {wape_score:.2f}%")
    print(f"sMAPE: {smape_score:.2f}%")

    # ---------------------------------------------------------
    # Save predictions
    # ---------------------------------------------------------

    prediction_columns = [
        "id",
        "item_id",
        "store_id",
        "date",
        "demand",
        "prediction"
    ]

    predictions = df[
        prediction_columns
    ].copy()

    prediction_file = (
        OUTPUT_DIR /
        "baseline_predictions.csv"
    )

    predictions.to_csv(
        prediction_file,
        index=False
    )

    # ---------------------------------------------------------
    # Save metrics
    # ---------------------------------------------------------

    metrics = pd.DataFrame({
        "model": ["7_day_lag_baseline"],
        "MAE": [mae],
        "RMSE": [rmse],
        "WAPE": [wape_score],
        "sMAPE": [smape_score]
    })

    metrics_file = (
        REPORT_DIR /
        "baseline_metrics.csv"
    )

    metrics.to_csv(
        metrics_file,
        index=False
    )

    print("\nSaved files:")
    print(prediction_file)
    print(metrics_file)

    print("\nBaseline evaluation completed successfully.")


if __name__ == "__main__":
    main()