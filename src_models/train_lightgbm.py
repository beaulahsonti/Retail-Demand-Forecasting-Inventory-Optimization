from google.cloud import bigquery
import pandas as pd
import numpy as np
import lightgbm as lgb
import yaml
import os

def run_baseline_training(model_dir="src_models/registry", config_path="src_models/hyperparams.yml"):
    """
    Week 5: BigQuery Integrated Machine Learning Training Pipeline.
    Streams pre-calculated feature engineering matrices directly from Google Cloud
    to train our high-performance LightGBM gradient boosting model.
    """
    print("🤖 Booting Decoupled Production LightGBM Pipeline...")
    os.makedirs(model_dir, exist_ok=True)
    
    # 💡 Load hyperparameters dynamically from our centralized config file
    print(f"📖 Loading parameters from {config_path}...")
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    lgb_params = config['baseline_tuning_parameters']
    
    # 🔌 Connect natively to Google Cloud BigQuery
    print("🔌 Authenticating and connecting to Google Cloud BigQuery...")
    try:
        # Client automatically reads environment GCP credentials tokens
        client = bigquery.Client()
        
        # Define the cloud data warehouse extraction query target
        print("📥 Streaming optimized ML training matrices from BigQuery cloud tables...")
        query = """
            SELECT * 
            FROM `your-gcp-project-id.main.fct_ml_training_matrix` 
            LIMIT 100000;
        """
        
        # Pull records directly down from BigQuery into active memory
        df = client.query(query).to_dataframe()
        print(f"✓ Cloud data mart extracted successfully. Shape: {df.shape}")

        # Chronological Validation Split
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
        print(f"🚨 Cloud Pipeline failure: {e}")

if __name__ == "__main__":
    run_baseline_training()
