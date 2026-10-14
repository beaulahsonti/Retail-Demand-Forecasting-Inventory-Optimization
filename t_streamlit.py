[1mdiff --git a/test_streamlit.py b/test_streamlit.py[m
[1mindex 3e1271e..a5b290e 100644[m
[1m--- a/test_streamlit.py[m
[1m+++ b/test_streamlit.py[m
[36m@@ -1,20 +1,698 @@[m
 import streamlit as st[m
[32m+[m[32mimport pandas as pd[m
[32m+[m[32mimport os[m
[32m+[m
[32m+[m[32m# ============================================================[m
[32m+[m[32m# PAGE CONFIG[m
[32m+[m[32m# ============================================================[m
 [m
 st.set_page_config([m
[31m-    page_title="Test",[m
[31m-    layout="wide"[m
[32m+[m[32m    page_title="RetailPulse",[m
[32m+[m[32m    page_icon="📦",[m
[32m+[m[32m    layout="wide",[m
[32m+[m[32m    initial_sidebar_state="expanded"[m
[32m+[m[32m)[m
[32m+[m
[32m+[m[32m# ============================================================[m
[32m+[m[32m# CUSTOM CSS[m
[32m+[m[32m# ============================================================[m
[32m+[m
[32m+[m[32mst.markdown("""[m
[32m+[m[32m<style>[m
[32m+[m
[32m+[m[32m.stApp {[m
[32m+[m[32m    background: #0b0f19;[m
[32m+[m[32m    color: #e5e7eb;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m[data-testid="stSidebar"] {[m
[32m+[m[32m    background: #111827;[m
[32m+[m[32m    border-right: 1px solid #263244;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m[data-testid="stSidebar"] * {[m
[32m+[m[32m    color: #d1d5db;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.block-container {[m
[32m+[m[32m    padding-top: 2rem;[m
[32m+[m[32m    padding-bottom: 3rem;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.brand {[m
[32m+[m[32m    font-size: 34px;[m
[32m+[m[32m    font-weight: 800;[m
[32m+[m[32m    color: #ffffff;[m
[32m+[m[32m    letter-spacing: -1px;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.brand-sub {[m
[32m+[m[32m    color: #8b95a7;[m
[32m+[m[32m    font-size: 14px;[m
[32m+[m[32m    margin-top: -5px;[m
[32m+[m[32m    margin-bottom: 30px;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.section {[m
[32m+[m[32m    font-size: 21px;[m
[32m+[m[32m    font-weight: 700;[m
[32m+[m[32m    color: #ffffff;[m
[32m+[m[32m    margin-top: 28px;[m
[32m+[m[32m    margin-bottom: 14px;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.kpi {[m
[32m+[m[32m    background: linear-gradient(145deg, #121a29, #182234);[m
[32m+[m[32m    border: 1px solid #263244;[m
[32m+[m[32m    border-radius: 15px;[m
[32m+[m[32m    padding: 20px;[m
[32m+[m[32m    min-height: 125px;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.kpi-label {[m
[32m+[m[32m    color: #8b95a7;[m
[32m+[m[32m    font-size: 12px;[m
[32m+[m[32m    font-weight: 700;[m
[32m+[m[32m    text-transform: uppercase;[m
[32m+[m[32m    letter-spacing: 0.8px;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.kpi-value {[m
[32m+[m[32m    color: #ffffff;[m
[32m+[m[32m    font-size: 27px;[m
[32m+[m[32m    font-weight: 800;[m
[32m+[m[32m    margin-top: 8px;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.kpi-desc {[m
[32m+[m[32m    color: #6ee7b7;[m
[32m+[m[32m    font-size: 11px;[m
[32m+[m[32m    margin-top: 5px;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.alert {[m
[32m+[m[32m    background: #1f1712;[m
[32m+[m[32m    border: 1px solid #854d0e;[m
[32m+[m[32m    border-radius: 12px;[m
[32m+[m[32m    padding: 16px 18px;[m
[32m+[m[32m    margin-bottom: 10px;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.info {[m
[32m+[m[32m    background: #111827;[m
[32m+[m[32m    border: 1px solid #263244;[m
[32m+[m[32m    border-radius: 12px;[m
[32m+[m[32m    padding: 15px 18px;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.footer {[m
[32m+[m[32m    text-align: center;[m
[32m+[m[32m    color: #6b7280;[m
[32m+[m[32m    font-size: 11px;[m
[32m+[m[32m    margin-top: 45px;[m
[32m+[m[32m    padding-top: 20px;[m
[32m+[m[32m    border-top: 1px solid #1f2937;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m</style>[m
[32m+[m[32m""", unsafe_allow_html=True)[m
[32m+[m
[32m+[m
[32m+[m[32m# ============================================================[m
[32m+[m[32m# DATA LOADING[m
[32m+[m[32m# ============================================================[m
[32m+[m
[32m+[m[32m@st.cache_data[m
[32m+[m[32mdef load_csv(path):[m
[32m+[m[32m    if os.path.exists(path):[m
[32m+[m[32m        return pd.read_csv(path)[m
[32m+[m[32m    return pd.DataFrame()[m
[32m+[m
[32m+[m
[32m+[m[32m@st.cache_data[m
[32m+[m[32mdef load_forecast():[m
[32m+[m[32m    path = "models/lightgbm_predictions.csv"[m
[32m+[m
[32m+[m[32m    if not os.path.exists(path):[m
[32m+[m[32m        return pd.DataFrame()[m
[32m+[m
[32m+[m[32m    df = pd.read_csv(path)[m
[32m+[m[32m    df["date"] = pd.to_datetime(df["date"])[m
[32m+[m
[32m+[m[32m    return df[m
[32m+[m
[32m+[m
[32m+[m[32minventory = load_csv([m
[32m+[m[32m    "models/inventory_analysis.csv"[m
[32m+[m[32m)[m
[32m+[m
[32m+[m[32mrecommendations = load_csv([m
[32m+[m[32m    "models/inventory_recommendations.csv"[m
[32m+[m[32m)[m
[32m+[m
[32m+[m[32mcomparison = load_csv([m
[32m+[m[32m    "models/model_comparison.csv"[m
[32m+[m[32m)[m
[32m+[m
[32m+[m[32mforecast = load_forecast()[m
[32m+[m
[32m+[m
[32m+[m[32m# ============================================================[m
[32m+[m[32m# DATA CHECK[m
[32m+[m[32m# ============================================================[m
[32m+[m
[32m+[m[32mif inventory.empty or comparison.empty or forecast.empty:[m
[32m+[m
[32m+[m[32m    st.error([m
[32m+[m[32m        "Required model files are missing. "[m
[32m+[m[32m        "Run the forecasting and inventory scripts first."[m
[32m+[m[32m    )[m
[32m+[m
[32m+[m[32m    st.stop()[m
[32m+[m
[32m+[m
[32m+[m[32m# ============================================================[m
[32m+[m[32m# SIDEBAR[m
[32m+[m[32m# ============================================================[m
[32m+[m
[32m+[m[32mwith st.sidebar:[m
[32m+[m
[32m+[m[32m    st.markdown([m
[32m+[m[32m        """[m
[32m+[m[32m        <div style="[m
[32m+[m[32m            font-size:26px;[m
[32m+[m[32m            font-weight:800;[m
[32m+[m[32m            color:white;[m
[32m+[m[32m        ">[m
[32m+[m[32m        📦 RetailPulse[m
[32m+[m[32m        </div>[m
[32m+[m
[32m+[m[32m        <div style="[m
[32m+[m[32m            color:#7f8a9d;[m
[32m+[m[32m            font-size:12px;[m
[32m+[m[32m            margin-bottom:28px;[m
[32m+[m[32m        ">[m
[32m+[m[32m        Demand & Inventory Intelligence[m
[32m+[m[32m        </div>[m
[32m+[m[32m        """,[m
[32m+[m[32m        unsafe_allow_html=True[m
[32m+[m[32m    )[m
[32m+[m
[32m+[m[32m    st.markdown("### Filters")[m
[32m+[m
[32m+[m[32m    stores = sorted([m
[32m+[m[32m        inventory["store_id"][m
[32m+[m[32m        .dropna()[m
[32m+[m[32m        .unique()[m
[32m+[m[32m    )[m
[32m+[m
[32m+[m[32m    selected_stores = st.multiselect([m
[32m+[m[32m        "Store",[m
[32m+[m[32m        stores,[m
[32m+[m[32m        default=stores[m
[32m+[m[32m    )[m
[32m+[m
[32m+[m[32m    priorities = [[m
[32m+[m[32m        "Low",[m
[32m+[m[32m        "Medium",[m
[32m+[m[32m        "High",[m
[32m+[m[32m        "Very High"[m
[32m+[m[32m    ][m
[32m+[m
[32m+[m[32m    selected_priorities = st.multiselect([m
[32m+[m[32m        "Inventory Priority",[m
[32m+[m[32m        priorities,[m
[32m+[m[32m        default=priorities[m
[32m+[m[32m    )[m
[32m+[m
[32m+[m[32m    items = sorted([m
[32m+[m[32m        inventory["item_id"][m
[32m+[m[32m        .dropna()[m
[32m+[m[32m        .unique()[m
[32m+[m[32m    )[m
[32m+[m
[32m+[m[32m    selected_item = st.selectbox([m
[32m+[m[32m        "Product",[m
[32m+[m[32m        ["All Products"] + items[m
[32m+[m[32m    )[m
[32m+[m
[32m+[m[32m    st.markdown("---")[m
[32m+[m
[32m+[m[32m    st.markdown([m
[32m+[m[32m        """[m
[32m+[m[32m        **Pipeline**[m
[32m+[m
[32m+[m[32m        Data → Features → Forecast[m[41m  [m
[32m+[m[32m        → Evaluation → Inventory[m
[32m+[m
[32m+[m[32m        **Models**[m
[32m+[m
[32m+[m[32m        Baseline[m[41m  [m
[32m+[m[32m        Prophet[m[41m  [m
[32m+[m[32m        LightGBM[m
[32m+[m[32m        """[m
[32m+[m[32m    )[m
[32m+[m
[32m+[m
[32m+[m[32m# ============================================================[m
[32m+[m[32m# FILTER INVENTORY[m
[32m+[m[32m# ============================================================[m
[32m+[m
[32m+[m[32mfiltered = inventory.copy()[m
[32m+[m
[32m+[m[32mif selected_stores:[m
[32m+[m[32m    filtered = filtered[[m
[32m+[m[32m        filtered["store_id"].isin(selected_stores)[m
[32m+[m[32m    ][m
[32m+[m
[32m+[m[32mif selected_priorities:[m
[32m+[m[32m    filtered = filtered[[m
[32m+[m[32m        filtered["inventory_priority"][m
[32m+[m[32m        .astype(str)[m
[32m+[m[32m        .isin(selected_priorities)[m
[32m+[m[32m    ][m
[32m+[m
[32m+[m[32mif selected_item != "All Products":[m
[32m+[m[32m    filtered = filtered[[m
[32m+[m[32m        filtered["item_id"] == selected_item[m
[32m+[m[32m    ][m
[32m+[m
[32m+[m
[32m+[m[32m# ============================================================[m
[32m+[m[32m# HEADER[m
[32m+[m[32m# ============================================================[m
[32m+[m
[32m+[m[32mst.markdown([m
[32m+[m[32m    '<div class="brand">RetailPulse</div>',[m
[32m+[m[32m    unsafe_allow_html=True[m
[32m+[m[32m)[m
[32m+[m
[32m+[m[32mst.markdown([m
[32m+[m[32m    '<div class="brand-sub">'[m
[32m+[m[32m    'Retail Demand Forecasting & Inventory Optimization'[m
[32m+[m[32m    '</div>',[m
[32m+[m[32m    unsafe_allow_html=True[m
[32m+[m[32m)[m
[32m+[m
[32m+[m
[32m+[m[32m# ============================================================[m
[32m+[m[32m# KPI CALCULATIONS[m
[32m+[m[32m# ============================================================[m
[32m+[m
[32m+[m[32mseries_count = len(filtered)[m
[32m+[m
[32m+[m[32mproduct_count = filtered["item_id"].nunique()[m
[32m+[m
[32m+[m[32mstore_count = filtered["store_id"].nunique()[m
[32m+[m
[32m+[m[32mforecast_demand = filtered[[m
[32m+[m[32m    "forecast_demand"[m
[32m+[m[32m].sum()[m
[32m+[m
[32m+[m[32msafety_stock = filtered[[m
[32m+[m[32m    "safety_stock"[m
[32m+[m[32m].sum()[m
[32m+[m
[32m+[m[32mrecommended_stock = filtered[[m
[32m+[m[32m    "recommended_inventory"[m
[32m+[m[32m].sum()[m
[32m+[m
[32m+[m[32mpriority_alerts = filtered[[m
[32m+[m[32m    filtered["inventory_priority"][m
[32m+[m[32m    .isin(["High", "Very High"])[m
[32m+[m[32m].shape[0][m
[32m+[m
[32m+[m
[32m+[m[32m# ============================================================[m
[32m+[m[32m# KPI CARDS[m
[32m+[m[32m# ============================================================[m
[32m+[m
[32m+[m[32mk1, k2, k3, k4, k5, k6 = st.columns(6)[m
[32m+[m
[32m+[m[32mcards = [[m
[32m+[m[32m    ([m
[32m+[m[32m        k1,[m
[32m+[m[32m        "ITEM-STORE SERIES",[m
[32m+[m[32m        f"{series_count:,}",[m
[32m+[m[32m        "Inventory series"[m
[32m+[m[32m    ),[m
[32m+[m[32m    ([m
[32m+[m[32m        k2,[m
[32m+[m[32m        "PRODUCTS",[m
[32m+[m[32m        f"{product_count:,}",[m
[32m+[m[32m        "Unique products"[m
[32m+[m[32m    ),[m
[32m+[m[32m    ([m
[32m+[m[32m        k3,[m
[32m+[m[32m        "STORES",[m
[32m+[m[32m        f"{store_count:,}",[m
[32m+[m[32m        "Active stores"[m
[32m+[m[32m    ),[m
[32m+[m[32m    ([m
[32m+[m[32m        k4,[m
[32m+[m[32m        "FORECAST DEMAND",[m
[32m+[m[32m        f"{forecast_demand:,.0f}",[m
[32m+[m[32m        "Forecast units"[m
[32m+[m[32m    ),[m
[32m+[m[32m    ([m
[32m+[m[32m        k5,[m
[32m+[m[32m        "SAFETY STOCK",[m
[32m+[m[32m        f"{safety_stock:,.0f}",[m
[32m+[m[32m        "Protection buffer"[m
[32m+[m[32m    ),[m
[32m+[m[32m    ([m
[32m+[m[32m        k6,[m
[32m+[m[32m        "PRIORITY ALERTS",[m
[32m+[m[32m        f"{priority_alerts:,}",[m
[32m+[m[32m        "High / Very High"[m
[32m+[m[32m    )[m
[32m+[m[32m][m
[32m+[m
[32m+[m[32mfor col, label, value, desc in cards:[m
[32m+[m
[32m+[m[32m    with col:[m
[32m+[m
[32m+[m[32m        st.markdown([m
[32m+[m[32m            f"""[m
[32m+[m[32m            <div class="kpi">[m
[32m+[m[32m                <div class="kpi-label">{label}</div>[m
[32m+[m[32m                <div class="kpi-value">{value}</div>[m
[32m+[m[32m                <div class="kpi-desc">{desc}</div>[m
[32m+[m[32m            </div>[m
[32m+[m[32m            """,[m
[32m+[m[32m            unsafe_allow_html=True[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m
[32m+[m[32m# ============================================================[m
[32m+[m[32m# TABS[m
[32m+[m[32m# ============================================================[m
[32m+[m
[32m+[m[32mtab1, tab2, tab3 = st.tabs([m
[32m+[m[32m    [[m
[32m+[m[32m        "Overview",[m
[32m+[m[32m        "Forecasting",[m
[32m+[m[32m        "Inventory Intelligence"[m
[32m+[m[32m    ][m
 )[m
 [m
[31m-st.title("RetailPulse Test")[m
[31m-st.write("Streamlit is working correctly.")[m
 [m
[31m-col1, col2, col3 = st.columns(3)[m
[32m+[m[32m# ============================================================[m
[32m+[m[32m# OVERVIEW[m
[32m+[m[32m# ============================================================[m
[32m+[m
[32m+[m[32mwith tab1:[m
[32m+[m
[32m+[m[32m    st.markdown([m
[32m+[m[32m        '<div class="section">Inventory Command Center</div>',[m
[32m+[m[32m        unsafe_allow_html=True[m
[32m+[m[32m    )[m
[32m+[m
[32m+[m[32m    left, right = st.columns(2)[m
[32m+[m
[32m+[m[32m    # --------------------------------------------------------[m
[32m+[m[32m    # PRIORITY DISTRIBUTION[m
[32m+[m[32m    # --------------------------------------------------------[m
[32m+[m
[32m+[m[32m    with left:[m
[32m+[m
[32m+[m[32m        st.markdown("#### Inventory Priority")[m
[32m+[m
[32m+[m[32m        priority_data = ([m
[32m+[m[32m            filtered[[m
[32m+[m[32m                "inventory_priority"[m
[32m+[m[32m            ][m
[32m+[m[32m            .value_counts()[m
[32m+[m[32m            .reindex([m
[32m+[m[32m                priorities,[m
[32m+[m[32m                fill_value=0[m
[32m+[m[32m            )[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m        st.bar_chart([m
[32m+[m[32m            priority_data,[m
[32m+[m[32m            height=300[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m    # --------------------------------------------------------[m
[32m+[m[32m    # TOP REORDER POINTS[m
[32m+[m[32m    # --------------------------------------------------------[m
[32m+[m
[32m+[m[32m    with right:[m
[32m+[m
[32m+[m[32m        st.markdown("#### Highest Reorder Points")[m
[32m+[m
[32m+[m[32m        top_reorder = ([m
[32m+[m[32m            filtered[m
[32m+[m[32m            .sort_values([m
[32m+[m[32m                "reorder_point",[m
[32m+[m[32m                ascending=False[m
[32m+[m[32m            )[m
[32m+[m[32m            .head(10)[m
[32m+[m[32m            .copy()[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m        top_reorder["series"] = ([m
[32m+[m[32m            top_reorder["item_id"][m
[32m+[m[32m            + " | "[m
[32m+[m[32m            + top_reorder["store_id"][m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m        chart = ([m
[32m+[m[32m            top_reorder[m
[32m+[m[32m            .set_index("series")[[m
[32m+[m[32m                ["reorder_point"][m
[32m+[m[32m            ][m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m        st.bar_chart([m
[32m+[m[32m            chart,[m
[32m+[m[32m            height=300[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m    # --------------------------------------------------------[m
[32m+[m[32m    # ALERTS[m
[32m+[m[32m    # --------------------------------------------------------[m
[32m+[m
[32m+[m[32m    st.markdown([m
[32m+[m[32m        '<div class="section">Inventory Alerts</div>',[m
[32m+[m[32m        unsafe_allow_html=True[m
[32m+[m[32m    )[m
[32m+[m
[32m+[m[32m    alerts = ([m
[32m+[m[32m        filtered[[m
[32m+[m[32m            filtered["inventory_priority"][m
[32m+[m[32m            .isin(["High", "Very High"])[m
[32m+[m[32m        ][m
[32m+[m[32m        .sort_values([m
[32m+[m[32m            "reorder_point",[m
[32m+[m[32m            ascending=False[m
[32m+[m[32m        )[m
[32m+[m[32m        .head(8)[m
[32m+[m[32m    )[m
[32m+[m
[32m+[m[32m    if alerts.empty:[m
[32m+[m
[32m+[m[32m        st.markdown([m
[32m+[m[32m            """[m
[32m+[m[32m            <div class="info">[m
[32m+[m[32m            No high-priority inventory alerts under the[m
[32m+[m[32m            current filters.[m
[32m+[m[32m            </div>[m
[32m+[m[32m            """,[m
[32m+[m[32m            unsafe_allow_html=True[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m    else:[m
[32m+[m
[32m+[m[32m        for _, row in alerts.iterrows():[m
[32m+[m
[32m+[m[32m            st.markdown([m
[32m+[m[32m                f"""[m
[32m+[m[32m                <div class="alert">[m
[32m+[m[32m                    <b>{row["item_id"]}</b>[m
[32m+[m[32m                    &nbsp; | &nbsp;[m
[32m+[m[32m                    Store <b>{row["store_id"]}</b>[m
[32m+[m[32m                    <br>[m
[32m+[m[32m                    Reorder Point:[m
[32m+[m[32m                    <b>{row["reorder_point"]:,.0f}</b>[m
[32m+[m[32m                    &nbsp;&nbsp;[m
[32m+[m[32m                    Safety Stock:[m
[32m+[m[32m                    <b>{row["safety_stock"]:,.0f}</b>[m
[32m+[m[32m                    &nbsp;&nbsp;[m
[32m+[m[32m                    Priority:[m
[32m+[m[32m                    <b>{row["inventory_priority"]}</b>[m
[32m+[m[32m                </div>[m
[32m+[m[32m                """,[m
[32m+[m[32m                unsafe_allow_html=True[m
[32m+[m[32m            )[m
[32m+[m
[32m+[m
[32m+[m[32m# ============================================================[m
[32m+[m[32m# FORECASTING TAB[m
[32m+[m[32m# ============================================================[m
[32m+[m
[32m+[m[32mwith tab2:[m
[32m+[m
[32m+[m[32m    st.markdown([m
[32m+[m[32m        '<div class="section">Demand Forecast Monitor</div>',[m
[32m+[m[32m        unsafe_allow_html=True[m
[32m+[m[32m    )[m
[32m+[m
[32m+[m[32m    forecast_filtered = forecast.copy()[m
[32m+[m
[32m+[m[32m    if selected_stores:[m
[32m+[m
[32m+[m[32m        forecast_filtered = forecast_filtered[[m
[32m+[m[32m            forecast_filtered["store_id"][m
[32m+[m[32m            .isin(selected_stores)[m
[32m+[m[32m        ][m
[32m+[m
[32m+[m[32m    if selected_item != "All Products":[m
[32m+[m
[32m+[m[32m        forecast_filtered = forecast_filtered[[m
[32m+[m[32m            forecast_filtered["item_id"][m
[32m+[m[32m            == selected_item[m
[32m+[m[32m        ][m
[32m+[m
[32m+[m[32m    daily = ([m
[32m+[m[32m        forecast_filtered[m
[32m+[m[32m        .groupby("date")[[m
[32m+[m[32m            ["sales", "prediction"][m
[32m+[m[32m        ][m
[32m+[m[32m        .sum()[m
[32m+[m[32m        .rename([m
[32m+[m[32m            columns={[m
[32m+[m[32m                "sales": "Actual Demand",[m
[32m+[m[32m                "prediction": "LightGBM Forecast"[m
[32m+[m[32m            }[m
[32m+[m[32m        )[m
[32m+[m[32m    )[m
[32m+[m
[32m+[m[32m    st.markdown("#### Actual vs Forecast Demand")[m
[32m+[m
[32m+[m[32m    st.line_chart([m
[32m+[m[32m        daily,[m
[32m+[m[32m        height=400[m
[32m+[m[32m    )[m
[32m+[m
[32m+[m[32m    st.markdown([m
[32m+[m[32m        '<div class="section">Model Performance</div>',[m
[32m+[m[32m        unsafe_allow_html=True[m
[32m+[m[32m    )[m
[32m+[m
[32m+[m[32m    c1, c2 = st.columns([1.4, 1])[m
[32m+[m
[32m+[m[32m    with c1:[m
[32m+[m
[32m+[m[32m        performance = comparison.set_index([m
[32m+[m[32m            "model"[m
[32m+[m[32m        )[["MAE", "RMSE"]][m
[32m+[m
[32m+[m[32m        st.bar_chart([m
[32m+[m[32m            performance,[m
[32m+[m[32m            height=330[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m    with c2:[m
[32m+[m
[32m+[m[32m        st.dataframe([m
[32m+[m[32m            comparison,[m
[32m+[m[32m            use_container_width=True,[m
[32m+[m[32m            hide_index=True[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m        st.markdown([m
[32m+[m[32m            """[m
[32m+[m[32m            <div class="info">[m
[32m+[m[32m            Lower MAE and RMSE indicate lower forecast[m
[32m+[m[32m            error on the evaluated test split.[m
[32m+[m[32m            </div>[m
[32m+[m[32m            """,[m
[32m+[m[32m            unsafe_allow_html=True[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m
[32m+[m[32m# ============================================================[m
[32m+[m[32m# INVENTORY TAB[m
[32m+[m[32m# ============================================================[m
[32m+[m
[32m+[m[32mwith tab3:[m
[32m+[m
[32m+[m[32m    st.markdown([m
[32m+[m[32m        '<div class="section">Inventory Optimization</div>',[m
[32m+[m[32m        unsafe_allow_html=True[m
[32m+[m[32m    )[m
[32m+[m
[32m+[m[32m    inventory_cols = [[m
[32m+[m[32m        "item_id",[m
[32m+[m[32m        "store_id",[m
[32m+[m[32m        "average_demand",[m
[32m+[m[32m        "forecast_demand",[m
[32m+[m[32m        "safety_stock",[m
[32m+[m[32m        "lead_time_demand",[m
[32m+[m[32m        "reorder_point",[m
[32m+[m[32m        "recommended_inventory",[m
[32m+[m[32m        "inventory_priority"[m
[32m+[m[32m    ][m
[32m+[m
[32m+[m[32m    table = ([m
[32m+[m[32m        filtered[m
[32m+[m[32m        .sort_values([m
[32m+[m[32m            "reorder_point",[m
[32m+[m[32m            ascending=False[m
[32m+[m[32m        )[m
[32m+[m[32m        [inventory_cols][m
[32m+[m[32m    )[m
[32m+[m
[32m+[m[32m    st.dataframe([m
[32m+[m[32m        table,[m
[32m+[m[32m        use_container_width=True,[m
[32m+[m[32m        hide_index=True,[m
[32m+[m[32m        height=500[m
[32m+[m[32m    )[m
[32m+[m
[32m+[m[32m    st.markdown([m
[32m+[m[32m        '<div class="section">Inventory Metrics</div>',[m
[32m+[m[32m        unsafe_allow_html=True[m
[32m+[m[32m    )[m
[32m+[m
[32m+[m[32m    a, b, c = st.columns(3)[m
[32m+[m
[32m+[m[32m    with a:[m
[32m+[m
[32m+[m[32m        st.metric([m
[32m+[m[32m            "Recommended Inventory",[m
[32m+[m[32m            f"{recommended_stock:,.0f}"[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m    with b:[m
[32m+[m
[32m+[m[32m        st.metric([m
[32m+[m[32m            "Forecast Demand",[m
[32m+[m[32m            f"{forecast_demand:,.0f}"[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m    with c:[m
[32m+[m
[32m+[m[32m        st.metric([m
[32m+[m[32m            "Safety Stock",[m
[32m+[m[32m            f"{safety_stock:,.0f}"[m
[32m+[m[32m        )[m
 [m
[31m-with col1:[m
[31m-    st.metric("Forecast Demand", "12,450")[m
 [m
[31m-with col2:[m
[31m-    st.metric("Items", "100")[m
[32m+[m[32m# ============================================================[m
[32m+[m[32m# FOOTER[m
[32m+[m[32m# ============================================================[m
 [m
[31m-with col3:[m
[31m-    st.metric("Stores", "10")[m
\ No newline at end of file[m
[32m+[m[32mst.markdown([m
[32m+[m[32m    """[m
[32m+[m[32m    <div class="footer">[m
[32m+[m[32m        RetailPulse[m
[32m+[m[32m        • Retail Demand Forecasting & Inventory Optimization[m
[32m+[m[32m        <br>[m
[32m+[m[32m        Python • DuckDB • Prophet • LightGBM • Streamlit[m
[32m+[m[32m    </div>[m
[32m+[m[32m    """,[m
[32m+[m[32m    unsafe_allow_html=True[m
[32m+[m[32m)[m
\ No newline at end of file[m
