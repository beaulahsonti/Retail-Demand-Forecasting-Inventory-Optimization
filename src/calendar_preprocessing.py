import pandas as pd

INPUT_PATH = "data/raw/calendar.csv"
OUTPUT_PATH = "data/raw/calendar_processed.csv"

# Keep state-specific SNAP flags intact for downstream state-level modeling.


def main():
    print("Loading calendar data...")

    calendar = pd.read_csv(INPUT_PATH)

    print(f"Original shape: {calendar.shape}")

    # Convert date column to datetime
    calendar["date"] = pd.to_datetime(calendar["date"])

    # Combine event information
    calendar["event_name"] = calendar["event_name_1"].fillna(
        calendar["event_name_2"]
    )

    calendar["event_type"] = calendar["event_type_1"].fillna(
        calendar["event_type_2"]
    )

    # Remove original event columns
    calendar = calendar.drop(
        columns=[
            "event_name_1",
            "event_type_1",
            "event_name_2",
            "event_type_2",
        ]
    )

    # Fill optional event fields
    calendar["event_name"] = calendar["event_name"].fillna("None")
    calendar["event_type"] = calendar["event_type"].fillna("None")

    # Keep state-specific SNAP indicators
    calendar["snap_CA"] = calendar["snap_CA"].astype(int)
    calendar["snap_TX"] = calendar["snap_TX"].astype(int)
    calendar["snap_WI"] = calendar["snap_WI"].astype(int)

    print(f"Processed shape: {calendar.shape}")

    print("\nMissing values:")
    print(calendar.isnull().sum())

    print("\nProcessed columns:")
    print(calendar.columns.tolist())

    calendar.to_csv(OUTPUT_PATH, index=False)

    print(f"\nSaved processed calendar to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()