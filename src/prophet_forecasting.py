import duckdb
import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import os

FEATURE_PATH = "data/model_training.parquet"
OUTPUT_PATH = "models/prophet_predictions.csv"


def main():
    print("Loading model training data...")

    con = duckdb.connect()

    df = con.execute(f"""
        SELECT *
        FROM read_parquet('{FEATURE_PATH}')
        ORDER BY item_id, store_id, date
    """).fetchdf()

    con.close()

    print(f"Rows loaded: {len(df):,}")

    df["date"] = pd.to_datetime(df["date"])

    # Select the highest-sales item-store combination
    series = (
        df.groupby(["item_id", "store_id"])["sales"]
        .sum()
        .sort_values(ascending=False)
    )

    item_id = series.index[0][0]
    store_id = series.index[0][1]

    print(f"\nSelected series:")
    print(f"Item : {item_id}")
    print(f"Store: {store_id}")

    data = df[
        (df["item_id"] == item_id) &
        (df["store_id"] == store_id)
    ].copy()

    data = data.sort_values("date")

    # Last 28 days for testing
    cutoff_date = data["date"].max() - pd.Timedelta(days=27)

    train = data[data["date"] < cutoff_date].copy()
    test = data[data["date"] >= cutoff_date].copy()

    print(f"Training rows: {len(train):,}")
    print(f"Test rows: {len(test):,}")

    # Prophet requires columns ds and y
    prophet_train = train[["date", "sales"]].rename(
        columns={
            "date": "ds",
            "sales": "y"
        }
    )

    print("\nTraining Prophet model...")

    model = Prophet(
        weekly_seasonality=True,
        yearly_seasonality=True,
        daily_seasonality=False
    )

    model.fit(prophet_train)

    # Forecast test period
    future = test[["date"]].rename(columns={"date": "ds"})

    forecast = model.predict(future)

    predictions = forecast[
        ["ds", "yhat"]
    ].copy()

    predictions = predictions.rename(
        columns={
            "ds": "date",
            "yhat": "prediction"
        }
    )

    predictions["prediction"] = predictions["prediction"].clip(lower=0)

    predictions["actual"] = test["sales"].values

    mae = mean_absolute_error(
        predictions["actual"],
        predictions["prediction"]
    )

    rmse = np.sqrt(
        mean_squared_error(
            predictions["actual"],
            predictions["prediction"]
        )
    )

    print("\n========== PROPHET RESULTS ==========")
    print(f"MAE : {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")

    predictions["item_id"] = item_id
    predictions["store_id"] = store_id

    predictions = predictions[
        [
            "item_id",
            "store_id",
            "date",
            "actual",
            "prediction"
        ]
    ]

    os.makedirs("models", exist_ok=True)

    predictions.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(f"\nPredictions saved to: {OUTPUT_PATH}")
    print("Prophet forecasting completed successfully.")


if __name__ == "__main__":
    main()