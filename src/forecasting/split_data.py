from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "model_features.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"


TRAIN_FILE = OUTPUT_DIR / "forecast_train.csv"
VALIDATION_FILE = OUTPUT_DIR / "forecast_validation.csv"


def main():

    print("=" * 70)
    print("TIME-SERIES TRAIN / VALIDATION SPLIT")
    print("=" * 70)

    df = pd.read_csv(INPUT_FILE)
    df["date"] = pd.to_datetime(df["date"])

    df = df.sort_values(
        ["date", "item_id", "store_id"]
    ).reset_index(drop=True)

    print(f"\nTotal rows: {len(df):,}")
    print(f"Start date: {df['date'].min().date()}")
    print(f"End date:   {df['date'].max().date()}")

    # Use the last 28 days of the available feature dataset
    # as the validation period.
    validation_start = (
        df["date"].max() - pd.Timedelta(days=27)
    )

    train_df = df[
        df["date"] < validation_start
    ].copy()

    validation_df = df[
        df["date"] >= validation_start
    ].copy()

    # Save datasets
    train_df.to_csv(
        TRAIN_FILE,
        index=False
    )

    validation_df.to_csv(
        VALIDATION_FILE,
        index=False
    )

    print("\nSplit completed successfully.")

    print("\nTraining period:")
    print(
        f"{train_df['date'].min().date()} "
        f"→ "
        f"{train_df['date'].max().date()}"
    )

    print(f"Training rows: {len(train_df):,}")

    print("\nValidation period:")
    print(
        f"{validation_df['date'].min().date()} "
        f"→ "
        f"{validation_df['date'].max().date()}"
    )

    print(f"Validation rows: {len(validation_df):,}")

    print("\nSaved files:")
    print(TRAIN_FILE)
    print(VALIDATION_FILE)


if __name__ == "__main__":
    main()