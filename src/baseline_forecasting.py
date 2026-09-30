import duckdb
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

FEATURE_PATH = "data/model_training.parquet"
OUTPUT_PATH = "models/baseline_predictions.csv"


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

    # Find the last 28 days for each item-store series
    df["max_date"] = df.groupby(
        ["item_id", "store_id"]
    )["date"].transform("max")

    df["days_from_end"] = (
        df["max_date"] - df["date"]
    ).dt.days

    test = df[df["days_from_end"] < 28].copy()

    print(f"Test rows: {len(test):,}")

    # Baseline prediction = sales from 7 days ago
    test["prediction"] = test["lag_7"]

    test = test.dropna(subset=["prediction"])

    mae = mean_absolute_error(
        test["sales"],
        test["prediction"]
    )

    rmse = np.sqrt(
        mean_squared_error(
            test["sales"],
            test["prediction"]
        )
    )

    print("\n========== BASELINE RESULTS ==========")
    print(f"MAE : {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")

    output = test[
        [
            "item_id",
            "store_id",
            "date",
            "sales",
            "prediction"
        ]
    ]

    output.to_csv(OUTPUT_PATH, index=False)

    print(f"\nPredictions saved to: {OUTPUT_PATH}")
    print("Baseline forecasting completed successfully.")


if __name__ == "__main__":
    main()