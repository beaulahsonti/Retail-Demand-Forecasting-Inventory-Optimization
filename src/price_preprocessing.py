import pandas as pd

INPUT_PATH = "data/raw/sell_prices.csv"
OUTPUT_PATH = "data/raw/prices_processed.csv"


def main():
    print("Loading sell-price data...")

    prices = pd.read_csv(INPUT_PATH)

    print(f"Original shape: {prices.shape}")

    # Convert price column to numeric
    prices["sell_price"] = pd.to_numeric(
        prices["sell_price"],
        errors="coerce"
    )

    # Check missing values
    print("\nMissing values:")
    print(prices.isnull().sum())

    # Remove invalid rows
    prices = prices.dropna(
        subset=["store_id", "item_id", "wm_yr_wk", "sell_price"]
    )

    # Remove duplicate store-item-week records
    prices = prices.drop_duplicates(
        subset=["store_id", "item_id", "wm_yr_wk"]
    )

    # Sort for easier joining and analysis
    prices = prices.sort_values(
        ["store_id", "item_id", "wm_yr_wk"]
    ).reset_index(drop=True)

    print(f"\nProcessed shape: {prices.shape}")

    print("\nProcessed columns:")
    print(prices.columns.tolist())

    print("\nPrice statistics:")
    print(prices["sell_price"].describe())

    prices.to_csv(OUTPUT_PATH, index=False)

    print(f"\nSaved processed price data to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()