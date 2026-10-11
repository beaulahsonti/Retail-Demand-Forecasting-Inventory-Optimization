import os
import pandas as pd


REQUIRED_FILES = [
    "models/baseline_predictions.csv",
    "models/prophet_predictions.csv",
    "models/lightgbm_predictions.csv",
    "models/model_comparison.csv",
    "models/inventory_recommendations.csv",
    "models/inventory_analysis.csv",
    "data/model_features.parquet",
    "data/model_training.parquet",
]


def check_file(path):
    exists = os.path.exists(path)

    status = "OK" if exists else "MISSING"

    print(f"[{status}] {path}")

    return exists


def main():

    print("=" * 60)
    print("RETAIL DEMAND FORECASTING PROJECT VALIDATION")
    print("=" * 60)

    print("\nChecking required project files...\n")

    results = [
        check_file(path)
        for path in REQUIRED_FILES
    ]

    print("\nChecking model comparison...")

    comparison = pd.read_csv(
        "models/model_comparison.csv"
    )

    print(
        f"Models evaluated: "
        f"{len(comparison)}"
    )

    print(comparison.to_string(index=False))

    print("\nChecking inventory recommendations...")

    inventory = pd.read_csv(
        "models/inventory_recommendations.csv"
    )

    print(
        f"Inventory series: "
        f"{len(inventory)}"
    )

    print("\nChecking Streamlit dashboard...")

    dashboard_exists = os.path.exists("app.py")

    print(
        "[OK] app.py"
        if dashboard_exists
        else "[MISSING] app.py"
    )

    print("\nChecking project documentation...")

    readme_exists = os.path.exists("README.md")

    print(
        "[OK] README.md"
        if readme_exists
        else "[MISSING] README.md"
    )

    print("\n" + "=" * 60)

    if all(results) and dashboard_exists and readme_exists:
        print("PROJECT VALIDATION PASSED")
    else:
        print("PROJECT VALIDATION REQUIRES ATTENTION")

    print("=" * 60)


if __name__ == "__main__":
    main()