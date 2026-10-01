import pandas as pd

# Load forecasting dataset
input_file = "data/processed/forecasting_dataset.csv"

df = pd.read_csv(input_file)

# Convert date column
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Convert sales to numeric
df["sales"] = pd.to_numeric(df["sales"], errors="coerce")

# Sort data
df = df.sort_values(
    by=["item", "store", "date"]
).reset_index(drop=True)

# Baseline forecast:
# Use previous day's sales as the prediction
df["baseline_forecast"] = (
    df.groupby(["item", "store"])["sales"].shift(1)
)

# Calculate absolute error
df["absolute_error"] = (
    df["sales"] - df["baseline_forecast"]
).abs()

# Remove rows where previous-day sales is unavailable
evaluation_df = df.dropna(
    subset=["baseline_forecast"]
).copy()

# Calculate MAE
mae = evaluation_df["absolute_error"].mean()

print("Baseline forecasting completed.")
print("Rows evaluated:", len(evaluation_df))
print("Mean Absolute Error (MAE):", mae)

# Save baseline forecast dataset
output_file = "data/processed/baseline_forecast.csv"

evaluation_df.to_csv(
    output_file,
    index=False
)

print("Saved to:", output_file)