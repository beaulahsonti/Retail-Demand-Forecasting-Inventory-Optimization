"""
LightGBM Retail Demand Forecasting

Trains a global LightGBM regression model using:
- Calendar features
- Lag features
- Rolling demand features
- Product/store/category information

Evaluates predictions on the 28-day validation period.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


# -------------------------------------------------------------------
# PROJECT PATHS
# -------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

TRAIN_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "forecast_train.csv"
)

VALIDATION_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "forecast_validation.csv"
)

FORECAST_OUTPUT = (
    PROJECT_ROOT
    / "outputs"
    / "forecasts"
    / "lightgbm_predictions.csv"
)

METRICS_OUTPUT = (
    PROJECT_ROOT
    / "reports"
    / "lightgbm_metrics.csv"
)

IMPORTANCE_OUTPUT = (
    PROJECT_ROOT
    / "reports"
    / "lightgbm_feature_importance.csv"
)


# -------------------------------------------------------------------
# METRICS
# -------------------------------------------------------------------

def calculate_wape(actual, predicted):
    """Calculate Weighted Absolute Percentage Error."""

    denominator = np.sum(np.abs(actual))

    if denominator == 0:
        return 0.0

    return (
        np.sum(np.abs(actual - predicted))
        / denominator
        * 100
    )


def calculate_smape(actual, predicted):
    """
    Calculate symmetric Mean Absolute Percentage Error.

    Rows where both actual and predicted are zero are assigned
    an sMAPE contribution of zero.
    """

    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)

    numerator = 2 * np.abs(actual - predicted)

    denominator = np.abs(actual) + np.abs(predicted)

    result = np.zeros_like(denominator, dtype=float)

    valid = denominator != 0

    result[valid] = (
        numerator[valid]
        / denominator[valid]
    )

    return np.mean(result) * 100


# -------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------

def main():

    print("=" * 70)
    print("LIGHTGBM RETAIL DEMAND FORECAST")
    print("=" * 70)

    # ---------------------------------------------------------------
    # LOAD DATA
    # ---------------------------------------------------------------

    print("\nLoading training and validation data...")

    train = pd.read_csv(TRAIN_FILE)
    validation = pd.read_csv(VALIDATION_FILE)

    train["date"] = pd.to_datetime(train["date"])
    validation["date"] = pd.to_datetime(validation["date"])

    print(f"Training rows: {len(train):,}")
    print(f"Validation rows: {len(validation):,}")

    # ---------------------------------------------------------------
    # FEATURES
    # ---------------------------------------------------------------

    categorical_features = [
        "item_id",
        "dept_id",
        "cat_id",
        "store_id",
        "state_id",
    ]

    numerical_features = [
        "day_of_week",
        "day_of_month",
        "week_of_year",
        "month",
        "quarter",
        "year",
        "is_weekend",
        "lag_1",
        "lag_7",
        "lag_14",
        "lag_28",
        "rolling_mean_7",
        "rolling_mean_28",
        "rolling_std_7",
        "rolling_std_28",
    ]

    feature_columns = (
        categorical_features
        + numerical_features
    )

    target_column = "demand"

    # ---------------------------------------------------------------
    # CHECK FEATURES
    # ---------------------------------------------------------------

    missing_train = [
        column
        for column in feature_columns
        if column not in train.columns
    ]

    missing_validation = [
        column
        for column in feature_columns
        if column not in validation.columns
    ]

    if missing_train:
        raise ValueError(
            f"Missing training features: {missing_train}"
        )

    if missing_validation:
        raise ValueError(
            f"Missing validation features: {missing_validation}"
        )

    # ---------------------------------------------------------------
    # CONVERT CATEGORICAL FEATURES
    # ---------------------------------------------------------------

    for column in categorical_features:

        train[column] = train[column].astype("category")

        validation[column] = pd.Categorical(
            validation[column],
            categories=train[column].cat.categories
        )

    # ---------------------------------------------------------------
    # PREPARE TRAINING DATA
    # ---------------------------------------------------------------

    X_train = train[feature_columns]
    y_train = train[target_column]

    X_validation = validation[feature_columns]
    y_validation = validation[target_column]

    print(
        f"\nNumber of features: {len(feature_columns)}"
    )

    print(
        f"Categorical features: "
        f"{len(categorical_features)}"
    )

    print(
        f"Numerical features: "
        f"{len(numerical_features)}"
    )

    # ---------------------------------------------------------------
    # TRAIN LIGHTGBM
    # ---------------------------------------------------------------

    print("\nTraining LightGBM model...")

    model = LGBMRegressor(
        objective="regression",
        n_estimators=500,
        learning_rate=0.05,
        num_leaves=31,
        max_depth=-1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1,
        verbosity=-1,
    )

    model.fit(
        X_train,
        y_train,
        categorical_feature=categorical_features,
    )

    print("LightGBM training completed.")

    # ---------------------------------------------------------------
    # GENERATE PREDICTIONS
    # ---------------------------------------------------------------

    print("\nGenerating validation predictions...")

    predictions = model.predict(X_validation)

    # Demand cannot be negative
    predictions = np.maximum(
        predictions,
        0
    )

    # ---------------------------------------------------------------
    # EVALUATION
    # ---------------------------------------------------------------

    mae = mean_absolute_error(
        y_validation,
        predictions
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_validation,
            predictions
        )
    )

    wape = calculate_wape(
        y_validation.to_numpy(),
        predictions
    )

    smape = calculate_smape(
        y_validation.to_numpy(),
        predictions
    )

    print("\n" + "=" * 70)
    print("LIGHTGBM EVALUATION")
    print("=" * 70)

    print(
        f"\nValidation rows: "
        f"{len(validation):,}"
    )

    print(
        f"MAE:   {mae:.4f}"
    )

    print(
        f"RMSE:  {rmse:.4f}"
    )

    print(
        f"WAPE:  {wape:.2f}%"
    )

    print(
        f"sMAPE: {smape:.2f}%"
    )

    # ---------------------------------------------------------------
    # SAVE PREDICTIONS
    # ---------------------------------------------------------------

    prediction_output = validation[
        [
            "date",
            "item_id",
            "dept_id",
            "cat_id",
            "store_id",
            "state_id",
            "demand",
        ]
    ].copy()

    prediction_output["prediction"] = predictions

    prediction_output.rename(
        columns={
            "demand": "actual_demand"
        },
        inplace=True
    )

    FORECAST_OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    prediction_output.to_csv(
        FORECAST_OUTPUT,
        index=False
    )

    # ---------------------------------------------------------------
    # SAVE METRICS
    # ---------------------------------------------------------------

    metrics = pd.DataFrame(
        [
            {
                "model": "LightGBM",
                "validation_rows": len(validation),
                "MAE": mae,
                "RMSE": rmse,
                "WAPE": wape,
                "sMAPE": smape,
            }
        ]
    )

    METRICS_OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    metrics.to_csv(
        METRICS_OUTPUT,
        index=False
    )

    # ---------------------------------------------------------------
    # FEATURE IMPORTANCE
    # ---------------------------------------------------------------

    importance = pd.DataFrame(
        {
            "feature": feature_columns,
            "importance": model.feature_importances_,
        }
    )

    importance = importance.sort_values(
        "importance",
        ascending=False
    )

    importance.to_csv(
        IMPORTANCE_OUTPUT,
        index=False
    )

    # ---------------------------------------------------------------
    # FINAL OUTPUT
    # ---------------------------------------------------------------

    print("\nSaved files:")

    print(
        FORECAST_OUTPUT
    )

    print(
        METRICS_OUTPUT
    )

    print(
        IMPORTANCE_OUTPUT
    )

    print(
        "\nLightGBM forecasting completed successfully."
    )


# -------------------------------------------------------------------
# RUN PROGRAM
# -------------------------------------------------------------------

if __name__ == "__main__":
    main()