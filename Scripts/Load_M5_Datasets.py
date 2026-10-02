# ============================================================
# M5 DATA EXTRACTION AND LOADING SCRIPT
# ============================================================
#
# Objective:
# Extract the raw M5 Forecasting Dataset from local CSV files
# and load it into Snowflake.
#
# Dataset:
# M5 Forecasting Dataset (Walmart)
#
# Raw files:
# 1. calendar.csv
# 2. sales_train_validation.csv
# 3. sell_prices.csv
# 4. sales_train_evaluation.csv
#
# Destination:
# Snowflake
# Database: RETAIL_DEMAND
# Schema: PUBLIC
#
# ============================================================


# ============================================================
# 1. IMPORT REQUIRED LIBRARIES
# ============================================================

import pandas as pd
import snowflake.connector


# ============================================================
# 2. SNOWFLAKE CONNECTION
# ============================================================
#
# Establish a connection between Python and Snowflake.
#
# IMPORTANT:
# Do NOT hard-code your Snowflake password in a GitHub file.
# Use environment variables or another secure method.
#
# ============================================================

import os

conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse="COMPUTE_WH",
    database="RETAIL_DEMAND",
    schema="PUBLIC",
    role="ACCOUNTADMIN"
)

print("Connected to Snowflake successfully.")


# ============================================================
# 3. DEFINE LOCAL FILE PATHS
# ============================================================
#
# These paths point to the raw M5 CSV files downloaded from
# the M5 Forecasting Dataset.
#
# Change these paths according to where the files are stored
# on your computer.
#
# ============================================================

DATA_PATH = r"C:\Users\RATHICK A\OneDrive\Desktop\DA_P2\Retail-Demand-Forecasting-Inventory-Optimization\Data"

calendar_file = f"{DATA_PATH}\\calendar.csv"
sales_validation_file = f"{DATA_PATH}\\sales_train_validation.csv"
sell_prices_file = f"{DATA_PATH}\\sell_prices.csv"
sales_evaluation_file = f"{DATA_PATH}\\sales_train_evaluation.csv"


# ============================================================
# 4. EXTRACT RAW DATA
# ============================================================
#
# Read the CSV files into pandas DataFrames.
#
# At this stage, we are not transforming the data.
# The purpose is to extract the raw dataset as provided.
#
# ============================================================

calendar_df = pd.read_csv(calendar_file)

sales_validation_df = pd.read_csv(
    sales_validation_file
)

sell_prices_df = pd.read_csv(
    sell_prices_file
)

sales_evaluation_df = pd.read_csv(
    sales_evaluation_file
)


# ============================================================
# 5. BASIC EXTRACTION CHECK
# ============================================================
#
# Display the dimensions of each dataset.
#
# Expected:
# calendar.csv                  → 1969 rows
# sales_train_validation.csv   → 30490 rows
# sell_prices.csv              → 6841121 rows
# sales_train_evaluation.csv   → 30490 rows
#
# ============================================================

print("\nDataset dimensions:")

print(
    "Calendar:",
    calendar_df.shape
)

print(
    "Sales Validation:",
    sales_validation_df.shape
)

print(
    "Sell Prices:",
    sell_prices_df.shape
)

print(
    "Sales Evaluation:",
    sales_evaluation_df.shape
)


# ============================================================
# 6. LOAD RAW DATA INTO SNOWFLAKE
# ============================================================
#
# The Snowflake connector's write_pandas() function is used
# to upload pandas DataFrames into Snowflake tables.
#
# These tables represent the RAW layer of the project.
#
# ============================================================

from snowflake.connector.pandas_tools import write_pandas


# ------------------------------------------------------------
# Load Calendar
# ------------------------------------------------------------

success, nchunks, nrows, _ = write_pandas(
    conn,
    calendar_df,
    "RAW_CALENDAR",
    auto_create_table=True,
    overwrite=True
)

print(
    f"RAW_CALENDAR loaded: {nrows} rows"
)


# ------------------------------------------------------------
# Load Sales Validation
# ------------------------------------------------------------

success, nchunks, nrows, _ = write_pandas(
    conn,
    sales_validation_df,
    "RAW_SALES_TRAIN_VALIDATION",
    auto_create_table=True,
    overwrite=True
)

print(
    f"RAW_SALES_TRAIN_VALIDATION loaded: {nrows} rows"
)


# ------------------------------------------------------------
# Load Sell Prices
# ------------------------------------------------------------

success, nchunks, nrows, _ = write_pandas(
    conn,
    sell_prices_df,
    "RAW_SELL_PRICES",
    auto_create_table=True,
    overwrite=True
)

print(
    f"RAW_SELL_PRICES loaded: {nrows} rows"
)


# ------------------------------------------------------------
# Load Sales Evaluation
# ------------------------------------------------------------

success, nchunks, nrows, _ = write_pandas(
    conn,
    sales_evaluation_df,
    "RAW_SALES_TRAIN_EVALUATION",
    auto_create_table=True,
    overwrite=True
)

print(
    f"RAW_SALES_TRAIN_EVALUATION loaded: {nrows} rows"
)


# ============================================================
# 7. CLOSE SNOWFLAKE CONNECTION
# ============================================================

conn.close()

print("\nSnowflake connection closed.")
print("M5 raw data loading completed successfully.")

