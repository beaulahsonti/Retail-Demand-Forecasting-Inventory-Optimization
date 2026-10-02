"""
Validation utilities for forecasting model evaluation.
"""

import pandas as pd


REQUIRED_METRICS = ["MAE", "RMSE", "WAPE", "sMAPE"]


def validate_metrics(metrics):
    """Validate that all required evaluation metrics are available."""
    missing_metrics = [
        metric for metric in REQUIRED_METRICS
        if metric not in metrics
    ]

    if missing_metrics:
        raise ValueError(
            f"Missing evaluation metrics: {missing_metrics}"
        )

    return True


def validate_prediction_file(file_path):
    """Validate the basic structure of a prediction CSV file."""
    data = pd.read_csv(file_path)

    required_columns = ["id", "date", "demand"]

    missing_columns = [
        column for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing prediction columns: {missing_columns}"
        )

    if data.empty:
        raise ValueError("Prediction file is empty.")

    return True


def compare_models(model_metrics):
    """Return models sorted by MAE for metric inspection."""
    metrics_df = pd.DataFrame(model_metrics)

    if "MAE" not in metrics_df.columns:
        raise ValueError("MAE column is required for comparison.")

    return metrics_df.sort_values("MAE").reset_index(drop=True)


if __name__ == "__main__":
    print("RETAIL DEMAND FORECASTING - MODEL VALIDATION")
    print("-" * 55)

    sample_metrics = {
        "MAE": 0.8643,
        "RMSE": 1.5303,
        "WAPE": 84.96,
        "sMAPE": 137.47,
    }

    if validate_metrics(sample_metrics):
        print("Metric validation: PASSED")

    print("Required metrics:", ", ".join(REQUIRED_METRICS))