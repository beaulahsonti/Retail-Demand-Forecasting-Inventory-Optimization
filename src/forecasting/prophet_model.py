from pathlib import Path

import numpy as np
import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error


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

OUTPUT_DIR = PROJECT_ROOT / "outputs" / "forecasts"
REPORT_DIR = PROJECT_ROOT / "reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def wape(actual, predicted):
    denominator = np.abs(actual).sum()

    if denominator == 0:
        return np.nan

    return (
        np.abs(actual - predicted).sum()
        / denominator
        * 100
    )


def smape(actual, predicted):
    denominator = (
        np.abs(actual)
        + np.abs(predicted)
    )

    valid = denominator != 0

    if valid.sum() == 0:
        return np.nan

    return (
        np.mean(
            2
            * np.abs(actual[valid] - predicted[valid])
            / denominator[valid]
        )
        * 100
    )


def main():

    print("=" * 70)
    print("PROPHET RETAIL DEMAND FORECAST")
    print("=" * 70)

    # ---------------------------------------------------------
    # Load data
    # ---------------------------------------------------------

    train_df = pd.read_csv(TRAIN_FILE)
    validation_df = pd.read_csv(VALIDATION_FILE)

    train_df["date"] = pd.to_datetime(
        train_df["date"]
    )

    validation_df["date"] = pd.to_datetime(
        validation_df["date"]
    )

    print(
        f"\nTraining rows: "
        f"{len(train_df):,}"
    )

    print(
        f"Validation rows: "
        f"{len(validation_df):,}"
    )

    # ---------------------------------------------------------
    # Product-store combinations
    # ---------------------------------------------------------

    series = (
        train_df[
            ["item_id", "store_id"]
        ]
        .drop_duplicates()
        .sort_values(
            ["item_id", "store_id"]
        )
    )

    print(
        f"\nProduct-store series: "
        f"{len(series)}"
    )

    # Store predictions
    all_predictions = []

    # ---------------------------------------------------------
    # Train one Prophet model per product-store series
    # ---------------------------------------------------------

    for position, row in enumerate(
        series.itertuples(index=False),
        start=1
    ):

        item_id = row.item_id
        store_id = row.store_id

        print(
            f"\n[{position}/{len(series)}] "
            f"Training Prophet: "
            f"{item_id} / {store_id}"
        )

        series_train = train_df[
            (train_df["item_id"] == item_id)
            & (train_df["store_id"] == store_id)
        ][
            ["date", "demand"]
        ].copy()

        series_validation = validation_df[
            (validation_df["item_id"] == item_id)
            & (validation_df["store_id"] == store_id)
        ][
            ["id", "item_id", "store_id", "date", "demand"]
        ].copy()

        # Prophet requires ds and y
        prophet_train = series_train.rename(
            columns={
                "date": "ds",
                "demand": "y"
            }
        )

        # Create Prophet model
        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False,
            seasonality_mode="additive",
            interval_width=0.80
        )

        model.fit(prophet_train)

        # Forecast validation dates
        future = pd.DataFrame({
            "ds": series_validation["date"]
        })

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

        # Prophet can theoretically produce negative
        # forecasts for demand, so constrain to zero.
        predictions["prediction"] = (
            predictions["prediction"]
            .clip(lower=0)
        )

        series_validation = series_validation.merge(
            predictions,
            on="date",
            how="left"
        )

        all_predictions.append(
            series_validation
        )

    # ---------------------------------------------------------
    # Combine all predictions
    # ---------------------------------------------------------

    predictions_df = pd.concat(
        all_predictions,
        ignore_index=True
    )

    predictions_df = predictions_df.sort_values(
        ["date", "item_id", "store_id"]
    ).reset_index(drop=True)

    # ---------------------------------------------------------
    # Evaluation
    # ---------------------------------------------------------

    actual = predictions_df["demand"].to_numpy()
    predicted = predictions_df["prediction"].to_numpy()

    mae = mean_absolute_error(
        actual,
        predicted
    )

    rmse = np.sqrt(
        mean_squared_error(
            actual,
            predicted
        )
    )

    wape_score = wape(
        actual,
        predicted
    )

    smape_score = smape(
        actual,
        predicted
    )

    # ---------------------------------------------------------
    # Print metrics
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("PROPHET EVALUATION")
    print("=" * 70)

    print(
        f"\nValidation rows: "
        f"{len(predictions_df):,}"
    )

    print(f"MAE:   {mae:.4f}")
    print(f"RMSE:  {rmse:.4f}")
    print(f"WAPE:  {wape_score:.2f}%")
    print(f"sMAPE: {smape_score:.2f}%")

    # ---------------------------------------------------------
    # Save predictions
    # ---------------------------------------------------------

    prediction_file = (
        OUTPUT_DIR
        / "prophet_predictions.csv"
    )

    predictions_df.to_csv(
        prediction_file,
        index=False
    )

    # ---------------------------------------------------------
    # Save metrics
    # ---------------------------------------------------------

    metrics = pd.DataFrame({
        "model": ["Prophet"],
        "MAE": [mae],
        "RMSE": [rmse],
        "WAPE": [wape_score],
        "sMAPE": [smape_score]
    })

    metrics_file = (
        REPORT_DIR
        / "prophet_metrics.csv"
    )

    metrics.to_csv(
        metrics_file,
        index=False
    )

    print("\nSaved files:")
    print(prediction_file)
    print(metrics_file)

    print(
        "\nProphet forecasting completed successfully."
    )


if __name__ == "__main__":
    main()