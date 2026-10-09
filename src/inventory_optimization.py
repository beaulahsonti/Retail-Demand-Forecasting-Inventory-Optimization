import pandas as pd
import numpy as np
import os

INPUT_PATH = "models/lightgbm_predictions.csv"
OUTPUT_PATH = "models/inventory_recommendations.csv"

LEAD_TIME_DAYS = 7
SERVICE_LEVEL_Z = 1.65


def main():
    print("Loading LightGBM predictions...")

    df = pd.read_csv(INPUT_PATH)

    df["date"] = pd.to_datetime(df["date"])

    print(f"Prediction rows: {len(df):,}")

    # Calculate demand statistics for each item-store combination
    inventory = (
        df.groupby(["item_id", "store_id"])
        .agg(
            average_demand=("prediction", "mean"),
            demand_std=("prediction", "std"),
            forecast_demand=("prediction", "sum")
        )
        .reset_index()
    )

    inventory["demand_std"] = inventory["demand_std"].fillna(0)

    # Safety stock
    inventory["safety_stock"] = (
        SERVICE_LEVEL_Z
        * inventory["demand_std"]
        * np.sqrt(LEAD_TIME_DAYS)
    )

    # Expected demand during lead time
    inventory["lead_time_demand"] = (
        inventory["average_demand"]
        * LEAD_TIME_DAYS
    )

    # Reorder point
    inventory["reorder_point"] = (
        inventory["lead_time_demand"]
        + inventory["safety_stock"]
    )

    # Recommended inventory level
    inventory["recommended_inventory"] = (
        inventory["forecast_demand"]
        + inventory["safety_stock"]
    )

    # Round values
    numeric_columns = [
        "average_demand",
        "demand_std",
        "forecast_demand",
        "safety_stock",
        "lead_time_demand",
        "reorder_point",
        "recommended_inventory"
    ]

    inventory[numeric_columns] = (
        inventory[numeric_columns].round(2)
    )

    inventory = inventory.sort_values(
        "recommended_inventory",
        ascending=False
    )

    os.makedirs("models", exist_ok=True)

    inventory.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print("\n========== INVENTORY OPTIMIZATION ==========")
    print(f"Item-store combinations: {len(inventory):,}")

    print("\nTop 10 inventory recommendations:")
    print(
        inventory.head(10).to_string(index=False)
    )

    print(f"\nSaved to: {OUTPUT_PATH}")
    print("Inventory optimization completed successfully.")


if __name__ == "__main__":
    main()