from pathlib import Path
import pandas as pd


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

TRAIN_FILE = RAW_DIR / "M5 sampled train.csv"
TEST_FILE = RAW_DIR / "M5 sampled test.csv"

CLEAN_TRAIN_FILE = PROCESSED_DIR / "clean_train.csv"
CLEAN_TEST_FILE = PROCESSED_DIR / "clean_test.csv"


EXPECTED_COLUMNS = [
    "id",
    "item_id",
    "dept_id",
    "cat_id",
    "store_id",
    "state_id",
    "demand",
    "date",
]


def clean_dataset(file_path):
    """Load and clean one dataset."""

    df = pd.read_csv(file_path)

    # Keep only expected columns
    df = df[EXPECTED_COLUMNS].copy()

    # Convert data types
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["demand"] = pd.to_numeric(df["demand"], errors="coerce")

    # Remove rows with invalid essential values
    df = df.dropna(
        subset=[
            "id",
            "item_id",
            "store_id",
            "demand",
            "date",
        ]
    )

    # Demand cannot be negative
    df = df[df["demand"] >= 0]

    # Remove exact duplicate records
    df = df.drop_duplicates()

    # Sort for time-series processing
    df = df.sort_values(
        by=["item_id", "store_id", "date"]
    ).reset_index(drop=True)

    return df


def main():

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("RETAIL DATA CLEANING")
    print("=" * 60)

    print("\nLoading training data...")
    train_df = clean_dataset(TRAIN_FILE)

    print("Loading testing data...")
    test_df = clean_dataset(TEST_FILE)

    # Save cleaned datasets
    train_df.to_csv(CLEAN_TRAIN_FILE, index=False)
    test_df.to_csv(CLEAN_TEST_FILE, index=False)

    print("\nCleaning completed successfully.")

    print("\nTraining dataset:")
    print(f"Rows: {len(train_df):,}")
    print(f"Columns: {len(train_df.columns)}")

    print("\nTesting dataset:")
    print(f"Rows: {len(test_df):,}")
    print(f"Columns: {len(test_df.columns)}")

    print("\nClean training file:")
    print(CLEAN_TRAIN_FILE)

    print("\nClean testing file:")
    print(CLEAN_TEST_FILE)

    print("\nFinal columns:")
    print(train_df.columns.tolist())


if __name__ == "__main__":
    main()