import streamlit as st
import pandas as pd
import os

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="RetailPulse",
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
    background: #0b0f19;
    color: #e5e7eb;
}

[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #263244;
}

[data-testid="stSidebar"] * {
    color: #d1d5db;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.brand {
    font-size: 34px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -1px;
}

.brand-sub {
    color: #8b95a7;
    font-size: 14px;
    margin-top: -5px;
    margin-bottom: 30px;
}

.section {
    font-size: 21px;
    font-weight: 700;
    color: #ffffff;
    margin-top: 28px;
    margin-bottom: 14px;
}

.kpi {
    background: linear-gradient(145deg, #121a29, #182234);
    border: 1px solid #263244;
    border-radius: 15px;
    padding: 20px;
    min-height: 125px;
}

.kpi-label {
    color: #8b95a7;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.kpi-value {
    color: #ffffff;
    font-size: 27px;
    font-weight: 800;
    margin-top: 8px;
}

.kpi-desc {
    color: #6ee7b7;
    font-size: 11px;
    margin-top: 5px;
}

.alert {
    background: #1f1712;
    border: 1px solid #854d0e;
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 10px;
}

.info {
    background: #111827;
    border: 1px solid #263244;
    border-radius: 12px;
    padding: 15px 18px;
}

.footer {
    text-align: center;
    color: #6b7280;
    font-size: 11px;
    margin-top: 45px;
    padding-top: 20px;
    border-top: 1px solid #1f2937;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_csv(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()


@st.cache_data
def load_forecast():
    path = "models/lightgbm_predictions.csv"

    if not os.path.exists(path):
        return pd.DataFrame()

    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])

    return df


inventory = load_csv(
    "models/inventory_analysis.csv"
)

recommendations = load_csv(
    "models/inventory_recommendations.csv"
)

comparison = load_csv(
    "models/model_comparison.csv"
)

forecast = load_forecast()


# ============================================================
# DATA CHECK
# ============================================================

if inventory.empty or comparison.empty or forecast.empty:

    st.error(
        "Required model files are missing. "
        "Run the forecasting and inventory scripts first."
    )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:26px;
            font-weight:800;
            color:white;
        ">
        📦 RetailPulse
        </div>

        <div style="
            color:#7f8a9d;
            font-size:12px;
            margin-bottom:28px;
        ">
        Demand & Inventory Intelligence
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Filters")

    stores = sorted(
        inventory["store_id"]
        .dropna()
        .unique()
    )

    selected_stores = st.multiselect(
        "Store",
        stores,
        default=stores
    )

    priorities = [
        "Low",
        "Medium",
        "High",
        "Very High"
    ]

    selected_priorities = st.multiselect(
        "Inventory Priority",
        priorities,
        default=priorities
    )

    items = sorted(
        inventory["item_id"]
        .dropna()
        .unique()
    )

    selected_item = st.selectbox(
        "Product",
        ["All Products"] + items
    )

    st.markdown("---")

    st.markdown(
        """
        **Pipeline**

        Data → Features → Forecast  
        → Evaluation → Inventory

        **Models**

        Baseline  
        Prophet  
        LightGBM
        """
    )


# ============================================================
# FILTER INVENTORY
# ============================================================

filtered = inventory.copy()

if selected_stores:
    filtered = filtered[
        filtered["store_id"].isin(selected_stores)
    ]

if selected_priorities:
    filtered = filtered[
        filtered["inventory_priority"]
        .astype(str)
        .isin(selected_priorities)
    ]

if selected_item != "All Products":
    filtered = filtered[
        filtered["item_id"] == selected_item
    ]


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="brand">RetailPulse</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="brand-sub">'
    'Retail Demand Forecasting & Inventory Optimization'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

series_count = len(filtered)

product_count = filtered["item_id"].nunique()

store_count = filtered["store_id"].nunique()

forecast_demand = filtered[
    "forecast_demand"
].sum()

safety_stock = filtered[
    "safety_stock"
].sum()

recommended_stock = filtered[
    "recommended_inventory"
].sum()

priority_alerts = filtered[
    filtered["inventory_priority"]
    .isin(["High", "Very High"])
].shape[0]


# ============================================================
# KPI CARDS
# ============================================================

k1, k2, k3, k4, k5, k6 = st.columns(6)

cards = [
    (
        k1,
        "ITEM-STORE SERIES",
        f"{series_count:,}",
        "Inventory series"
    ),
    (
        k2,
        "PRODUCTS",
        f"{product_count:,}",
        "Unique products"
    ),
    (
        k3,
        "STORES",
        f"{store_count:,}",
        "Active stores"
    ),
    (
        k4,
        "FORECAST DEMAND",
        f"{forecast_demand:,.0f}",
        "Forecast units"
    ),
    (
        k5,
        "SAFETY STOCK",
        f"{safety_stock:,.0f}",
        "Protection buffer"
    ),
    (
        k6,
        "PRIORITY ALERTS",
        f"{priority_alerts:,}",
        "High / Very High"
    )
]

for col, label, value, desc in cards:

    with col:

        st.markdown(
            f"""
            <div class="kpi">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-desc">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3 = st.tabs(
    [
        "Overview",
        "Forecasting",
        "Inventory Intelligence"
    ]
)


# ============================================================
# OVERVIEW
# ============================================================

with tab1:

    st.markdown(
        '<div class="section">Inventory Command Center</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns(2)

    # --------------------------------------------------------
    # PRIORITY DISTRIBUTION
    # --------------------------------------------------------

    with left:

        st.markdown("#### Inventory Priority")

        priority_data = (
            filtered[
                "inventory_priority"
            ]
            .value_counts()
            .reindex(
                priorities,
                fill_value=0
            )
        )

        st.bar_chart(
            priority_data,
            height=300
        )

    # --------------------------------------------------------
    # TOP REORDER POINTS
    # --------------------------------------------------------

    with right:

        st.markdown("#### Highest Reorder Points")

        top_reorder = (
            filtered
            .sort_values(
                "reorder_point",
                ascending=False
            )
            .head(10)
            .copy()
        )

        top_reorder["series"] = (
            top_reorder["item_id"]
            + " | "
            + top_reorder["store_id"]
        )

        chart = (
            top_reorder
            .set_index("series")[
                ["reorder_point"]
            ]
        )

        st.bar_chart(
            chart,
            height=300
        )

    # --------------------------------------------------------
    # ALERTS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section">Inventory Alerts</div>',
        unsafe_allow_html=True
    )

    alerts = (
        filtered[
            filtered["inventory_priority"]
            .isin(["High", "Very High"])
        ]
        .sort_values(
            "reorder_point",
            ascending=False
        )
        .head(8)
    )

    if alerts.empty:

        st.markdown(
            """
            <div class="info">
            No high-priority inventory alerts under the
            current filters.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        for _, row in alerts.iterrows():

            st.markdown(
                f"""
                <div class="alert">
                    <b>{row["item_id"]}</b>
                    &nbsp; | &nbsp;
                    Store <b>{row["store_id"]}</b>
                    <br>
                    Reorder Point:
                    <b>{row["reorder_point"]:,.0f}</b>
                    &nbsp;&nbsp;
                    Safety Stock:
                    <b>{row["safety_stock"]:,.0f}</b>
                    &nbsp;&nbsp;
                    Priority:
                    <b>{row["inventory_priority"]}</b>
                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# FORECASTING TAB
# ============================================================

with tab2:

    st.markdown(
        '<div class="section">Demand Forecast Monitor</div>',
        unsafe_allow_html=True
    )

    forecast_filtered = forecast.copy()

    if selected_stores:

        forecast_filtered = forecast_filtered[
            forecast_filtered["store_id"]
            .isin(selected_stores)
        ]

    if selected_item != "All Products":

        forecast_filtered = forecast_filtered[
            forecast_filtered["item_id"]
            == selected_item
        ]

    daily = (
        forecast_filtered
        .groupby("date")[
            ["sales", "prediction"]
        ]
        .sum()
        .rename(
            columns={
                "sales": "Actual Demand",
                "prediction": "LightGBM Forecast"
            }
        )
    )

    st.markdown("#### Actual vs Forecast Demand")

    st.line_chart(
        daily,
        height=400
    )

    st.markdown(
        '<div class="section">Model Performance</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns([1.4, 1])

    with c1:

        performance = comparison.set_index(
            "model"
        )[["MAE", "RMSE"]]

        st.bar_chart(
            performance,
            height=330
        )

    with c2:

        st.dataframe(
            comparison,
            use_container_width=True,
            hide_index=True
        )

        st.markdown(
            """
            <div class="info">
            Lower MAE and RMSE indicate lower forecast
            error on the evaluated test split.
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# INVENTORY TAB
# ============================================================

with tab3:

    st.markdown(
        '<div class="section">Inventory Optimization</div>',
        unsafe_allow_html=True
    )

    inventory_cols = [
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

    table = (
        filtered
        .sort_values(
            "reorder_point",
            ascending=False
        )
        [inventory_cols]
    )

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True,
        height=500
    )

    st.markdown(
        '<div class="section">Inventory Metrics</div>',
        unsafe_allow_html=True
    )

    a, b, c = st.columns(3)

    with a:

        st.metric(
            "Recommended Inventory",
            f"{recommended_stock:,.0f}"
        )

    with b:

        st.metric(
            "Forecast Demand",
            f"{forecast_demand:,.0f}"
        )

    with c:

        st.metric(
            "Safety Stock",
            f"{safety_stock:,.0f}"
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        RetailPulse
        • Retail Demand Forecasting & Inventory Optimization
        <br>
        Python • DuckDB • Prophet • LightGBM • Streamlit
    </div>
    """,
    unsafe_allow_html=True
)