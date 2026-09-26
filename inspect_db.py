import sqlite3
import pandas as pd
import os

def inspect_staging_tables():
    print("🔍 Opening local staging warehouse database file...")
    db_path = os.path.join("src_etl", "retail_warehouse.db")
    
    if not os.path.exists(db_path):
        print(f"❌ Error: Database file not found at path target: {db_path}")
        return
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Fetch the names of all structural tables created inside the database file container
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"📦 Total Tables Discovered: {len(tables)}")
    for index, table in enumerate(tables, 1):
        table_name = table[0]
        print(f"\n--- [{index}] Table Name Target: `{table_name}` ---")
        
        # Inspect the exact column names and data types
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        print("📁 Schema Columns Grid:")
        for col in columns:
            print(f"  • Column ID: {col[0]} | Name: {col[1]} | Type: {col[2]}")
            
        # Pull sample data rows to check for data frame structural parameters
        print("📊 Previewing Staged Target Rows Data Matrix:")
        try:
            df_preview = pd.read_sql(f"SELECT * FROM {table_name} LIMIT 3;", conn)
            print(df_preview.to_string(index=False))
        except Exception as e:
            print(f"⚠️ Row review warning: {e}")
            
    conn.close()
    print("\n🏁 Staging database inspection check complete!")

if __name__ == "__main__":
    inspect_staging_tables()
