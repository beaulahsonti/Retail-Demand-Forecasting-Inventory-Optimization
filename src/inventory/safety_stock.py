"""
Safety Stock Calculation

Calculates safety stock for each product-store combination
using historical demand variability.

Formula:
Safety Stock = Z × Demand Standard Deviation × sqrt(Lead Time)

Default service level:
95%

Z-score for 95% service level:
1.645
"""

from pathlib import Path

import numpy as np
import pandas as pd


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

OUTPUT_FILE = (
    PROJECT_ROOT
    / "reports"
    / "safety_stock.csv"
)


# -------------------------------------------------------------------
# INVENTORY PARAMETERS
# -------------------------------------------------------------------

SERVICE_LEVEL = 0.95

# Z-score corresponding approximately to a 95% service level
Z_SCORE = 1.645

# Assumed supplier lead time in days
LEAD_TIME_DAYS = 7


# -------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------

def main():

    print("=" * 70)
    print("SAFETY STOCK CALCULATION")
    print("=" * 70)

    # ---------------------------------------------------------------
    # LOAD HISTORICAL DEMAND
    # ---------------------------------------------------------------

    print("\nLoading historical demand data...")

    data = pd.read_csv(TRAIN_FILE)

    data["date"] = pd.to_datetime(
        data["date"]
    )

    print(
        f"Training rows: {len(data):,}"
    )

    # ---------------------------------------------------------------
    # CALCULATE DEMAND VARIABILITY
    # ---------------------------------------------------------------

    print(
        "\nCalculating demand variability "
        "by product-store..."
    )

    demand_stats = (
        data
        .groupby(
            [
                "item_id",
                "store_id"
            ],
            as_index=False
        )
        .agg(
            average_daily_demand=(
                "demand",
                "mean"
            ),
            demand_std=(
                "demand",
                "std"
            ),
            demand_records=(
                "demand",
                "count"
            )
        )
    )

    # ---------------------------------------------------------------
    # HANDLE MISSING STANDARD DEVIATION
    # ---------------------------------------------------------------

    demand_stats["demand_std"] = (
        demand_stats["demand_std"]
        .fillna(0)
    )

    # ---------------------------------------------------------------
    # SAFETY STOCK
    # ---------------------------------------------------------------

    demand_stats["safety_stock"] = (
        Z_SCORE
        * demand_stats["demand_std"]
        * np.sqrt(LEAD_TIME_DAYS)
    )

    # Round inventory quantities
    demand_stats["average_daily_demand"] = (
        demand_stats["average_daily_demand"]
        .round(2)
    )

    demand_stats["demand_std"] = (
        demand_stats["demand_std"]
        .round(2)
    )

    demand_stats["safety_stock"] = (
        demand_stats["safety_stock"]
        .round(2)
    )

    # ---------------------------------------------------------------
    # ADD INVENTORY PARAMETERS
    # ---------------------------------------------------------------

    demand_stats["service_level"] = (
        SERVICE_LEVEL
    )

    demand_stats["z_score"] = (
        Z_SCORE
    )

    demand_stats["lead_time_days"] = (
        LEAD_TIME_DAYS
    )

    # ---------------------------------------------------------------
    # SORT RESULTS
    # ---------------------------------------------------------------

    demand_stats = demand_stats.sort_values(
        "safety_stock",
        ascending=False
    ).reset_index(
        drop=True
    )

    # ---------------------------------------------------------------
    # SAVE RESULTS
    # ---------------------------------------------------------------

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    demand_stats.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # ---------------------------------------------------------------
    # DISPLAY SUMMARY
    # ---------------------------------------------------------------

    print("\n" + "=" * 70)
    print("SAFETY STOCK SUMMARY")
    print("=" * 70)

    print(
        f"\nProduct-store combinations: "
        f"{len(demand_stats):,}"
    )

    print(
        f"Service level: "
        f"{SERVICE_LEVEL * 100:.0f}%"
    )

    print(
        f"Lead time: "
        f"{LEAD_TIME_DAYS} days"
    )

    print(
        f"Z-score: "
        f"{Z_SCORE}"
    )

    print(
        f"\nAverage safety stock: "
        f"{demand_stats['safety_stock'].mean():.2f}"
    )

    print(
        f"Maximum safety stock: "
        f"{demand_stats['safety_stock'].max():.2f}"
    )

    print(
        f"Minimum safety stock: "
        f"{demand_stats['safety_stock'].min():.2f}"
    )

    # ---------------------------------------------------------------
    # TOP 10
    # ---------------------------------------------------------------

    print("\nTop 10 product-store combinations by safety stock:")

    print(
        demand_stats[
            [
                "item_id",
                "store_id",
                "average_daily_demand",
                "demand_std",
                "safety_stock"
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
        "\nSafety stock calculation completed successfully."
    )


# -------------------------------------------------------------------
# RUN PROGRAM
# -------------------------------------------------------------------

if __name__ == "__main__":
    main()