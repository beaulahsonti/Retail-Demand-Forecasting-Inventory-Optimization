import duckdb

DB_PATH = "data/retail.duckdb"

SALES_PATH = "data/raw/sales_long.csv"
CALENDAR_PATH = "data/raw/calendar_processed.csv"
PRICES_PATH = "data/raw/prices_processed.csv"


def main():
    print("Creating DuckDB database...")

    con = duckdb.connect(DB_PATH)

    print("Creating data views...")

    con.execute(f"""
        CREATE OR REPLACE VIEW sales AS
        SELECT *
        FROM read_csv_auto('{SALES_PATH}')
    """)

    con.execute(f"""
        CREATE OR REPLACE VIEW calendar AS
        SELECT *
        FROM read_csv_auto('{CALENDAR_PATH}')
    """)

    con.execute(f"""
        CREATE OR REPLACE VIEW prices AS
        SELECT *
        FROM read_csv_auto('{PRICES_PATH}')
    """)

    print("Views created successfully.")

    # Test integrated dataset
    print("\nTesting sales + calendar + price integration...")

    result = con.execute("""
        SELECT
            s.id,
            s.item_id,
            s.dept_id,
            s.cat_id,
            s.store_id,
            s.state_id,
            c.date,
            s.sales,
            p.sell_price,
            c.weekday,
            c.month,
            c.year,
            c.event_name,
            c.event_type,
            CASE
                WHEN s.state_id = 'CA' THEN c.snap_CA
                WHEN s.state_id = 'TX' THEN c.snap_TX
                WHEN s.state_id = 'WI' THEN c.snap_WI
                ELSE 0
            END AS snap
        FROM sales s
        INNER JOIN calendar c
            ON s.d = c.d
        LEFT JOIN prices p
            ON s.store_id = p.store_id
            AND s.item_id = p.item_id
            AND c.wm_yr_wk = p.wm_yr_wk
        LIMIT 10
    """).fetchdf()

    print("\nIntegrated sample:")
    print(result)

    print("\nIntegration test completed successfully.")

    con.close()

    print(f"\nDuckDB database saved to: {DB_PATH}")


if __name__ == "__main__":
    main()
