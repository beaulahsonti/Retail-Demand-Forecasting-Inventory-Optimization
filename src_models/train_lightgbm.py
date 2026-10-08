import duckdb
import pandas as pd
import numpy as np
import lightgbm as lgb
import yaml
import os

def run_baseline_training(db_path="src_dbt/zaalima_warehouse.duckdb", model_dir="src_models/registry", config_path="src_models/hyperparams.yml"):
    print("🤖 Booting Decoupled Production LightGBM Pipeline...")
    os.makedirs(model_dir, exist_ok=True)
    
    # 💡 Load hyperparameters dynamically from the centralized config file
    print(f"📖 Loading parameters from {config_path}...")
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    lgb_params = config['baseline_tuning_parameters']
    
    if not os.path.exists(db_path):
        print(f"❌ Blocker: Database not found at {db_path}.")
        return

    print("🔌 Extracting optimized ML training matrices from DuckDB features...")
    conn = duckdb.connect(db_path)
    
    try:
        query = "SELECT * FROM main.fct_ml_training_matrix LIMIT 100000;"
        df = conn.execute(query).fetchdf()
        print(f"✓ Data mart extracted successfully. Shape: {df.shape}")

        split_idx = int(len(df) * 0.85)
        train_df = df.iloc[:split_idx]
        val_df = df.iloc[split_idx:]

        features = [
            'walmart_year_week', 'weekday_number', 'calendar_month', 'calendar_year',
            'sales_lag_1d', 'sales_lag_7d', 'sales_lag_28d', 
            'sales_rolling_avg_7d', 'sales_rolling_avg_30d', 'item_sell_price'
        ]
        target = 'log_daily_sales_units'

        X_train, y_train = train_df[features], train_df[target]
        X_val, y_val = val_df[features], val_df[target]

        train_data = lgb.Dataset(X_train, label=y_train)
        val_data = lgb.Dataset(X_val, label=y_val, reference=train_data)

        print("🚀 Executing model training with decoupled parameters...")
        model = lgb.train(
            lgb_params,
            train_data,
            num_boost_round=50,
            valid_sets=[train_data, val_data],
            callbacks=[lgb.log_evaluation(period=10)]
        )
        print("✓ Training loops successfully completed.")

        model_output_path = os.path.join(model_dir, "forecasting_baseline_v1.txt")
        model.save_model(model_output_path)
        print(f"📦 Model registry artifact saved to: {model_output_path}")

    except Exception as e:
        print(f"🚨 Pipeline failure: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    run_baseline_training()