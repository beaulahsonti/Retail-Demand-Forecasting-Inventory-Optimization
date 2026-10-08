import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Retail Demand Forecasting",
    layout="wide"
)

st.title("Retail Demand Forecasting & Inventory Optimization")

st.write(
    "Interactive dashboard for demand forecasting, "
    "model evaluation and inventory planning."
)

# Load files
forecast = pd.read_csv(
    "data/processed/lightgbm_forecast.csv"
)

evaluation = pd.read_csv(
    "data/processed/model_evaluation.csv"
)

inventory = pd.read_csv(
    "data/processed/inventory_replenishment.csv"
)

# Convert date
forecast["date"] = pd.to_datetime(
    forecast["date"],
    errors="coerce"
)

# -------------------------------
# KPI SECTION
# -------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sales",
    round(forecast["sales"].sum(), 2)
)

col2.metric(
    "Predicted Sales",
    round(forecast["predicted_sales"].sum(), 2)
)

col3.metric(
    "Best Model",
    evaluation.iloc[0]["model"]
)

col4.metric(
    "Reorder Point",
    round(inventory.iloc[0]["reorder_point"], 2)
)

# -------------------------------
# SALES CHART
# -------------------------------

st.subheader("Actual vs Predicted Sales")

chart_data = forecast[
    ["date", "sales", "predicted_sales"]
].set_index("date")

st.line_chart(chart_data)

# -------------------------------
# MODEL PERFORMANCE
# -------------------------------

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Retail Demand Forecasting",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------

forecast = pd.read_csv(
    "data/processed/lightgbm_forecast.csv"
)

evaluation = pd.read_csv(
    "data/processed/model_evaluation.csv"
)

inventory = pd.read_csv(
    "data/processed/inventory_replenishment.csv"
)

forecast["date"] = pd.to_datetime(
    forecast["date"],
    errors="coerce"
)

# -----------------------------
# TITLE
# -----------------------------

st.title("📊 Retail Demand Forecasting & Inventory Optimization")

st.write(
    "Interactive analytics dashboard for demand forecasting, "
    "model performance and inventory decision-making."
)

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------

st.sidebar.header("Dashboard Filters")

items = ["All"] + sorted(
    forecast["item"].dropna().unique().tolist()
)

selected_item = st.sidebar.selectbox(
    "Select Item",
    items
)

stores = ["All"] + sorted(
    forecast["store"].dropna().unique().tolist()
)

selected_store = st.sidebar.selectbox(
    "Select Store",
    stores
)

filtered = forecast.copy()

if selected_item != "All":
    filtered = filtered[
        filtered["item"] == selected_item
    ]

if selected_store != "All":
    filtered = filtered[
        filtered["store"] == selected_store
    ]

# -----------------------------
# KPI SECTION
# -----------------------------

st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Actual Sales",
    f"{filtered['sales'].sum():,.0f}"
)

col2.metric(
    "Predicted Sales",
    f"{filtered['predicted_sales'].sum():,.0f}"
)

best_model = evaluation.iloc[0]["model"]

col3.metric(
    "Best Model",
    best_model
)

col4.metric(
    "Reorder Point",
    f"{inventory.iloc[0]['reorder_point']:.2f}"
)

# -----------------------------
# SALES TREND
# -----------------------------

st.subheader("Actual vs Predicted Sales")

trend = (
    filtered
    .groupby("date")[["sales", "predicted_sales"]]
    .sum()
)

st.line_chart(trend)

# -----------------------------
# MODEL PERFORMANCE
# -----------------------------

st.subheader("Model Performance")

st.dataframe(
    evaluation,
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# INVENTORY SECTION
# -----------------------------

st.subheader("Inventory Replenishment")

inv_col1, inv_col2, inv_col3 = st.columns(3)

inv_col1.metric(
    "Daily Predicted Demand",
    f"{inventory.iloc[0]['predicted_daily_demand']:.2f}"
)

inv_col2.metric(
    "Safety Stock",
    f"{inventory.iloc[0]['safety_stock']:.2f}"
)

inv_col3.metric(
    "Recommended Order",
    f"{inventory.iloc[0]['recommended_order_quantity']:.2f}"
)

st.dataframe(
    inventory,
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# BUSINESS RECOMMENDATION
# -----------------------------

# -----------------------------
# WHAT-IF PRICE SCENARIO
# -----------------------------

st.subheader("💰 Price What-If Scenario")

current_price = st.number_input(
    "Current Price",
    min_value=0.0,
    value=10.0,
    step=0.5
)

price_change = st.slider(
    "Simulate Price Change (%)",
    min_value=-30,
    max_value=30,
    value=0,
    step=5
)

scenario_price = current_price * (
    1 + price_change / 100
)

# Simple demand sensitivity assumption
demand_change = -0.5 * (price_change / 100)

base_demand = filtered["predicted_sales"].mean()

scenario_demand = base_demand * (
    1 + demand_change
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Current Price",
    f"{current_price:.2f}"
)

col2.metric(
    "Scenario Price",
    f"{scenario_price:.2f}"
)

col3.metric(
    "Estimated Demand",
    f"{scenario_demand:.2f}"
)

st.info(
    "This scenario estimates demand impact based on "
    "the simulated price change."
)