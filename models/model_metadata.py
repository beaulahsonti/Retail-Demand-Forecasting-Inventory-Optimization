"""
Model metadata and evaluation results for the
Retail Demand Forecasting & Inventory Optimization project.
"""

MODEL_METADATA = {
    "baseline": {
        "name": "7-Day Lag Baseline",
        "type": "Baseline Forecasting",
        "metrics": {
            "MAE": 1.0527,
            "RMSE": 1.9956,
            "WAPE": 103.48,
            "sMAPE": 134.13,
        },
    },
    "prophet": {
        "name": "Prophet",
        "type": "Time-Series Forecasting",
        "metrics": {
            "MAE": 0.9238,
            "RMSE": 1.5743,
            "WAPE": 90.81,
            "sMAPE": 138.91,
        },
    },
    "lightgbm": {
        "name": "LightGBM",
        "type": "Machine Learning Forecasting",
        "metrics": {
            "MAE": 0.8643,
            "RMSE": 1.5303,
            "WAPE": 84.96,
            "sMAPE": 137.47,
        },
    },
}


def get_model_metadata(model_name):
    """Return metadata for a specific forecasting model."""
    return MODEL_METADATA.get(model_name)


def get_all_models():
    """Return metadata for all forecasting models."""
    return MODEL_METADATA


if __name__ == "__main__":
    print("RETAIL DEMAND FORECASTING - MODEL METADATA")
    print("-" * 50)

    for model_key, model in MODEL_METADATA.items():
        print(f"\nModel: {model['name']}")
        print(f"Type: {model['type']}")
        print(f"MAE: {model['metrics']['MAE']}")
        print(f"RMSE: {model['metrics']['RMSE']}")
        print(f"WAPE: {model['metrics']['WAPE']}%")
        print(f"sMAPE: {model['metrics']['sMAPE']}%")