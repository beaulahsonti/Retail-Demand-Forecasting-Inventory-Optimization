"""
Utilities for managing trained model artifacts.
"""

from pathlib import Path


MODEL_DIR = Path(__file__).resolve().parent


def get_model_path(model_name, extension=".joblib"):
    """Return the expected path for a model artifact."""
    if not model_name:
        raise ValueError("Model name cannot be empty.")

    return MODEL_DIR / f"{model_name}{extension}"


def artifact_exists(model_name, extension=".joblib"):
    """Check whether a model artifact exists."""
    return get_model_path(model_name, extension).exists()


def list_artifacts():
    """List files currently stored in the models directory."""
    return sorted(
        path.name
        for path in MODEL_DIR.iterdir()
        if path.is_file()
    )


def get_artifact_summary():
    """Return basic information about model artifacts."""
    artifacts = []

    for path in MODEL_DIR.iterdir():
        if path.is_file():
            artifacts.append(
                {
                    "name": path.name,
                    "suffix": path.suffix,
                    "size_bytes": path.stat().st_size,
                }
            )

    return sorted(artifacts, key=lambda item: item["name"])


if __name__ == "__main__":
    print("RETAIL DEMAND FORECASTING - MODEL ARTIFACTS")
    print("-" * 55)

    artifacts = list_artifacts()

    if artifacts:
        for artifact in artifacts:
            print(f"- {artifact}")
    else:
        print("No model artifacts found yet.")

    print("\nModel directory:")
    print(MODEL_DIR)