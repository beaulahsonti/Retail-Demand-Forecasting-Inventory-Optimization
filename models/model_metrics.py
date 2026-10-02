"""
Model evaluation metrics for the Retail Demand Forecasting project.
"""

import pandas as pd


METRIC_COLUMNS = ["MAE", "RMSE", "WAPE", "sMAPE"]


def load_model_metrics(file_path):
    """Load model comparison metrics from a CSV file."""
    metrics = pd.read_csv(file_path)

    missing_columns = [
        column for column in METRIC_COLUMNS
        if column not in metrics.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing metric columns: {missing_columns}"
        )

    return metrics


def get_best_by_metric(metrics, metric="MAE"):
    """Return the model with the lowest value for the selected metric."""
    if metric not in metrics.columns:
        raise ValueError(f"Metric not found: {metric}")

    return metrics.loc[metrics[metric].idxmin()]


def summarize_metrics(metrics):
    """Return basic statistics for the evaluation metrics."""
    return metrics[METRIC_COLUMNS].describe()


if __name__ == "__main__":
    print("RETAIL DEMAND FORECASTING - MODEL METRICS")
    print("-" * 50)
    print("Supported metrics:")
    
    for metric in METRIC_COLUMNS:
        print(f"- {metric}")