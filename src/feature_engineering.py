import duckdb

DB_PATH = "data/retail.duckdb"
OUTPUT_PATH = "data/model_features.parquet"


def main():
    print("Connecting to DuckDB...")

    con = duckdb.connect(DB_PATH)

    print("Creating feature dataset...")

    query = """
        WITH daily_sales AS (
            SELECT
                s.item_id,
                s.store_id,
                s.state_id,
                c.date,
                c.wday,
                c.month,
                c.year,
                CASE
                    WHEN s.state_id = 'CA' THEN c.snap_CA
                    WHEN s.state_id = 'TX' THEN c.snap_TX
                    WHEN s.state_id = 'WI' THEN c.snap_WI
                    ELSE 0
                END AS snap,
                SUM(s.sales) AS sales
            FROM sales s
            JOIN calendar c
                ON s.d = c.d
            GROUP BY
                s.item_id,
                s.store_id,
                s.state_id,
                c.date,
                c.wday,
                c.month,
                c.year,
                snap
        ),

        featured AS (
            SELECT
                *,
                LAG(sales, 7) OVER (
                    PARTITION BY item_id, store_id
                    ORDER BY date
                ) AS lag_7,

                LAG(sales, 28) OVER (
                    PARTITION BY item_id, store_id
                    ORDER BY date
                ) AS lag_28,

                AVG(sales) OVER (
                    PARTITION BY item_id, store_id
                    ORDER BY date
                    ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING
                ) AS rolling_mean_7,

                AVG(sales) OVER (
                    PARTITION BY item_id, store_id
                    ORDER BY date
                    ROWS BETWEEN 28 PRECEDING AND 1 PRECEDING
                ) AS rolling_mean_28

            FROM daily_sales
        )

        SELECT *
        FROM featured
        WHERE lag_28 IS NOT NULL
        ORDER BY item_id, store_id, date
    """

    con.execute(f"""
        COPY ({query})
        TO '{OUTPUT_PATH}'
        (FORMAT PARQUET, COMPRESSION ZSTD)
    """)

    count = con.execute(f"""
        SELECT COUNT(*)
        FROM read_parquet('{OUTPUT_PATH}')
    """).fetchone()[0]

    print(f"\nFeature rows created: {count:,}")
    print(f"Saved to: {OUTPUT_PATH}")

    sample = con.execute(f"""
        SELECT *
        FROM read_parquet('{OUTPUT_PATH}')
        LIMIT 10
    """).fetchdf()

    print("\nFeature sample:")
    print(sample)

    con.close()

    print("\nFeature engineering completed successfully.")


if __name__ == "__main__":
    main()