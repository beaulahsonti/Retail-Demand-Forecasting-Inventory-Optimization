import pandas as pd
import os

INPUT_PATH = "models/inventory_recommendations.csv"
OUTPUT_PATH = "models/inventory_analysis.csv"


def main():
    print("Loading inventory recommendations...")

    df = pd.read_csv(INPUT_PATH)

    print(f"Inventory records: {len(df):,}")

    # Calculate inventory coverage
    df["inventory_buffer_ratio"] = (
        df["safety_stock"] / df["forecast_demand"]
    ).replace([float("inf"), -float("inf")], 0)

    # Categorize inventory priority
    df["inventory_priority"] = pd.cut(
        df["safety_stock"],
        bins=[-float("inf"), 50, 100, 200, float("inf")],
        labels=[
            "Low",
            "Medium",
            "High",
            "Very High"
        ]
    )

    # Sort by reorder point
    df = df.sort_values(
        "reorder_point",
        ascending=False
    )

    output_columns = [
        "item_id",
        "store_id",
        "average_demand",
        "demand_std",
        "forecast_demand",
        "safety_stock",
        "lead_time_demand",
        "reorder_point",
        "recommended_inventory",
        "inventory_buffer_ratio",
        "inventory_priority"
    ]

    analysis = df[output_columns].copy()

    analysis["inventory_buffer_ratio"] = (
        analysis["inventory_buffer_ratio"]
        .round(3)
    )

    os.makedirs("models", exist_ok=True)

    analysis.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print("\n========== INVENTORY ANALYSIS ==========")

    print("\nPriority distribution:")
    print(
        analysis["inventory_priority"]
        .value_counts()
        .sort_index()
    )

    print("\nTop 10 reorder-point recommendations:")
    print(
        analysis.head(10).to_string(index=False)
    )

    print(f"\nAnalysis saved to: {OUTPUT_PATH}")
    print("Inventory analysis completed successfully.")


if __name__ == "__main__":
    main()