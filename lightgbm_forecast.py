import pandas as pd
import lightgbm as lgb
from sklearn.metrics import mean_absolute_error

# Load forecasting dataset
input_file = "data/processed/forecasting_dataset.csv"

df = pd.read_csv(input_file, low_memory=False)

# Convert columns
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["sales"] = pd.to_numeric(df["sales"], errors="coerce")
df["price"] = pd.to_numeric(df["price"], errors="coerce")

# Sort data
df = df.sort_values(
    by=["item", "store", "date"]
).reset_index(drop=True)

# Create time features
df["weekday_num"] = df["date"].dt.weekday
df["month_num"] = df["date"].dt.month

# Create lag features
group = df.groupby(["item", "store"])["sales"]

df["lag_1"] = group.shift(1)
df["lag_7"] = group.shift(7)
df["lag_14"] = group.shift(14)
df["lag_28"] = group.shift(28)

# Rolling features
df["rolling_mean_7"] = group.transform(
    lambda x: x.shift(1).rolling(7).mean()
)

df["rolling_mean_28"] = group.transform(
    lambda x: x.shift(1).rolling(28).mean()
)

# Event feature
df["event_flag"] = (
    df["event"]
    .fillna("No Event")
    .ne("No Event")
    .astype(int)
)

# Model features
features = [
    "lag_1",
    "lag_7",
    "lag_14",
    "lag_28",
    "rolling_mean_7",
    "rolling_mean_28",
    "price",
    "weekday_num",
    "month_num",
    "event_flag"
]

# Remove rows without enough history
model_df = df.dropna(
    subset=features + ["sales"]
).copy()

# Time-based split
split_date = model_df["date"].quantile(0.8)

train = model_df[
    model_df["date"] <= split_date
]

test = model_df[
    model_df["date"] > split_date
]

X_train = train[features]
y_train = train["sales"]

X_test = test[features]
y_test = test["sales"]

# Train LightGBM model
model = lgb.LGBMRegressor(
    n_estimators=200,
    learning_rate=0.05,
    num_leaves=31,
    random_state=42
)

model.fit(
    X_train,
    y_train
)

# Predict
predictions = model.predict(X_test)

# Evaluate
mae = mean_absolute_error(
    y_test,
    predictions
)

print("LightGBM forecasting completed.")
print("Training rows:", len(train))
print("Testing rows:", len(test))
print("Mean Absolute Error (MAE):", mae)

# Save predictions
results = test[
    ["date", "item", "store", "sales"]
].copy()

results["predicted_sales"] = predictions

output_file = "data/processed/lightgbm_forecast.csv"

results.to_csv(
    output_file,
    index=False
)

print("Saved to:", output_file)