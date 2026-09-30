import duckdb
import pandas as pd
import numpy as np
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import os

FEATURE_PATH = "data/model_training.parquet"
OUTPUT_PATH = "models/lightgbm_predictions.csv"


def main():
    print("Loading model training data...")

    con = duckdb.connect()

    df = con.execute(f"""
        SELECT *
        FROM read_parquet('{FEATURE_PATH}')
        ORDER BY date
    """).fetchdf()

    con.close()

    print(f"Rows loaded: {len(df):,}")

    df["date"] = pd.to_datetime(df["date"])

    # Last 28 days are used for testing
    cutoff_date = df["date"].max() - pd.Timedelta(days=27)

    train = df[df["date"] < cutoff_date].copy()
    test = df[df["date"] >= cutoff_date].copy()

    print(f"Training rows: {len(train):,}")
    print(f"Test rows: {len(test):,}")

    features = [
        "wday",
        "month",
        "year",
        "snap",
        "lag_7",
        "lag_28",
        "rolling_mean_7",
        "rolling_mean_28"
    ]

    categorical_features = [
        "item_id",
        "store_id",
        "state_id"
    ]

    # Convert categorical columns to category dtype
    for column in categorical_features:
        train[column] = train[column].astype("category")

        test[column] = pd.Categorical(
            test[column],
            categories=train[column].cat.categories
        )

    features += categorical_features

    X_train = train[features]
    y_train = train["sales"]

    X_test = test[features]
    y_test = test["sales"]

    print("\nTraining LightGBM model...")

    model = LGBMRegressor(
        objective="regression",
        n_estimators=300,
        learning_rate=0.05,
        num_leaves=31,
        max_depth=-1,
        random_state=42,
        verbosity=-1
    )

    model.fit(X_train, y_train)

    print("Generating predictions...")

    predictions = model.predict(X_test)

    predictions = np.maximum(predictions, 0)

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            predictions
        )
    )

    print("\n========== LIGHTGBM RESULTS ==========")
    print(f"MAE : {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")

    output = test[
        [
            "item_id",
            "store_id",
            "date",
            "sales"
        ]
    ].copy()

    output["prediction"] = predictions

    os.makedirs("models", exist_ok=True)

    output.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(f"\nPredictions saved to: {OUTPUT_PATH}")
    print("LightGBM forecasting completed successfully.")


if __name__ == "__main__":
    main()