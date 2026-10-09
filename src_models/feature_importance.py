import lightgbm as lgb
import os
import pandas as pd

def extract_feature_importance(model_path="src_models/registry/forecasting_baseline_v1.txt"):
    """
    Week 4: Day 5 - Machine Learning Feature Importance Pipeline.
    Loads our compiled model binary artifact, extracts feature weights,
    and calculates structural importance arrays for time-series analysis.
    """
    print("🤖 Booting Production Feature Importance Matrix Suite...")
    
    if not os.path.exists(model_path):
        print(f"❌ Blocker: Trained model binary not found at {model_path}. Run training first.")
        return

    try:
        # 1. Load the compiled booster straight from the registry folder
        model = lgb.Booster(model_file=model_path)
        
        # 2. Extract structural engineering weights
        importance_scores = model.feature_importance(importance_type='split')
        feature_names = [
            'walmart_year_week', 'weekday_number', 'calendar_month', 'calendar_year',
            'sales_lag_1d', 'sales_lag_7d', 'sales_lag_28d', 
            'sales_rolling_avg_7d', 'sales_rolling_avg_30d', 'item_sell_price'
        ]
        
        # 3. Create a clean ranking map layout dataframe
        df_importance = pd.DataFrame({
            'Feature': feature_names,
            'Importance_Score_Split': importance_scores
        }).sort_values(by='Importance_Score_Split', ascending=False)
        
        print("\n📊 Final Operational Feature Importance Ranking Arrays:")
        print("=============================================================")
        print(df_importance.to_string(index=False))
        print("=============================================================")
        print("\n🏁 Feature extraction complete! Matrix values successfully logged.")
        
    except Exception as e:
        print(f"🚨 Features analytics engine failure: {e}")

if __name__ == "__main__":
    extract_feature_importance()