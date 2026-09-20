"""
Forecasting Model Comparison

Compares:
- Baseline
- Prophet
- LightGBM

Creates:
- Combined model comparison CSV
- Model comparison chart
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# ---------------------------------------------------------------
# PROJECT PATH
# ---------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"

BASELINE_FILE = REPORTS_DIR / "baseline_metrics.csv"
PROPHET_FILE = REPORTS_DIR / "prophet_metrics.csv"
LIGHTGBM_FILE = REPORTS_DIR / "lightgbm_metrics.csv"

COMPARISON_FILE = REPORTS_DIR / "model_comparison.csv"
CHART_FILE = FIGURES_DIR / "model_comparison.png"


# ---------------------------------------------------------------
# LOAD METRICS
# ---------------------------------------------------------------

def load_metrics(file_path, model_name):
    """Load a model metric file and standardize its model name."""

    df = pd.read_csv(file_path)

    # Standardize model name
    df["model"] = model_name

    # Baseline and Prophet metric files do not contain
    # validation_rows, so add the known validation size.
    if "validation_rows" not in df.columns:
        df["validation_rows"] = 3640

    return df


# ---------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------

def main():

    print("=" * 70)
    print("FORECASTING MODEL COMPARISON")
    print("=" * 70)

    # -----------------------------------------------------------
    # LOAD MODEL METRICS
    # -----------------------------------------------------------

    print("\nLoading model metrics...")

    baseline = load_metrics(
        BASELINE_FILE,
        "Baseline"
    )

    prophet = load_metrics(
        PROPHET_FILE,
        "Prophet"
    )

    lightgbm = load_metrics(
        LIGHTGBM_FILE,
        "LightGBM"
    )

    # -----------------------------------------------------------
    # COMBINE RESULTS
    # -----------------------------------------------------------

    comparison = pd.concat(
        [
            baseline,
            prophet,
            lightgbm
        ],
        ignore_index=True
    )

    # -----------------------------------------------------------
    # KEEP REQUIRED COLUMNS
    # -----------------------------------------------------------

    required_columns = [
        "model",
        "validation_rows",
        "MAE",
        "RMSE",
        "WAPE",
        "sMAPE"
    ]

    available_columns = [
        column
        for column in required_columns
        if column in comparison.columns
    ]

    comparison = comparison[available_columns]

    # -----------------------------------------------------------
    # ENSURE VALIDATION ROWS ARE INTEGER
    # -----------------------------------------------------------

    comparison["validation_rows"] = (
        comparison["validation_rows"]
        .fillna(3640)
        .astype(int)
    )

    # -----------------------------------------------------------
    # ROUND METRICS
    # -----------------------------------------------------------

    comparison["MAE"] = comparison["MAE"].round(4)
    comparison["RMSE"] = comparison["RMSE"].round(4)
    comparison["WAPE"] = comparison["WAPE"].round(2)
    comparison["sMAPE"] = comparison["sMAPE"].round(2)

    # -----------------------------------------------------------
    # SORT BY MAE
    # -----------------------------------------------------------

    comparison = comparison.sort_values(
        "MAE",
        ascending=True
    ).reset_index(drop=True)

    # -----------------------------------------------------------
    # SAVE COMPARISON CSV
    # -----------------------------------------------------------

    REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    FIGURES_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    comparison.to_csv(
        COMPARISON_FILE,
        index=False
    )

    # -----------------------------------------------------------
    # DISPLAY RESULTS
    # -----------------------------------------------------------

    print("\nMODEL COMPARISON")
    print("-" * 70)

    print(
        comparison.to_string(
            index=False
        )
    )

    # -----------------------------------------------------------
    # CREATE COMPARISON CHART
    # -----------------------------------------------------------

    metrics = [
        "MAE",
        "RMSE",
        "WAPE",
        "sMAPE"
    ]

    chart_data = comparison.set_index("model")[metrics]

    ax = chart_data.plot(
        kind="bar",
        figsize=(12, 7)
    )

    ax.set_title(
        "Retail Demand Forecasting Model Comparison"
    )

    ax.set_xlabel(
        "Model"
    )

    ax.set_ylabel(
        "Metric Value"
    )

    ax.legend(
        title="Metrics"
    )

    plt.xticks(
        rotation=0
    )

    plt.tight_layout()

    plt.savefig(
        CHART_FILE,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    # -----------------------------------------------------------
    # FINAL OUTPUT
    # -----------------------------------------------------------

    print("\nSaved files:")
    print(COMPARISON_FILE)
    print(CHART_FILE)

    print("\nModel comparison completed successfully.")


# ---------------------------------------------------------------
# RUN PROGRAM
# ---------------------------------------------------------------

if __name__ == "__main__":
    main()