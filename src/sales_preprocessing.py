import pandas as pd


INPUT_PATH = "data/raw/sales_train_validation.csv"
OUTPUT_PATH = "data/raw/sales_long.csv"


def main():
    print("Loading sales data...")

    sales_df = pd.read_csv(INPUT_PATH)

    print(f"Original shape: {sales_df.shape}")

    id_columns = [
        "id",
        "item_id",
        "dept_id",
        "cat_id",
        "store_id",
        "state_id",
    ]

    sales_columns = [
        column for column in sales_df.columns
        if column.startswith("d_")
    ]

    print(f"Sales day columns: {len(sales_columns)}")

    print("Converting wide format to long format...")

    sales_long = sales_df.melt(
        id_vars=id_columns,
        value_vars=sales_columns,
        var_name="d",
        value_name="sales",
    )

    print(f"Long format shape: {sales_long.shape}")

    sales_long.to_csv(OUTPUT_PATH, index=False)

    print(f"Saved processed sales data to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
    