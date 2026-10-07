"""
Tests for model utility modules.
"""

from pathlib import Path
import sys
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from models.model_config import get_model_config, get_forecast_horizon
from models.model_registry import get_model, list_models
from models.model_metadata import get_model_metadata


class TestModelUtilities(unittest.TestCase):

    def test_model_registry_contains_expected_models(self):
        """Verify the forecasting models are registered."""
        models = list_models()

        self.assertIn("baseline", models)
        self.assertIn("prophet", models)
        self.assertIn("lightgbm", models)

    def test_model_registry_returns_lightgbm(self):
        """Verify LightGBM metadata can be retrieved."""
        model = get_model("lightgbm")

        self.assertIsNotNone(model)
        self.assertEqual(model["name"], "LightGBM")

    def test_model_config_exists(self):
        """Verify LightGBM configuration is available."""
        config = get_model_config("lightgbm")

        self.assertIsNotNone(config)
        self.assertEqual(config["model_type"], "LightGBM")
        self.assertEqual(config["target_column"], "demand")

    def test_forecast_horizon(self):
        """Verify all forecasting models use the seven-day horizon."""
        for model_name in ["baseline", "prophet", "lightgbm"]:
            self.assertEqual(
                get_forecast_horizon(model_name),
                7
            )

    def test_model_metadata_contains_metrics(self):
        """Verify LightGBM metadata contains evaluation metrics."""
        metadata = get_model_metadata("lightgbm")

        self.assertIsNotNone(metadata)
        self.assertIn("metrics", metadata)

        required_metrics = {
            "MAE",
            "RMSE",
            "WAPE",
            "sMAPE",
        }

        self.assertTrue(
            required_metrics.issubset(
                metadata["metrics"].keys()
            )
        )


if __name__ == "__main__":
    unittest.main()