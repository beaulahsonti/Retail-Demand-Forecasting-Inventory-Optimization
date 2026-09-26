import pandas as pd
import sqlite3
import os

def run_production_etl(data_directory="data_raw", db_name="retail_warehouse.db"):
    """
    Week 1: Data Architecture & ETL Ingestion Pipeline.
    Streams all four authentic Kaggle M5 Forecasting files from local storage
    directly into your local database staging warehouse using chunk optimization
    and native database transactional protection blocks.
    """
    print("🚀 Initializing Master M5 Production Ingestion Pipeline...")
    
    # Establish connection to your warehouse staging database file
    db_path = os.path.join("src_etl", db_name)
    conn = sqlite3.connect(db_path)
    print(f"📦 Staging Data Mart Connected securely at: {db_path}\n")

    # The 4 complete core tables to load from your data folder
    m5_files = ['calendar.csv', 'sell_prices.csv', 'sales_train_validation.csv', 'sales_train_evaluation.csv']
    
    for file_name in m5_files:
        file_path = os.path.join(data_directory, file_name)
        table_name = file_name.replace(".csv", "")
        
        if not os.path.exists(file_path):
            print(f"❌ Error: Required file missing at '{file_path}'")
            conn.close()
            return
            
        print(f"📥 Processing true records from file: {file_name}")
        chunk_count = 0
        
        try:
            # Using Python's native transaction context manager block.
            # If any chunk fails, the database automatically rolls back completely.
            with conn:
                for chunk in pd.read_csv(file_path, chunksize=100000):
                    # Standardize column layouts to strict lowercase for seamless querying
                    chunk.columns = [col.lower() for col in chunk.columns]
                    
                    # The first chunk creates/replaces the table; subsequent chunks append data records
                    mode = 'replace' if chunk_count == 0 else 'append'
                    chunk.to_sql(table_name, conn, if_exists=mode, index=False)
                    chunk_count += 1
                    
                    if chunk_count % 5 == 0 or table_name == 'calendar':
                        print(f"  ⚡ Processed Batch {chunk_count}: Loaded cumulative rows matrix...")
                        
            print(f"✓ Table `{table_name}` successfully committed into database staging matrices.\n")
            
        except Exception as err:
            # Native context manager handles rollback actions automatically under the hood
            print(f"🚨 Critical Failure while processing `{file_name}`. Changes rolled back safely.")
            print(f"Traceback error details: {err}")
            conn.close()
            return

    conn.close()
    print("🏁 Full Production Ingestion Complete! Your Kaggle data tables are staging live.")

if __name__ == "__main__":
    run_production_etl()
