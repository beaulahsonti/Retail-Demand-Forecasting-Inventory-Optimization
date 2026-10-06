"""
Tests for the demand forecasting outputs.
"""

from pathlib import Path
import unittest

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

BASELINE_FILE = (
    PROJECT_ROOT
    / "outputs"
    / "forecasts"
    / "baseline_predictions.csv"
)

LIGHTGBM_FILE = (
    PROJECT_ROOT
    / "outputs"
    / "forecasts"
    / "lightgbm_predictions.csv"
)

BASELINE_METRICS = (
    PROJECT_ROOT
    / "reports"
    / "baseline_metrics.csv"
)

LIGHTGBM_METRICS = (
    PROJECT_ROOT
    / "reports"
    / "lightgbm_metrics.csv"
)


class TestForecasting(unittest.TestCase):

    def test_baseline_predictions_exist(self):
        """Verify that baseline predictions were generated."""
        self.assertTrue(
            BASELINE_FILE.exists(),
            f"Baseline prediction file not found: {BASELINE_FILE}"
        )

    def test_lightgbm_predictions_exist(self):
        """Verify that LightGBM predictions were generated."""
        self.assertTrue(
            LIGHTGBM_FILE.exists(),
            f"LightGBM prediction file not found: {LIGHTGBM_FILE}"
        )

    def test_baseline_metrics_exist(self):
        """Verify that baseline evaluation metrics exist."""
        self.assertTrue(
            BASELINE_METRICS.exists(),
            f"Baseline metrics file not found: {BASELINE_METRICS}"
        )

    def test_lightgbm_metrics_exist(self):
        """Verify that LightGBM evaluation metrics exist."""
        self.assertTrue(
            LIGHTGBM_METRICS.exists(),
            f"LightGBM metrics file not found: {LIGHTGBM_METRICS}"
        )

    def test_lightgbm_predictions_are_valid(self):
        """Verify that LightGBM predictions contain valid demand values."""
        data = pd.read_csv(LIGHTGBM_FILE)

        self.assertFalse(data.empty)

        prediction_columns = [
            column
            for column in data.columns
            if "prediction" in column.lower()
            or "forecast" in column.lower()
            or "demand" in column.lower()
        ]

        self.assertTrue(
            len(prediction_columns) > 0,
            "No prediction-related column was found."
        )

    def test_lightgbm_metrics_are_available(self):
        """Verify that the expected evaluation metrics are available."""
        metrics = pd.read_csv(LIGHTGBM_METRICS)

        required_metrics = {"MAE", "RMSE", "WAPE", "sMAPE"}

        available_columns = set(metrics.columns)

        self.assertTrue(
            required_metrics.issubset(available_columns),
            "One or more required forecasting metrics are missing."
        )


if __name__ == "__main__":
    unittest.main()