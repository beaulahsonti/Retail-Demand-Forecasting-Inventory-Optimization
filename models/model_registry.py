"""
Model registry for the Retail Demand Forecasting project.

Provides a central place to register and retrieve
the forecasting models used by the project.
"""

MODEL_REGISTRY = {
    "baseline": {
        "name": "7-Day Lag Baseline",
        "module": "src.forecasting.baseline_model",
        "purpose": "Baseline demand forecasting",
    },
    "prophet": {
        "name": "Prophet",
        "module": "src.forecasting.prophet_model",
        "purpose": "Time-series demand forecasting",
    },
    "lightgbm": {
        "name": "LightGBM",
        "module": "src.forecasting.lightgbm_model",
        "purpose": "Machine-learning demand forecasting",
    },
}


def get_model(model_name):
    """Return a registered model configuration."""
    return MODEL_REGISTRY.get(model_name)


def list_models():
    """Return all registered model names."""
    return list(MODEL_REGISTRY.keys())


def register_model(model_name, name, module, purpose):
    """Register a new forecasting model."""
    MODEL_REGISTRY[model_name] = {
        "name": name,
        "module": module,
        "purpose": purpose,
    }


if __name__ == "__main__":
    print("RETAIL DEMAND FORECASTING - MODEL REGISTRY")
    print("-" * 50)

    for model_name in list_models():
        model = get_model(model_name)
        print(f"\nKey: {model_name}")
        print(f"Name: {model['name']}")
        print(f"Module: {model['module']}")
        print(f"Purpose: {model['purpose']}")