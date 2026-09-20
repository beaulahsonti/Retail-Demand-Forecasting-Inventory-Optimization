from pathlib import Path

import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "clean_train.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

OUTPUT_FILE = OUTPUT_DIR / "model_features.csv"


def create_features(df):
    """
    Create time-series and historical demand features.

    Features are generated separately for each
    product-store combination.
    """

    df = df.copy()

    # ---------------------------------------------------------
    # Date features
    # ---------------------------------------------------------

    df["date"] = pd.to_datetime(df["date"])

    df["day_of_week"] = df["date"].dt.dayofweek
    df["day_of_month"] = df["date"].dt.day
    df["week_of_year"] = df["date"].dt.isocalendar().week.astype(int)
    df["month"] = df["date"].dt.month
    df["quarter"] = df["date"].dt.quarter
    df["year"] = df["date"].dt.year
    df["is_weekend"] = (
        df["day_of_week"] >= 5
    ).astype(int)

    # ---------------------------------------------------------
    # Sort before creating historical features
    # ---------------------------------------------------------

    df = df.sort_values(
        ["item_id", "store_id", "date"]
    ).reset_index(drop=True)

    group_columns = ["item_id", "store_id"]

    grouped_demand = df.groupby(
        group_columns
    )["demand"]

    # ---------------------------------------------------------
    # Lag features
    # ---------------------------------------------------------

    df["lag_1"] = grouped_demand.shift(1)
    df["lag_7"] = grouped_demand.shift(7)
    df["lag_14"] = grouped_demand.shift(14)
    df["lag_28"] = grouped_demand.shift(28)

    # ---------------------------------------------------------
    # Rolling demand features
    #
    # Shift by one day first so today's demand is NOT
    # used to predict today's demand.
    # ---------------------------------------------------------

    shifted_demand = grouped_demand.shift(1)

    df["rolling_mean_7"] = (
        shifted_demand
        .groupby(
            [
                df["item_id"],
                df["store_id"]
            ]
        )
        .transform(
            lambda x: x.rolling(7).mean()
        )
    )

    df["rolling_mean_28"] = (
        shifted_demand
        .groupby(
            [
                df["item_id"],
                df["store_id"]
            ]
        )
        .transform(
            lambda x: x.rolling(28).mean()
        )
    )

    df["rolling_std_7"] = (
        shifted_demand
        .groupby(
            [
                df["item_id"],
                df["store_id"]
            ]
        )
        .transform(
            lambda x: x.rolling(7).std()
        )
    )

    df["rolling_std_28"] = (
        shifted_demand
        .groupby(
            [
                df["item_id"],
                df["store_id"]
            ]
        )
        .transform(
            lambda x: x.rolling(28).std()
        )
    )

    # ---------------------------------------------------------
    # Fill rolling standard deviation for constant demand
    # ---------------------------------------------------------

    df["rolling_std_7"] = df["rolling_std_7"].fillna(0)
    df["rolling_std_28"] = df["rolling_std_28"].fillna(0)

    # ---------------------------------------------------------
    # Remove rows where sufficient history does not exist
    # ---------------------------------------------------------

    required_history = [
        "lag_28",
        "rolling_mean_28"
    ]

    df = df.dropna(
        subset=required_history
    ).reset_index(drop=True)

    return df


def main():

    print("=" * 70)
    print("RETAIL DEMAND FEATURE ENGINEERING")
    print("=" * 70)

    # Load cleaned data
    df = pd.read_csv(INPUT_FILE)

    print(f"\nInput rows: {len(df):,}")

    # Create features
    features = create_features(df)

    # Save
    features.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nFeature engineering completed successfully.")

    print(f"\nOutput rows: {len(features):,}")
    print(f"Output columns: {len(features.columns)}")

    print("\nCreated features:")

    feature_columns = [
        "day_of_week",
        "day_of_month",
        "week_of_year",
        "month",
        "quarter",
        "year",
        "is_weekend",
        "lag_1",
        "lag_7",
        "lag_14",
        "lag_28",
        "rolling_mean_7",
        "rolling_mean_28",
        "rolling_std_7",
        "rolling_std_28",
    ]

    for feature in feature_columns:
        print(f"  ✓ {feature}")

    print(f"\nSaved to:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()