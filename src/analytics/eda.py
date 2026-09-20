from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "clean_train.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "figures"
REPORT_DIR = PROJECT_ROOT / "reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def main():

    print("=" * 70)
    print("RETAIL DEMAND EXPLORATORY DATA ANALYSIS")
    print("=" * 70)

    # Load data
    df = pd.read_csv(INPUT_FILE)
    df["date"] = pd.to_datetime(df["date"])

    print(f"\nRows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    # ---------------------------------------------------------
    # 1. Basic statistics
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("1. DEMAND STATISTICS")
    print("=" * 70)

    print(df["demand"].describe())

    # ---------------------------------------------------------
    # 2. Missing values
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("2. MISSING VALUES")
    print("=" * 70)

    print(df.isnull().sum())

    # ---------------------------------------------------------
    # 3. Demand by product
    # ---------------------------------------------------------

    product_demand = (
        df.groupby("item_id", as_index=False)["demand"]
        .sum()
        .sort_values("demand", ascending=False)
    )

    print("\nTop products by total demand:")
    print(product_demand.head(10).to_string(index=False))

    plt.figure(figsize=(12, 6))

    sns.barplot(
        data=product_demand,
        x="item_id",
        y="demand"
    )

    plt.title("Total Demand by Product")
    plt.xlabel("Product")
    plt.ylabel("Total Demand")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "demand_by_product.png",
        dpi=300
    )

    plt.close()

    # ---------------------------------------------------------
    # 4. Demand by store
    # ---------------------------------------------------------

    store_demand = (
        df.groupby("store_id", as_index=False)["demand"]
        .sum()
        .sort_values("demand", ascending=False)
    )

    print("\nDemand by store:")
    print(store_demand.to_string(index=False))

    plt.figure(figsize=(10, 6))

    sns.barplot(
        data=store_demand,
        x="store_id",
        y="demand"
    )

    plt.title("Total Demand by Store")
    plt.xlabel("Store")
    plt.ylabel("Total Demand")
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "demand_by_store.png",
        dpi=300
    )

    plt.close()

    # ---------------------------------------------------------
    # 5. Demand by category
    # ---------------------------------------------------------

    category_demand = (
        df.groupby("cat_id", as_index=False)["demand"]
        .sum()
        .sort_values("demand", ascending=False)
    )

    print("\nDemand by category:")
    print(category_demand.to_string(index=False))

    plt.figure(figsize=(10, 6))

    sns.barplot(
        data=category_demand,
        x="cat_id",
        y="demand"
    )

    plt.title("Total Demand by Category")
    plt.xlabel("Category")
    plt.ylabel("Total Demand")
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "demand_by_category.png",
        dpi=300
    )

    plt.close()

    # ---------------------------------------------------------
    # 6. Daily demand trend
    # ---------------------------------------------------------

    daily_demand = (
        df.groupby("date", as_index=False)["demand"]
        .sum()
        .sort_values("date")
    )

    plt.figure(figsize=(14, 6))

    plt.plot(
        daily_demand["date"],
        daily_demand["demand"]
    )

    plt.title("Daily Retail Demand Trend")
    plt.xlabel("Date")
    plt.ylabel("Total Demand")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "daily_demand_trend.png",
        dpi=300
    )

    plt.close()

    # ---------------------------------------------------------
    # 7. Monthly demand trend
    # ---------------------------------------------------------

    df["month"] = df["date"].dt.to_period("M").astype(str)

    monthly_demand = (
        df.groupby("month", as_index=False)["demand"]
        .sum()
    )

    plt.figure(figsize=(14, 6))

    plt.plot(
        monthly_demand["month"],
        monthly_demand["demand"],
        marker="o"
    )

    plt.title("Monthly Retail Demand Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Demand")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "monthly_demand_trend.png",
        dpi=300
    )

    plt.close()

    # ---------------------------------------------------------
    # 8. Demand distribution
    # ---------------------------------------------------------

    plt.figure(figsize=(10, 6))

    sns.histplot(
        df["demand"],
        bins=50,
        kde=True
    )

    plt.title("Distribution of Retail Demand")
    plt.xlabel("Demand")
    plt.ylabel("Frequency")
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "demand_distribution.png",
        dpi=300
    )

    plt.close()

    # ---------------------------------------------------------
    # 9. Zero-demand analysis
    # ---------------------------------------------------------

    zero_demand_count = int((df["demand"] == 0).sum())
    total_rows = len(df)

    zero_demand_percentage = (
        zero_demand_count / total_rows * 100
    )

    print("\n" + "=" * 70)
    print("3. ZERO-DEMAND ANALYSIS")
    print("=" * 70)

    print(f"Zero-demand records: {zero_demand_count:,}")
    print(
        f"Zero-demand percentage: "
        f"{zero_demand_percentage:.2f}%"
    )

    # ---------------------------------------------------------
    # 10. Demand summary by product and store
    # ---------------------------------------------------------

    product_store_summary = (
        df.groupby(
            ["item_id", "store_id"],
            as_index=False
        )["demand"]
        .agg(
            total_demand="sum",
            average_demand="mean",
            maximum_demand="max"
        )
        .sort_values(
            "total_demand",
            ascending=False
        )
    )

    product_store_summary.to_csv(
        REPORT_DIR / "product_store_demand_summary.csv",
        index=False
    )

    # ---------------------------------------------------------
    # Save overall EDA summary
    # ---------------------------------------------------------

    summary = pd.DataFrame({
        "metric": [
            "rows",
            "columns",
            "unique_products",
            "unique_departments",
            "unique_categories",
            "unique_stores",
            "unique_states",
            "total_demand",
            "average_demand",
            "median_demand",
            "zero_demand_records",
            "zero_demand_percentage",
            "start_date",
            "end_date"
        ],
        "value": [
            len(df),
            len(df.columns),
            df["item_id"].nunique(),
            df["dept_id"].nunique(),
            df["cat_id"].nunique(),
            df["store_id"].nunique(),
            df["state_id"].nunique(),
            df["demand"].sum(),
            df["demand"].mean(),
            df["demand"].median(),
            zero_demand_count,
            zero_demand_percentage,
            df["date"].min().date(),
            df["date"].max().date()
        ]
    })

    summary.to_csv(
        REPORT_DIR / "eda_summary.csv",
        index=False
    )

    print("\n" + "=" * 70)
    print("EDA COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print("\nGenerated figures:")

    for file in sorted(OUTPUT_DIR.glob("*.png")):
        print(f"  ✓ {file.name}")

    print("\nGenerated reports:")

    for file in sorted(REPORT_DIR.glob("*.csv")):
        print(f"  ✓ {file.name}")


if __name__ == "__main__":
    main()