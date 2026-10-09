import duckdb

DB_PATH = "data/retail.duckdb"
FEATURE_PATH = "data/model_features.parquet"
OUTPUT_PATH = "data/model_training.parquet"


def main():
    print("Connecting to DuckDB...")

    con = duckdb.connect(DB_PATH)

    print("Selecting top 100 item-store combinations...")

    con.execute(f"""
        CREATE OR REPLACE TABLE top_series AS
        SELECT
            item_id,
            store_id,
            SUM(sales) AS total_sales
        FROM read_parquet('{FEATURE_PATH}')
        GROUP BY item_id, store_id
        ORDER BY total_sales DESC
        LIMIT 100
    """)

    count = con.execute("""
        SELECT COUNT(*)
        FROM top_series
    """).fetchone()[0]

    print(f"Selected series: {count}")

    print("Creating model training dataset...")

    con.execute(f"""
        COPY (
            SELECT
                f.item_id,
                f.store_id,
                f.state_id,
                f.date,
                f.wday,
                f.month,
                f.year,
                f.snap,
                f.sales,
                f.lag_7,
                f.lag_28,
                f.rolling_mean_7,
                f.rolling_mean_28
            FROM read_parquet('{FEATURE_PATH}') f
            INNER JOIN top_series t
                ON f.item_id = t.item_id
                AND f.store_id = t.store_id
            ORDER BY f.item_id, f.store_id, f.date
        )
        TO '{OUTPUT_PATH}'
        (FORMAT PARQUET, COMPRESSION ZSTD)
    """)

    rows = con.execute(f"""
        SELECT COUNT(*)
        FROM read_parquet('{OUTPUT_PATH}')
    """).fetchone()[0]

    print(f"Training rows: {rows:,}")

    sample = con.execute(f"""
        SELECT *
        FROM read_parquet('{OUTPUT_PATH}')
        LIMIT 10
    """).fetchdf()

    print("\nTraining dataset sample:")
    print(sample)

    con.close()

    print(f"\nSaved model dataset to: {OUTPUT_PATH}")
    print("Model data preparation completed successfully.")


if __name__ == "__main__":
    main()