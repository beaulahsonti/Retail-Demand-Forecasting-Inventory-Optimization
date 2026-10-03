"""
Prediction utility for trained retail demand forecasting models.
"""

import numpy as np


def prepare_features(data, feature_columns):
    """Prepare the required features for model prediction."""
    missing_columns = [
        column for column in feature_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing prediction features: {missing_columns}"
        )

    return data[feature_columns]


def generate_predictions(model, data, feature_columns):
    """Generate demand predictions using a trained model."""
    features = prepare_features(data, feature_columns)

    predictions = model.predict(features)

    predictions = np.asarray(predictions)
    predictions = np.maximum(predictions, 0)

    return predictions


def add_predictions(data, predictions, column_name="predicted_demand"):
    """Add predictions to a copy of the input dataset."""
    if len(data) != len(predictions):
        raise ValueError(
            "Number of predictions must match the number of rows."
        )

    result = data.copy()
    result[column_name] = predictions

    return result


if __name__ == "__main__":
    print("RETAIL DEMAND FORECASTING - MODEL PREDICTOR")
    print("-" * 55)
    print("Prediction utility is ready.")
    print("Negative predictions will be clipped to zero.")