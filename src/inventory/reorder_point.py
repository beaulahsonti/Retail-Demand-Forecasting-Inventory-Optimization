"""
Reorder Point Calculation

Formula:

Reorder Point =
Average Daily Demand × Lead Time
+ Safety Stock

Uses:
- Historical average daily demand
- Calculated safety stock
- 7-day supplier lead time
"""

from pathlib import Path

import pandas as pd


# -------------------------------------------------------------------
# PROJECT PATHS
# -------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SAFETY_STOCK_FILE = (
    PROJECT_ROOT
    / "reports"
    / "safety_stock.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "reports"
    / "reorder_point.csv"
)


# -------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------

def main():

    print("=" * 70)
    print("REORDER POINT CALCULATION")
    print("=" * 70)

    # ---------------------------------------------------------------
    # LOAD SAFETY STOCK DATA
    # ---------------------------------------------------------------

    print("\nLoading safety stock data...")

    data = pd.read_csv(
        SAFETY_STOCK_FILE
    )

    print(
        f"Product-store combinations: "
        f"{len(data):,}"
    )

    # ---------------------------------------------------------------
    # VALIDATE REQUIRED COLUMNS
    # ---------------------------------------------------------------

    required_columns = [
        "item_id",
        "store_id",
        "average_daily_demand",
        "safety_stock",
        "lead_time_days",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: "
            f"{missing_columns}"
        )

    # ---------------------------------------------------------------
    # CALCULATE LEAD-TIME DEMAND
    # ---------------------------------------------------------------

    data["lead_time_demand"] = (
        data["average_daily_demand"]
        * data["lead_time_days"]
    )

    # ---------------------------------------------------------------
    # CALCULATE REORDER POINT
    # ---------------------------------------------------------------

    data["reorder_point"] = (
        data["lead_time_demand"]
        + data["safety_stock"]
    )

    # ---------------------------------------------------------------
    # ROUND INVENTORY VALUES
    # ---------------------------------------------------------------

    data["lead_time_demand"] = (
        data["lead_time_demand"]
        .round(2)
    )

    data["reorder_point"] = (
        data["reorder_point"]
        .round(2)
    )

    # ---------------------------------------------------------------
    # ADD INVENTORY STATUS
    # ---------------------------------------------------------------

    def classify_inventory(row):

        if row["reorder_point"] <= 5:
            return "Low"

        elif row["reorder_point"] <= 15:
            return "Medium"

        else:
            return "High"

    data["inventory_level"] = (
        data.apply(
            classify_inventory,
            axis=1
        )
    )

    # ---------------------------------------------------------------
    # SORT BY REORDER POINT
    # ---------------------------------------------------------------

    data = data.sort_values(
        "reorder_point",
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

    data.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # ---------------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------------

    print("\n" + "=" * 70)
    print("REORDER POINT SUMMARY")
    print("=" * 70)

    print(
        f"\nAverage reorder point: "
        f"{data['reorder_point'].mean():.2f}"
    )

    print(
        f"Maximum reorder point: "
        f"{data['reorder_point'].max():.2f}"
    )

    print(
        f"Minimum reorder point: "
        f"{data['reorder_point'].min():.2f}"
    )

    # ---------------------------------------------------------------
    # INVENTORY LEVEL COUNTS
    # ---------------------------------------------------------------

    print("\nInventory level distribution:")

    print(
        data["inventory_level"]
        .value_counts()
        .to_string()
    )

    # ---------------------------------------------------------------
    # TOP 10
    # ---------------------------------------------------------------

    print(
        "\nTop 10 product-store combinations "
        "by reorder point:"
    )

    print(
        data[
            [
                "item_id",
                "store_id",
                "average_daily_demand",
                "lead_time_demand",
                "safety_stock",
                "reorder_point",
                "inventory_level",
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
        "\nReorder point calculation "
        "completed successfully."
    )


# -------------------------------------------------------------------
# RUN PROGRAM
# -------------------------------------------------------------------

if __name__ == "__main__":
    main()