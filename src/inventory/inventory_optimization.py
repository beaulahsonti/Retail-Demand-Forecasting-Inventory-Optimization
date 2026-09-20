"""
Inventory Optimization

Combines:
- Reorder point
- Safety stock
- Lead-time demand
- Demand forecast

Creates a final inventory recommendation for
each product-store combination.
"""

from pathlib import Path

import numpy as np
import pandas as pd


# -------------------------------------------------------------------
# PROJECT PATHS
# -------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

REORDER_POINT_FILE = (
    PROJECT_ROOT
    / "reports"
    / "reorder_point.csv"
)

FORECAST_FILE = (
    PROJECT_ROOT
    / "outputs"
    / "forecasts"
    / "lightgbm_predictions.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "reports"
    / "inventory_optimization.csv"
)


# -------------------------------------------------------------------
# INVENTORY PARAMETERS
# -------------------------------------------------------------------

# Number of days used for the recommended inventory horizon.
FORECAST_HORIZON_DAYS = 7


# -------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------

def main():

    print("=" * 70)
    print("INVENTORY OPTIMIZATION")
    print("=" * 70)

    # ---------------------------------------------------------------
    # LOAD REORDER POINT DATA
    # ---------------------------------------------------------------

    print("\nLoading reorder point data...")

    inventory = pd.read_csv(
        REORDER_POINT_FILE
    )

    print(
        f"Product-store combinations: "
        f"{len(inventory):,}"
    )

    # ---------------------------------------------------------------
    # LOAD LIGHTGBM FORECASTS
    # ---------------------------------------------------------------

    print("\nLoading LightGBM forecasts...")

    forecasts = pd.read_csv(
        FORECAST_FILE
    )

    forecasts["date"] = pd.to_datetime(
        forecasts["date"]
    )

    print(
        f"Forecast rows: "
        f"{len(forecasts):,}"
    )

    # ---------------------------------------------------------------
    # VALIDATE FORECAST COLUMNS
    # ---------------------------------------------------------------

    required_forecast_columns = [
        "date",
        "item_id",
        "store_id",
        "prediction",
    ]

    missing_forecast_columns = [
        column
        for column in required_forecast_columns
        if column not in forecasts.columns
    ]

    if missing_forecast_columns:
        raise ValueError(
            "Missing forecast columns: "
            f"{missing_forecast_columns}"
        )

    # ---------------------------------------------------------------
    # AGGREGATE FORECAST DEMAND
    # ---------------------------------------------------------------

    forecast_summary = (
        forecasts
        .groupby(
            [
                "item_id",
                "store_id"
            ],
            as_index=False
        )
        .agg(
            forecast_demand=(
                "prediction",
                "sum"
            ),
            forecast_daily_average=(
                "prediction",
                "mean"
            ),
            forecast_peak_demand=(
                "prediction",
                "max"
            )
        )
    )

    # ---------------------------------------------------------------
    # MERGE INVENTORY AND FORECAST DATA
    # ---------------------------------------------------------------

    result = inventory.merge(
        forecast_summary,
        on=[
            "item_id",
            "store_id"
        ],
        how="left"
    )

    # ---------------------------------------------------------------
    # HANDLE MISSING FORECASTS
    # ---------------------------------------------------------------

    forecast_columns = [
        "forecast_demand",
        "forecast_daily_average",
        "forecast_peak_demand",
    ]

    for column in forecast_columns:

        result[column] = (
            result[column]
            .fillna(0)
        )

    # ---------------------------------------------------------------
    # CALCULATE FORECAST HORIZON DEMAND
    # ---------------------------------------------------------------

    result["forecast_horizon_demand"] = (
        result["forecast_daily_average"]
        * FORECAST_HORIZON_DAYS
    )

    # ---------------------------------------------------------------
    # RECOMMENDED INVENTORY
    # ---------------------------------------------------------------

    result["recommended_inventory"] = (
        result["forecast_horizon_demand"]
        + result["safety_stock"]
    )

    # ---------------------------------------------------------------
    # TARGET INVENTORY
    # ---------------------------------------------------------------

    result["target_inventory"] = (
        np.maximum(
            result["recommended_inventory"],
            result["reorder_point"]
        )
    )

    # ---------------------------------------------------------------
    # INVENTORY BUFFER
    # ---------------------------------------------------------------

    result["inventory_buffer"] = (
        result["target_inventory"]
        - result["forecast_horizon_demand"]
    )

    # ---------------------------------------------------------------
    # INVENTORY ACTION
    # ---------------------------------------------------------------

    def determine_action(row):

        if row["target_inventory"] >= row["reorder_point"]:

            if row["inventory_level"] == "High":
                return "Maintain High Stock"

            elif row["inventory_level"] == "Medium":
                return "Maintain Stock"

            else:
                return "Maintain Safety Stock"

        return "Review Inventory"

    result["recommended_action"] = (
        result.apply(
            determine_action,
            axis=1
        )
    )

    # ---------------------------------------------------------------
    # ROUND NUMERIC VALUES
    # ---------------------------------------------------------------

    numeric_columns = [
        "forecast_demand",
        "forecast_daily_average",
        "forecast_peak_demand",
        "forecast_horizon_demand",
        "recommended_inventory",
        "target_inventory",
        "inventory_buffer",
    ]

    for column in numeric_columns:

        result[column] = (
            result[column]
            .round(2)
        )

    # ---------------------------------------------------------------
    # ADD FORECAST HORIZON
    # ---------------------------------------------------------------

    result["forecast_horizon_days"] = (
        FORECAST_HORIZON_DAYS
    )

    # ---------------------------------------------------------------
    # SORT BY TARGET INVENTORY
    # ---------------------------------------------------------------

    result = result.sort_values(
        "target_inventory",
        ascending=False
    ).reset_index(
        drop=True
    )

    # ---------------------------------------------------------------
    # SAVE OUTPUT
    # ---------------------------------------------------------------

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    result.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # ---------------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------------

    print("\n" + "=" * 70)
    print("INVENTORY OPTIMIZATION SUMMARY")
    print("=" * 70)

    print(
        f"\nProduct-store combinations: "
        f"{len(result):,}"
    )

    print(
        f"Forecast horizon: "
        f"{FORECAST_HORIZON_DAYS} days"
    )

    print(
        f"Average forecast demand: "
        f"{result['forecast_demand'].mean():.2f}"
    )

    print(
        f"Average recommended inventory: "
        f"{result['recommended_inventory'].mean():.2f}"
    )

    print(
        f"Average target inventory: "
        f"{result['target_inventory'].mean():.2f}"
    )

    print(
        f"Maximum target inventory: "
        f"{result['target_inventory'].max():.2f}"
    )

    # ---------------------------------------------------------------
    # ACTION DISTRIBUTION
    # ---------------------------------------------------------------

    print("\nRecommended action distribution:")

    print(
        result["recommended_action"]
        .value_counts()
        .to_string()
    )

    # ---------------------------------------------------------------
    # TOP 10
    # ---------------------------------------------------------------

    print(
        "\nTop 10 product-store combinations "
        "by target inventory:"
    )

    print(
        result[
            [
                "item_id",
                "store_id",
                "forecast_demand",
                "safety_stock",
                "reorder_point",
                "target_inventory",
                "inventory_level",
                "recommended_action",
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

    # ---------------------------------------------------------------
    # FINAL OUTPUT
    # ---------------------------------------------------------------

    print("\nSaved file:")
    print(OUTPUT_FILE)

    print(
        "\nInventory optimization completed successfully."
    )


# -------------------------------------------------------------------
# RUN PROGRAM
# -------------------------------------------------------------------

if __name__ == "__main__":
    main()