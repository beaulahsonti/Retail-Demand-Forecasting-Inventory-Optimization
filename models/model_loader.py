"""
Model loading utilities for the Retail Demand Forecasting project.
"""

from pathlib import Path
import joblib


MODEL_DIR = Path(__file__).resolve().parent


def save_model(model, model_name):
    """Save a trained model to the models directory."""
    model_path = MODEL_DIR / f"{model_name}.joblib"
    joblib.dump(model, model_path)
    return model_path


def load_model(model_name):
    """Load a saved model from the models directory."""
    model_path = MODEL_DIR / f"{model_name}.joblib"

    if not model_path.exists():
        raise FileNotFoundError(
            f"Model file not found: {model_path}"
        )

    return joblib.load(model_path)


def model_exists(model_name):
    """Check whether a saved model exists."""
    model_path = MODEL_DIR / f"{model_name}.joblib"
    return model_path.exists()


if __name__ == "__main__":
    print("RETAIL DEMAND FORECASTING - MODEL LOADER")
    print("-" * 50)
    print(f"Model directory: {MODEL_DIR}")
    print("Model loader is ready.")