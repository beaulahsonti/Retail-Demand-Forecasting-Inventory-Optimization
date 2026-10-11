import streamlit as st
import pandas as pd
import numpy as np
import os

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="RetailPulse | Inventory Intelligence",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background: #0b1120;
    color: #e5e7eb;
}

[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #1f2937;
}

[data-testid="stSidebar"] * {
    color: #d1d5db;
}

.main-title {
    font-size: 34px;
    font-weight: 800;
    letter-spacing: -1px;
    color: #f9fafb;
    margin-bottom: 2px;
}

.subtitle {
    color: #9ca3af;
    font-size: 15px;
    margin-bottom: 28px;
}

.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #f9fafb;
    margin-top: 30px;
    margin-bottom: 15px;
}

.kpi-card {
    background: linear-gradient(145deg, #111827, #172033);
    border: 1px solid #263244;
    border-radius: 14px;
    padding: 20px;
    min-height: 125px;
}

.kpi-label {
    color: #9ca3af;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.7px;
}

.kpi-value {
    color: #f9fafb;
    font-size: 28px;
    font-weight: 800;
    margin-top: 10px;
}

.kpi-sub {
    color: #6ee7b7;
    font-size: 12px;
    margin-top: 5px;
}

.alert-card {
    background: #1c1917;
    border: 1px solid #78350f;
    border-radius: 12px;
    padding: 16px;
}

.footer {
    text-align: center;
    color: #6b7280;
    font-size: 12px;
    margin-top: 45px;
    padding: 20px;
    border-top: 1px solid #1f2937;
}

div[data-testid="stMetric"] {
    background: transparent;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_inventory():
    path = "models/inventory_analysis.csv"

    if not os.path.exists(path):
        return pd.DataFrame()

    df = pd.read_csv(path)

    return df


@st.cache_data
def load_inventory_recommendations():
    path = "models/inventory_recommendations.csv"

    if not os.path.exists(path):
        return pd.DataFrame()

    return pd.read_csv(path)


@st.cache_data
def load_model_comparison():
    path = "models/model_comparison.csv"

    if not os.path.exists(path):
        return pd.DataFrame()

    return pd.read_csv(path)


@st.cache_data
def load_lightgbm():
    path = "models/lightgbm_predictions.csv"

    if not os.path.exists(path):
        return pd.DataFrame()

    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])

    return df


inventory = load_inventory()
recommendations = load_inventory_recommendations()
model_comparison = load_model_comparison()
lightgbm = load_lightgbm()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="font-size:26px;font-weight:800;color:#f9fafb;">
        📦 RetailPulse
        </div>
        <div style="color:#6b7280;font-size:12px;margin-bottom:25px;">
        Demand & Inventory Intelligence
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Dashboard Filters")

    if not inventory.empty:

        stores = sorted(
            inventory["store_id"].dropna().unique()
        )

        selected_stores = st.multiselect(
            "Store",
            stores,
            default=stores
        )

        priorities = sorted(
            inventory["inventory_priority"]
            .dropna()
            .astype(str)
            .unique()
        )

        selected_priorities = st.multiselect(
            "Inventory Priority",
            priorities,
            default=priorities
        )

        items = sorted(
            inventory["item_id"].dropna().unique()
        )

        selected_item = st.selectbox(
            "Item",
            ["All Items"] + items
        )

    else:
        selected_stores = []
        selected_priorities = []
        selected_item = "All Items"

    st.markdown("---")

    st.markdown(
        """
        **Project**

        Retail Demand Forecasting  
        & Inventory Optimization

        **Models**

        • Baseline  
        • Prophet  
        • LightGBM
        """
    )


# ============================================================
# FILTER DATA
# ============================================================

filtered_inventory = inventory.copy()

if not filtered_inventory.empty:

    if selected_stores:
        filtered_inventory = filtered_inventory[
            filtered_inventory["store_id"].isin(selected_stores)
        ]

    if selected_priorities:
        filtered_inventory = filtered_inventory[
            filtered_inventory["inventory_priority"]
            .astype(str)
            .isin(selected_priorities)
        ]

    if selected_item != "All Items":
        filtered_inventory = filtered_inventory[
            filtered_inventory["item_id"] == selected_item
        ]


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">RetailPulse</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Demand Forecasting & Inventory Intelligence Platform'
    '</div>',
    unsafe_allow_html=True
)


if inventory.empty:

    st.error(
        "Inventory data not found. Run the forecasting and inventory scripts first."
    )

    st.stop()


# ============================================================
# KPI SECTION
# ============================================================

st.markdown(
    '<div class="section-title">Executive Overview</div>',
    unsafe_allow_html=True
)

total_forecast = filtered_inventory["forecast_demand"].sum()
total_safety = filtered_inventory["safety_stock"].sum()
total_recommended = filtered_inventory[
    "recommended_inventory"
].sum()

items_count = filtered_inventory["item_id"].nunique()
stores_count = filtered_inventory["store_id"].nunique()

high_priority = filtered_inventory[
    filtered_inventory["inventory_priority"]
    .isin(["High", "Very High"])
].shape[0]


k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Forecast Demand</div>
            <div class="kpi-value">{total_forecast:,.0f}</div>
            <div class="kpi-sub">Forecast units</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Recommended Stock</div>
            <div class="kpi-value">{total_recommended:,.0f}</div>
            <div class="kpi-sub">Inventory units</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Safety Stock</div>
            <div class="kpi-value">{total_safety:,.0f}</div>
            <div class="kpi-sub">Protection buffer</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Items Monitored</div>
            <div class="kpi-value">{items_count:,}</div>
            <div class="kpi-sub">Product series</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k5:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Priority Alerts</div>
            <div class="kpi-value">{high_priority:,}</div>
            <div class="kpi-sub">High / Very High</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FORECASTING PERFORMANCE
# ============================================================

st.markdown(
    '<div class="section-title">Forecasting Performance</div>',
    unsafe_allow_html=True
)

if not model_comparison.empty:

    col1, col2 = st.columns([1.5, 1])

    with col1:

        chart_data = model_comparison.set_index("model")[
            ["MAE", "RMSE"]
        ]

        st.bar_chart(chart_data)

    with col2:

        st.dataframe(
            model_comparison,
            width="stretch",
            hide_index=True
        )


# ============================================================
# DEMAND FORECAST
# ============================================================

st.markdown(
    '<div class="section-title">Demand Forecast Monitor</div>',
    unsafe_allow_html=True
)

if not lightgbm.empty:

    forecast_data = lightgbm.copy()

    if selected_stores:
        forecast_data = forecast_data[
            forecast_data["store_id"].isin(selected_stores)
        ]

    if selected_item != "All Items":
        forecast_data = forecast_data[
            forecast_data["item_id"] == selected_item
        ]

    daily_forecast = (
        forecast_data
        .groupby("date")[["sales", "prediction"]]
        .sum()
        .rename(
            columns={
                "sales": "Actual Demand",
                "prediction": "Forecast Demand"
            }
        )
    )

    st.line_chart(
        daily_forecast,
        height=350
    )


# ============================================================
# INVENTORY ANALYTICS
# ============================================================

st.markdown(
    '<div class="section-title">Inventory Intelligence</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    priority_counts = (
        filtered_inventory[
            "inventory_priority"
        ]
        .value_counts()
        .reindex(
            ["Low", "Medium", "High", "Very High"],
            fill_value=0
        )
    )

    st.markdown("**Inventory Priority Distribution**")

    st.bar_chart(
        priority_counts,
        height=300
    )


with col2:

    top_reorder = (
        filtered_inventory
        .sort_values(
            "reorder_point",
            ascending=False
        )
        .head(10)
        .set_index("item_id")[
            ["reorder_point"]
        ]
    )

    st.markdown("**Top Reorder Points**")

    st.bar_chart(
        top_reorder,
        height=300
    )


# ============================================================
# INVENTORY ALERT
# ============================================================

high_items = filtered_inventory[
    filtered_inventory["inventory_priority"]
    .isin(["High", "Very High"])
].sort_values(
    "reorder_point",
    ascending=False
)

if not high_items.empty:

    st.markdown(
        '<div class="section-title">Inventory Alerts</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="alert-card">
        <b>{len(high_items)} item-store combinations</b>
        require elevated inventory protection based on the
        configured safety-stock analysis.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# RECOMMENDATION TABLE
# ============================================================

st.markdown(
    '<div class="section-title">Inventory Recommendations</div>',
    unsafe_allow_html=True
)

display_columns = [
    "item_id",
    "store_id",
    "average_demand",
    "forecast_demand",
    "safety_stock",
    "lead_time_demand",
    "reorder_point",
    "recommended_inventory",
    "inventory_priority"
]
display_df = (
    filtered_inventory
    .sort_values(
        "reorder_point",
        ascending=False
    )
    [display_columns]
    .head(25)
)

st.dataframe(
    display_df,
    hide_index=True,
    width="stretch"
)
# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        RetailPulse • Retail Demand Forecasting & Inventory Optimization
        <br>
        Built with Python • DuckDB • LightGBM • Prophet • Streamlit
    </div>
    """,
    unsafe_allow_html=True
)