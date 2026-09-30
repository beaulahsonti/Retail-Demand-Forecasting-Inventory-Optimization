"""
Configuration settings for retail demand forecasting models.
"""

MODEL_CONFIG = {
    "baseline": {
        "model_type": "7-day-lag",
        "forecast_horizon": 7,
        "target_column": "demand",
    },
    "prophet": {
        "model_type": "Prophet",
        "forecast_horizon": 7,
        "target_column": "demand",
        "date_column": "date",
    },
    "lightgbm": {
        "model_type": "LightGBM",
        "forecast_horizon": 7,
        "target_column": "demand",
        "categorical_features": [
            "item_id",
            "dept_id",
            "cat_id",
            "store_id",
            "state_id",
        ],
    },
}


def get_model_config(model_name):
    """Return configuration for the requested model."""
    return MODEL_CONFIG.get(model_name)


def get_forecast_horizon(model_name):
    """Return the forecast horizon for a model."""
    config = get_model_config(model_name)

    if config is None:
        raise ValueError(f"Unknown model: {model_name}")

    return config["forecast_horizon"]


if __name__ == "__main__":
    print("RETAIL DEMAND FORECASTING - MODEL CONFIGURATION")
    print("-" * 55)

    for model_name, config in MODEL_CONFIG.items():
        print(f"\nModel: {model_name}")
        print(f"Type: {config['model_type']}")
        print(f"Forecast Horizon: {config['forecast_horizon']} days")
        print(f"Target Column: {config['target_column']}")