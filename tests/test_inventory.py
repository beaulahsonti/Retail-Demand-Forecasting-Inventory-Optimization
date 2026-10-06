"""
Tests for inventory optimization outputs.
"""

from pathlib import Path
import unittest

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

SAFETY_STOCK_FILE = (
    PROJECT_ROOT / "reports" / "safety_stock.csv"
)

REORDER_POINT_FILE = (
    PROJECT_ROOT / "reports" / "reorder_point.csv"
)

INVENTORY_FILE = (
    PROJECT_ROOT / "reports" / "inventory_optimization.csv"
)


class TestInventory(unittest.TestCase):

    def test_safety_stock_file_exists(self):
        """Verify that safety stock results exist."""
        self.assertTrue(
            SAFETY_STOCK_FILE.exists(),
            f"Safety stock file not found: {SAFETY_STOCK_FILE}"
        )

    def test_reorder_point_file_exists(self):
        """Verify that reorder point results exist."""
        self.assertTrue(
            REORDER_POINT_FILE.exists(),
            f"Reorder point file not found: {REORDER_POINT_FILE}"
        )

    def test_inventory_optimization_file_exists(self):
        """Verify that inventory optimization results exist."""
        self.assertTrue(
            INVENTORY_FILE.exists(),
            f"Inventory optimization file not found: {INVENTORY_FILE}"
        )

    def test_safety_stock_values_are_non_negative(self):
        """Verify safety stock values are not negative."""
        data = pd.read_csv(SAFETY_STOCK_FILE)

        numeric_columns = data.select_dtypes(
            include="number"
        ).columns

        self.assertGreater(
            len(numeric_columns),
            0
        )

        for column in numeric_columns:
            self.assertTrue(
                (data[column] >= 0).all(),
                f"Negative value found in {column}"
            )

    def test_reorder_point_values_are_non_negative(self):
        """Verify reorder point values are not negative."""
        data = pd.read_csv(REORDER_POINT_FILE)

        numeric_columns = data.select_dtypes(
            include="number"
        ).columns

        for column in numeric_columns:
            self.assertTrue(
                (data[column] >= 0).all(),
                f"Negative value found in {column}"
            )

    def test_inventory_optimization_is_not_empty(self):
        """Verify inventory optimization contains records."""
        data = pd.read_csv(INVENTORY_FILE)

        self.assertFalse(data.empty)


if __name__ == "__main__":
    unittest.main()