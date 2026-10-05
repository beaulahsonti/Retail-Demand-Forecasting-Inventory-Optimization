"""
Tests for the feature engineering outputs used by the
Retail Demand Forecasting project.
"""

from pathlib import Path
import unittest

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FEATURE_FILE = PROJECT_ROOT / "data" / "processed" / "model_features.csv"


class TestFeatureEngineering(unittest.TestCase):

    def test_feature_file_exists(self):
        """Verify that the feature-engineered dataset exists."""
        self.assertTrue(
            FEATURE_FILE.exists(),
            f"Feature file not found: {FEATURE_FILE}"
        )

    def test_required_feature_columns_exist(self):
        """Verify that expected engineered features are available."""
        data = pd.read_csv(FEATURE_FILE, nrows=5)

        required_features = {
            "day_of_week",
            "day_of_month",
            "week_of_year",
            "month",
            "quarter",
            "year",
            "is_weekend",
            "lag_1",
            "lag_7",
            "lag_14",
            "lag_28",
            "rolling_mean_7",
            "rolling_mean_28",
            "rolling_std_7",
            "rolling_std_28",
        }

        self.assertTrue(
            required_features.issubset(data.columns),
            "One or more engineered features are missing."
        )

    def test_feature_file_is_not_empty(self):
        """Verify that the feature dataset contains records."""
        data = pd.read_csv(FEATURE_FILE, nrows=1)

        self.assertFalse(data.empty)

    def test_calendar_features_are_valid(self):
        """Verify basic ranges for calendar features."""
        data = pd.read_csv(
            FEATURE_FILE,
            usecols=[
                "day_of_week",
                "day_of_month",
                "month",
                "quarter",
                "is_weekend",
            ],
        )

        self.assertTrue(
            data["day_of_week"].between(0, 6).all()
        )

        self.assertTrue(
            data["day_of_month"].between(1, 31).all()
        )

        self.assertTrue(
            data["month"].between(1, 12).all()
        )

        self.assertTrue(
            data["quarter"].between(1, 4).all()
        )

        self.assertTrue(
            data["is_weekend"].isin([0, 1]).all()
        )


if __name__ == "__main__":
    unittest.main()