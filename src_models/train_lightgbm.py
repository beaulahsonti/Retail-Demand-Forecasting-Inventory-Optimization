import duckdb
import pandas as pd
import numpy as np
import lightgbm as lgb
import os

def run_baseline_training(db_path="src_dbt/zaalima_warehouse.duckdb", model_dir="src_models/registry"):
    """
    Week 4: Day 2 - Memory-Optimized Baseline LightGBM Model Training.
    Extracts a high-value validation chunk from the data mart to prevent 
    RAM allocation failures, splits chronologically, and exports the model binary.
    """
    print("🤖 Booting Memory-Optimized Production Baseline LightGBM Pipeline...")
    
    # Ensure local directory structures are ready
    os.makedirs(model_dir, exist_ok=True)
    
    if not os.path.exists(db_path):
        print(f"❌ Blocker: Database not found at {db_path}. Run dbt models first.")
        return

    # 1. Connect natively to the DuckDB data mart layer
    print("🔌 Extracting optimized ML training matrices from DuckDB features...")
    conn = duckdb.connect(db_path)
    
    try:
        query = "SELECT * FROM main.fct_ml_training_matrix LIMIT 100000;"
        df = conn.execute(query).fetchdf()
        print(f"✓ Data mart extracted successfully. Optimized records shape: {df.shape}")

        # 2. Chronological Train/Test Split
        print("✂️ Splitting data structures into chronological sets...")
        split_idx = int(len(df) * 0.85)
        train_df = df.iloc[:split_idx]
        val_df = df.iloc[split_idx:]

        # Define explicit model input features and targets
        features = [
            'walmart_year_week', 'weekday_number', 'calendar_month', 'calendar_year',
            'sales_lag_1d', 'sales_lag_7d', 'sales_lag_28d', 
            'sales_rolling_avg_7d', 'sales_rolling_avg_30d', 'item_sell_price'
        ]
        target = 'log_daily_sales_units'

        X_train, y_train = train_df[features], train_df[target]
        X_val, y_val = val_df[features], val_df[target]

        # 3. Initialize LightGBM Dataset objects
        print("📦 Compiling high-performance LightGBM Dataset matrix layers...")
        train_data = lgb.Dataset(X_train, label=y_train)
        val_data = lgb.Dataset(X_val, label=y_val, reference=train_data)

        # Hyperparameter baseline definitions
        lgb_params = {
            'objective': 'regression',
            'metric': 'rmse',
            'boosting_type': 'gbdt',
            'learning_rate': 0.05,
            'num_leaves': 31,
            'max_depth': 6,
            'verbose': -1,
            'n_jobs': -1
        }

        # 4. Train the baseline loop model
        print("🚀 Executing baseline model training iteration runs...")
        model = lgb.train(
            lgb_params,
            train_data,
            num_boost_round=50,
            valid_sets=[train_data, val_data],
            callbacks=[lgb.log_evaluation(period=10)]
        )
        print("✓ Baseline training loops successfully completed.")

        # 5. Export compiled model binary file registry artifact
        model_output_path = os.path.join(model_dir, "forecasting_baseline_v1.txt")
        model.save_model(model_output_path)
        print(f"📦 Model registry artifact successfully saved to: {model_output_path}")
        print("\n🏁 Pipeline complete! Ready for Review validation showcases!")

    except Exception as e:
        print(f"🚨 Pipeline failure during model training: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    run_baseline_training()