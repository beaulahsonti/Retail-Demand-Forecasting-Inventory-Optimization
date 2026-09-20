from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Retail Demand Forecasting & Inventory Optimization",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
        .main {
            padding-top: 1rem;
        }

        .dashboard-title {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }

        .dashboard-subtitle {
            font-size: 1rem;
            color: #666;
            margin-bottom: 1.5rem;
        }

        div[data-testid="stMetric"] {
            border: 1px solid #e5e7eb;
            padding: 15px;
            border-radius: 10px;
            background-color: #ffffff;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

@st.cache_data
def load_csv(filename):
    """Load a report CSV from the reports folder."""
    file_path = REPORTS_DIR / filename

    if not file_path.exists():
        return pd.DataFrame()

    return pd.read_csv(file_path)


def show_missing_file_message(filename):
    """Display a warning when a report is unavailable."""
    st.warning(
        f"Report file not found: reports/{filename}"
    )


# ============================================================
# LOAD REPORTS
# ============================================================

model_comparison = load_csv("model_comparison.csv")

baseline_metrics = load_csv("baseline_metrics.csv")
prophet_metrics = load_csv("prophet_metrics.csv")
lightgbm_metrics = load_csv("lightgbm_metrics.csv")

feature_importance = load_csv("lightgbm_feature_importance.csv")

inventory = load_csv("inventory_optimization.csv")
safety_stock = load_csv("safety_stock.csv")
reorder_point = load_csv("reorder_point.csv")

eda_summary = load_csv("eda_summary.csv")
product_store_summary = load_csv("product_store_demand_summary.csv")


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="dashboard-title">📊 Retail Demand Forecasting & Inventory Optimization</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'End-to-end analytics platform for demand forecasting, model evaluation, '
    'and inventory optimization.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("Dashboard Navigation")

page = st.sidebar.radio(
    "Select Section",
    [
        "Overview",
        "Model Performance",
        "Forecast Analysis",
        "Inventory Optimization",
        "Feature Importance",
        "Data Summary"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    "Data source: project reports generated from the forecasting "
    "and inventory optimization pipeline."
)


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    st.header("Project Overview")

    # --------------------------------------------------------
    # Calculate overview metrics
    # --------------------------------------------------------

    if not inventory.empty:

        total_products = inventory["item_id"].nunique()
        total_stores = inventory["store_id"].nunique()
        total_combinations = len(inventory)

        if "forecast_demand" in inventory.columns:
            total_forecast = inventory["forecast_demand"].sum()
        else:
            total_forecast = 0

        if "target_inventory" in inventory.columns:
            total_target_inventory = inventory["target_inventory"].sum()
        else:
            total_target_inventory = 0

    else:

        total_products = 0
        total_stores = 0
        total_combinations = 0
        total_forecast = 0
        total_target_inventory = 0

    # --------------------------------------------------------
    # KPI cards
    # --------------------------------------------------------

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Products",
            f"{total_products:,}"
        )

    with col2:
        st.metric(
            "Stores",
            f"{total_stores:,}"
        )

    with col3:
        st.metric(
            "Product-Store Pairs",
            f"{total_combinations:,}"
        )

    with col4:
        st.metric(
            "Forecast Demand",
            f"{total_forecast:,.2f}"
        )

    with col5:
        st.metric(
            "Target Inventory",
            f"{total_target_inventory:,.2f}"
        )

    st.markdown("---")

    # --------------------------------------------------------
    # Model summary
    # --------------------------------------------------------

    st.subheader("Forecasting Model Summary")

    if not model_comparison.empty:

        display_columns = [
            column
            for column in [
                "model",
                "validation_rows",
                "MAE",
                "RMSE",
                "WAPE",
                "sMAPE"
            ]
            if column in model_comparison.columns
        ]

        st.dataframe(
            model_comparison[display_columns],
            use_container_width=True,
            hide_index=True
        )

        if "MAE" in model_comparison.columns:

            fig = px.bar(
                model_comparison,
                x="model",
                y="MAE",
                title="Model MAE Comparison",
                text_auto=".4f"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    else:
        show_missing_file_message("model_comparison.csv")


# ============================================================
# MODEL PERFORMANCE
# ============================================================

elif page == "Model Performance":

    st.header("Forecasting Model Performance")

    if model_comparison.empty:

        show_missing_file_message("model_comparison.csv")

    else:

        # ----------------------------------------------------
        # Metrics table
        # ----------------------------------------------------

        st.subheader("Model Evaluation Metrics")

        st.dataframe(
            model_comparison,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")

        # ----------------------------------------------------
        # MAE / RMSE
        # ----------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            if "MAE" in model_comparison.columns:

                fig_mae = px.bar(
                    model_comparison,
                    x="model",
                    y="MAE",
                    title="Mean Absolute Error (MAE)",
                    text_auto=".4f"
                )

                st.plotly_chart(
                    fig_mae,
                    use_container_width=True
                )

        with col2:

            if "RMSE" in model_comparison.columns:

                fig_rmse = px.bar(
                    model_comparison,
                    x="model",
                    y="RMSE",
                    title="Root Mean Squared Error (RMSE)",
                    text_auto=".4f"
                )

                st.plotly_chart(
                    fig_rmse,
                    use_container_width=True
                )

        # ----------------------------------------------------
        # WAPE / sMAPE
        # ----------------------------------------------------

        col3, col4 = st.columns(2)

        with col3:

            if "WAPE" in model_comparison.columns:

                fig_wape = px.bar(
                    model_comparison,
                    x="model",
                    y="WAPE",
                    title="Weighted Absolute Percentage Error (WAPE)",
                    text_auto=".2f"
                )

                st.plotly_chart(
                    fig_wape,
                    use_container_width=True
                )

        with col4:

            if "sMAPE" in model_comparison.columns:

                fig_smape = px.bar(
                    model_comparison,
                    x="model",
                    y="sMAPE",
                    title="Symmetric Mean Absolute Percentage Error",
                    text_auto=".2f"
                )

                st.plotly_chart(
                    fig_smape,
                    use_container_width=True
                )

        # ----------------------------------------------------
        # Individual metric files
        # ----------------------------------------------------

        st.markdown("---")

        st.subheader("Individual Model Reports")

        tab1, tab2, tab3 = st.tabs(
            [
                "Baseline",
                "Prophet",
                "LightGBM"
            ]
        )

        with tab1:

            if not baseline_metrics.empty:
                st.dataframe(
                    baseline_metrics,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                show_missing_file_message(
                    "baseline_metrics.csv"
                )

        with tab2:

            if not prophet_metrics.empty:
                st.dataframe(
                    prophet_metrics,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                show_missing_file_message(
                    "prophet_metrics.csv"
                )

        with tab3:

            if not lightgbm_metrics.empty:
                st.dataframe(
                    lightgbm_metrics,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                show_missing_file_message(
                    "lightgbm_metrics.csv"
                )


# ============================================================
# FORECAST ANALYSIS
# ============================================================

elif page == "Forecast Analysis":

    st.header("Demand Forecast Analysis")

    if inventory.empty:

        show_missing_file_message(
            "inventory_optimization.csv"
        )

    else:

        # ----------------------------------------------------
        # Product selector
        # ----------------------------------------------------

        products = sorted(
            inventory["item_id"].dropna().unique()
        )

        selected_product = st.selectbox(
            "Select Product",
            products
        )

        product_data = inventory[
            inventory["item_id"] == selected_product
        ].copy()

        # ----------------------------------------------------
        # Product KPIs
        # ----------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            forecast_value = product_data[
                "forecast_demand"
            ].sum()

            st.metric(
                "Forecast Demand",
                f"{forecast_value:,.2f}"
            )

        with col2:

            if "average_daily_demand" in product_data.columns:

                avg_demand = product_data[
                    "average_daily_demand"
                ].mean()

                st.metric(
                    "Average Daily Demand",
                    f"{avg_demand:.2f}"
                )

        with col3:

            if "safety_stock" in product_data.columns:

                avg_safety = product_data[
                    "safety_stock"
                ].mean()

                st.metric(
                    "Average Safety Stock",
                    f"{avg_safety:.2f}"
                )

        with col4:

            if "reorder_point" in product_data.columns:

                avg_reorder = product_data[
                    "reorder_point"
                ].mean()

                st.metric(
                    "Average Reorder Point",
                    f"{avg_reorder:.2f}"
                )

        st.markdown("---")

        # ----------------------------------------------------
        # Product-store forecast chart
        # ----------------------------------------------------

        if "store_id" in product_data.columns:

            fig = px.bar(
                product_data,
                x="store_id",
                y="forecast_demand",
                title=f"Forecast Demand by Store — {selected_product}",
                text_auto=".2f"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ----------------------------------------------------
        # Product table
        # ----------------------------------------------------

        st.subheader(
            f"Forecast Details — {selected_product}"
        )

        columns = [
            "item_id",
            "store_id",
            "forecast_demand",
            "forecast_daily_average",
            "forecast_horizon_days",
            "safety_stock",
            "reorder_point",
            "target_inventory",
            "recommended_action"
        ]

        available_columns = [
            column
            for column in columns
            if column in product_data.columns
        ]

        st.dataframe(
            product_data[available_columns],
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# INVENTORY OPTIMIZATION
# ============================================================

elif page == "Inventory Optimization":

    st.header("Inventory Optimization")

    if inventory.empty:

        show_missing_file_message(
            "inventory_optimization.csv"
        )

    else:

        # ----------------------------------------------------
        # KPI calculations
        # ----------------------------------------------------

        avg_safety_stock = (
            inventory["safety_stock"].mean()
            if "safety_stock" in inventory.columns
            else 0
        )

        avg_reorder_point = (
            inventory["reorder_point"].mean()
            if "reorder_point" in inventory.columns
            else 0
        )

        avg_target_inventory = (
            inventory["target_inventory"].mean()
            if "target_inventory" in inventory.columns
            else 0
        )

        # ----------------------------------------------------
        # KPI cards
        # ----------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Average Safety Stock",
                f"{avg_safety_stock:.2f}"
            )

        with col2:
            st.metric(
                "Average Reorder Point",
                f"{avg_reorder_point:.2f}"
            )

        with col3:
            st.metric(
                "Average Target Inventory",
                f"{avg_target_inventory:.2f}"
            )

        with col4:

            if "forecast_demand" in inventory.columns:

                total_forecast = inventory[
                    "forecast_demand"
                ].sum()

                st.metric(
                    "Total Forecast Demand",
                    f"{total_forecast:,.2f}"
                )

        st.markdown("---")

        # ----------------------------------------------------
        # Inventory level distribution
        # ----------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            if "inventory_level" in inventory.columns:

                level_counts = (
                    inventory["inventory_level"]
                    .value_counts()
                    .reset_index()
                )

                level_counts.columns = [
                    "inventory_level",
                    "count"
                ]

                fig = px.pie(
                    level_counts,
                    names="inventory_level",
                    values="count",
                    title="Inventory Level Distribution",
                    hole=0.4
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        with col2:

            if "recommended_action" in inventory.columns:

                action_counts = (
                    inventory["recommended_action"]
                    .value_counts()
                    .reset_index()
                )

                action_counts.columns = [
                    "recommended_action",
                    "count"
                ]

                fig = px.bar(
                    action_counts,
                    x="recommended_action",
                    y="count",
                    title="Recommended Inventory Actions",
                    text_auto=True
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        # ----------------------------------------------------
        # Safety stock
        # ----------------------------------------------------

        st.markdown("---")

        st.subheader("Safety Stock Analysis")

        if not safety_stock.empty:

            st.dataframe(
                safety_stock,
                use_container_width=True,
                hide_index=True
            )

        # ----------------------------------------------------
        # Reorder point
        # ----------------------------------------------------

        st.subheader("Reorder Point Analysis")

        if not reorder_point.empty:

            st.dataframe(
                reorder_point,
                use_container_width=True,
                hide_index=True
            )

        # ----------------------------------------------------
        # Inventory optimization table
        # ----------------------------------------------------

        st.subheader("Inventory Recommendations")

        display_columns = [
            "item_id",
            "store_id",
            "forecast_demand",
            "safety_stock",
            "reorder_point",
            "target_inventory",
            "inventory_level",
            "recommended_action"
        ]

        available_columns = [
            column
            for column in display_columns
            if column in inventory.columns
        ]

        st.dataframe(
            inventory[available_columns],
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# FEATURE IMPORTANCE
# ============================================================

elif page == "Feature Importance":

    st.header("LightGBM Feature Importance")

    if feature_importance.empty:

        show_missing_file_message(
            "lightgbm_feature_importance.csv"
        )

    else:

        st.subheader(
            "Features Used by the LightGBM Forecasting Model"
        )

        # Try to identify feature and importance columns
        feature_column = None
        importance_column = None

        for column in feature_importance.columns:

            column_lower = column.lower()

            if (
                feature_column is None
                and "feature" in column_lower
            ):
                feature_column = column

            if (
                importance_column is None
                and "importance" in column_lower
            ):
                importance_column = column

        if (
            feature_column is not None
            and importance_column is not None
        ):

            feature_plot_data = (
                feature_importance
                .sort_values(
                    importance_column,
                    ascending=False
                )
                .head(20)
            )

            fig = px.bar(
                feature_plot_data,
                x=importance_column,
                y=feature_column,
                orientation="h",
                title="Top 20 Feature Importance"
            )

            fig.update_layout(
                yaxis={
                    "categoryorder": "total ascending"
                }
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.subheader("Feature Importance Table")

        st.dataframe(
            feature_importance,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# DATA SUMMARY
# ============================================================

elif page == "Data Summary":

    st.header("Data & EDA Summary")

    # --------------------------------------------------------
    # EDA summary
    # --------------------------------------------------------

    if not eda_summary.empty:

        st.subheader("EDA Summary")

        st.dataframe(
            eda_summary,
            use_container_width=True,
            hide_index=True
        )

    else:

        show_missing_file_message(
            "eda_summary.csv"
        )

    st.markdown("---")

    # --------------------------------------------------------
    # Product-store summary
    # --------------------------------------------------------

    if not product_store_summary.empty:

        st.subheader(
            "Product-Store Demand Summary"
        )

        st.dataframe(
            product_store_summary,
            use_container_width=True,
            hide_index=True
        )

    else:

        show_missing_file_message(
            "product_store_demand_summary.csv"
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Retail Demand Forecasting & Inventory Optimization | "
    "Python • SQL • DuckDB • Prophet • LightGBM • Streamlit"
)