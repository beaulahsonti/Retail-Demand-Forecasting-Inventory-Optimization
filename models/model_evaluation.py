"""
Evaluation utilities for retail demand forecasting models.
"""

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error


def calculate_mae(actual, predicted):
    """Calculate Mean Absolute Error."""
    return mean_absolute_error(actual, predicted)


def calculate_rmse(actual, predicted):
    """Calculate Root Mean Squared Error."""
    return np.sqrt(mean_squared_error(actual, predicted))


def calculate_wape(actual, predicted):
    """Calculate Weighted Absolute Percentage Error."""
    actual = np.asarray(actual)
    predicted = np.asarray(predicted)

    denominator = np.sum(np.abs(actual))

    if denominator == 0:
        return 0.0

    return (np.sum(np.abs(actual - predicted)) / denominator) * 100


def calculate_smape(actual, predicted):
    """Calculate Symmetric Mean Absolute Percentage Error."""
    actual = np.asarray(actual)
    predicted = np.asarray(predicted)

    denominator = np.abs(actual) + np.abs(predicted)

    valid = denominator != 0

    if not np.any(valid):
        return 0.0

    return (
        np.mean(
            2 * np.abs(actual[valid] - predicted[valid])
            / denominator[valid]
        )
        * 100
    )


def calculate_all_metrics(actual, predicted):
    """Calculate all project forecasting evaluation metrics."""
    return {
        "MAE": calculate_mae(actual, predicted),
        "RMSE": calculate_rmse(actual, predicted),
        "WAPE": calculate_wape(actual, predicted),
        "sMAPE": calculate_smape(actual, predicted),
    }


if __name__ == "__main__":
    print("RETAIL DEMAND FORECASTING - MODEL EVALUATION")
    print("-" * 55)

    actual = np.array([10, 20, 30, 40, 50])
    predicted = np.array([11, 19, 31, 38, 49])

    metrics = calculate_all_metrics(actual, predicted)

    for metric, value in metrics.items():
        print(f"{metric}: {value:.4f}")