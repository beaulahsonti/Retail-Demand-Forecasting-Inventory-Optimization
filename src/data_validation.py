import duckdb

DB_PATH = "data/retail.duckdb"


def main():
    print("Connecting to DuckDB...")

    con = duckdb.connect(DB_PATH)

    print("\n========== DATA VALIDATION ==========")

    # Total sales records
    total_rows = con.execute("""
        SELECT COUNT(*)
        FROM sales
    """).fetchone()[0]

    print(f"Total sales records: {total_rows:,}")

    # Unique products
    unique_items = con.execute("""
        SELECT COUNT(DISTINCT item_id)
        FROM sales
    """).fetchone()[0]

    print(f"Unique items: {unique_items:,}")

    # Unique stores
    unique_stores = con.execute("""
        SELECT COUNT(DISTINCT store_id)
        FROM sales
    """).fetchone()[0]

    print(f"Unique stores: {unique_stores:,}")

    # Sales date range
    date_range = con.execute("""
        SELECT MIN(date), MAX(date)
        FROM calendar
    """).fetchone()

    print(f"Date range: {date_range[0]} to {date_range[1]}")

    # Negative sales
    negative_sales = con.execute("""
        SELECT COUNT(*)
        FROM sales
        WHERE sales < 0
    """).fetchone()[0]

    print(f"Negative sales records: {negative_sales:,}")

    # Missing prices after joining
    missing_prices = con.execute("""
        SELECT COUNT(*)
        FROM sales s
        INNER JOIN calendar c
            ON s.d = c.d
        LEFT JOIN prices p
            ON s.store_id = p.store_id
            AND s.item_id = p.item_id
            AND c.wm_yr_wk = p.wm_yr_wk
        WHERE p.sell_price IS NULL
    """).fetchone()[0]

    print(f"Records with missing prices: {missing_prices:,}")

    # Sales by state
    state_counts = con.execute("""
        SELECT
            state_id,
            COUNT(*) AS records,
            SUM(sales) AS total_sales
        FROM sales
        GROUP BY state_id
        ORDER BY state_id
    """).fetchdf()

    print("\nSales by state:")
    print(state_counts)

    print("\nValidation completed successfully.")

    con.close()


if __name__ == "__main__":
    main()