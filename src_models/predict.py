import lightgbm as lgb
import os
import numpy as np
import pandas as pd

def run_model_inference(model_path="src_models/registry/forecasting_baseline_v1.txt"):
    """
    Week 4: Day 7 - Machine Learning Automated Inference & Prediction Sandbox.
    Loads our compiled baseline model artifact, simulates an incoming production 
    feature vector window, and executes retail demand forecasting validation tests.
    """
    print("🤖 Booting Production Model Inference & Prediction Sandbox Suite...")
    
    if not os.path.exists(model_path):
        print(f"❌ Blocker: Trained model binary artifact not found at {model_path}. Run training loop first.")
        return

    try:
        # 1. Load the compiled mathematical booster binary directly from the registry
        model = lgb.Booster(model_file=model_path)
        print(f"✓ Model registry artifact safely loaded. Total features mapping tree: {model.num_feature()}")
        
        # 2. Simulate an incoming real-time operational feature array matrix window
        print("⚙️ Mapping production-grade feature vectors for future demand scoring...")
        simulated_features = pd.DataFrame([{
            'walmart_year_week': 11601,
            'weekday_number': 1,
            'calendar_month': 1,
            'calendar_year': 2016,
            'sales_lag_1d': 4,
            'sales_lag_7d': 3,
            'sales_lag_28d': 2,
            'sales_rolling_avg_7d': 3.5,
            'sales_rolling_avg_30d': 3.2,
            'item_sell_price': 8.25
        }])
        
        # 3. Execute the forecasting score prediction inference loop
        print("🚀 Executing time-series demand forecasting inference loops...")
        predicted_log_demand = model.predict(simulated_features)
        
        # 4. Invert the logarithmic target transformation matrix scale cleanly back to raw scalar count units: exp(x) - 1
        predicted_raw_units = np.expm1(predicted_log_demand[0])
        
        print("\n🔮 Live Target Demand Inference Snapshot Results:")
        print("=============================================================")
        print(f"Predicted Logarithmic Target Demand Index: {predicted_log_demand[0]:.4f}")
        print(f"Calculated Forecast Raw Retail Sales Units: {max(0, int(round(predicted_raw_units)))} units")
        print("=============================================================")
        print("\n🏁 Inference execution complete! Forecasting matrix scores successfully output.")
        
    except Exception as e:
        print(f"🚨 Inference sandbox failure: {e}")

if __name__ == "__main__":
    run_model_inference()