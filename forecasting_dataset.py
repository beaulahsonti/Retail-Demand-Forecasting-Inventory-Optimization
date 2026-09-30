import pandas as pd

# Load processed sales data
input_file = "data/processed/Daily_sales_with_price.csv"

df = pd.read_csv(input_file, low_memory=False)

# Clean column names
df.columns = df.columns.str.strip().str.lower()

print("Columns found in CSV:")
print(df.columns.tolist())

# Select columns required for forecasting
forecasting_df = df[
    [
        "date",
        "item",
        "store",
        "sales",
        "price",
        "event",
        "event_type_1",
        "event_name_2",
        "event_type_2",
        "weekday",
        "year",
        "month",
        "week",
        "day",
        "wm_yr_wk"
    ]
].copy()

# Convert date column
forecasting_df["date"] = pd.to_datetime(
    forecasting_df["date"],
    errors="coerce"
)

# Sort data
forecasting_df = forecasting_df.sort_values(
    by=["item", "store", "date"]
)

# Check missing values
print("\nMissing values:")
print(forecasting_df.isnull().sum())

# Check zero-sales records
zero_sales = (forecasting_df["sales"] == 0).sum()

print("\nZero-sales records:", zero_sales)

# Sales statistics
print("\nSales statistics:")
print(forecasting_df["sales"].describe())

# Save forecasting dataset
output_file = "data/processed/forecasting_dataset.csv"

forecasting_df.to_csv(
    output_file,
    index=False
)

print("\nForecasting dataset created successfully.")
print("Rows:", len(forecasting_df))
print("Columns:", list(forecasting_df.columns))
print("Saved to:", output_file)