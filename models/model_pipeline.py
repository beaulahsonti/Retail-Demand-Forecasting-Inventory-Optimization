"""
Reusable model pipeline utilities for retail demand forecasting.
"""

from pathlib import Path

import joblib


MODEL_DIR = Path(__file__).resolve().parent


def save_pipeline(pipeline, pipeline_name):
    """Save a trained preprocessing/model pipeline."""
    if not pipeline_name:
        raise ValueError("Pipeline name cannot be empty.")

    output_path = MODEL_DIR / f"{pipeline_name}_pipeline.joblib"
    joblib.dump(pipeline, output_path)

    return output_path


def load_pipeline(pipeline_name):
    """Load a saved preprocessing/model pipeline."""
    input_path = MODEL_DIR / f"{pipeline_name}_pipeline.joblib"

    if not input_path.exists():
        raise FileNotFoundError(
            f"Pipeline not found: {input_path}"
        )

    return joblib.load(input_path)


def pipeline_exists(pipeline_name):
    """Check whether a saved pipeline exists."""
    input_path = MODEL_DIR / f"{pipeline_name}_pipeline.joblib"
    return input_path.exists()


def get_pipeline_path(pipeline_name):
    """Return the expected path for a pipeline."""
    return MODEL_DIR / f"{pipeline_name}_pipeline.joblib"


if __name__ == "__main__":
    print("RETAIL DEMAND FORECASTING - MODEL PIPELINE")
    print("-" * 55)
    print(f"Pipeline directory: {MODEL_DIR}")
    print("Pipeline utility is ready.")