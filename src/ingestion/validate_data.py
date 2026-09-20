from pathlib import Path
import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

TRAIN_FILE = RAW_DIR / "M5 sampled train.csv"
TEST_FILE = RAW_DIR / "M5 sampled test.csv"


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


def validate_dataset(file_path, dataset_name):
    print(f"\n{'=' * 60}")
    print(f"VALIDATING: {dataset_name}")
    print(f"{'=' * 60}")

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_csv(file_path)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    # Check columns
    if list(df.columns) != EXPECTED_COLUMNS:
        print("\nWARNING: Column structure is different from expected.")
        print("Actual columns:", df.columns.tolist())
    else:
        print("Column structure: PASS")

    # Convert date
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Convert demand
    df["demand"] = pd.to_numeric(df["demand"], errors="coerce")

    # Missing values
    missing = df.isna().sum()
    total_missing = int(missing.sum())

    print(f"Missing values: {total_missing:,}")

    if total_missing > 0:
        print("\nMissing values by column:")
        print(missing[missing > 0])
    else:
        print("Missing-value check: PASS")

    # Duplicate rows
    duplicates = int(df.duplicated().sum())
    print(f"Duplicate rows: {duplicates:,}")

    if duplicates == 0:
        print("Duplicate check: PASS")

    # Demand validation
    negative_demand = int((df["demand"] < 0).sum())

    print(f"Negative demand values: {negative_demand:,}")

    if negative_demand == 0:
        print("Demand validation: PASS")

    # Date validation
    invalid_dates = int(df["date"].isna().sum())

    print(f"Invalid dates: {invalid_dates:,}")

    if invalid_dates == 0:
        print("Date validation: PASS")

    # Basic date range
    print(f"Date range: {df['date'].min().date()} → {df['date'].max().date()}")

    # Cardinality
    print(f"Unique products: {df['item_id'].nunique():,}")
    print(f"Unique departments: {df['dept_id'].nunique():,}")
    print(f"Unique categories: {df['cat_id'].nunique():,}")
    print(f"Unique stores: {df['store_id'].nunique():,}")
    print(f"Unique states: {df['state_id'].nunique():,}")

    print(f"\n{dataset_name} validation completed.")

    return df


def main():
    train_df = validate_dataset(TRAIN_FILE, "TRAIN DATA")
    test_df = validate_dataset(TEST_FILE, "TEST DATA")

    print(f"\n{'=' * 60}")
    print("DATASET VALIDATION SUMMARY")
    print(f"{'=' * 60}")

    print(f"Training rows: {len(train_df):,}")
    print(f"Testing rows:  {len(test_df):,}")

    print("\nExpected columns:")
    for column in EXPECTED_COLUMNS:
        print(f"  ✓ {column}")

    print("\nData validation completed successfully.")


if __name__ == "__main__":
    main()