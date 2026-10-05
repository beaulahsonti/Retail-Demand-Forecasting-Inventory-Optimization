"""
Tests for validating the retail demand dataset.
"""

from pathlib import Path
import unittest

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TRAIN_FILE = PROJECT_ROOT / "data" / "processed" / "clean_train.csv"


class TestDataValidation(unittest.TestCase):

    def test_training_file_exists(self):
        """Verify that the processed training dataset exists."""
        self.assertTrue(
            TRAIN_FILE.exists(),
            f"Training file not found: {TRAIN_FILE}"
        )

    def test_required_columns_exist(self):
        """Verify that the training dataset has required columns."""
        data = pd.read_csv(TRAIN_FILE, nrows=5)

        required_columns = {
            "id",
            "item_id",
            "dept_id",
            "cat_id",
            "store_id",
            "state_id",
            "demand",
            "date",
        }

        self.assertTrue(
            required_columns.issubset(data.columns),
            "One or more required columns are missing."
        )

    def test_demand_is_non_negative(self):
        """Verify that demand values are not negative."""
        data = pd.read_csv(
            TRAIN_FILE,
            usecols=["demand"]
        )

        self.assertGreaterEqual(
            data["demand"].min(),
            0
        )

    def test_date_column_is_valid(self):
        """Verify that date values can be parsed."""
        data = pd.read_csv(
            TRAIN_FILE,
            usecols=["date"]
        )

        dates = pd.to_datetime(
            data["date"],
            errors="coerce"
        )

        self.assertEqual(
            dates.isna().sum(),
            0
        )


if __name__ == "__main__":
    unittest.main()