import duckdb

DB_PATH = "data/retail.duckdb"


def main():
    print("Connecting to DuckDB...")
    con = duckdb.connect(DB_PATH)

    print("\n========== TREND & SEASONALITY ANALYSIS ==========")

    # 1. Monthly sales trend
    print("\n--- Monthly Sales Trend ---")

    monthly_sales = con.execute("""
        SELECT
            DATE_TRUNC('month', c.date) AS month,
            SUM(s.sales) AS total_sales
        FROM sales s
        JOIN calendar c
            ON s.d = c.d
        GROUP BY 1
        ORDER BY 1
    """).fetchdf()

    print(monthly_sales.head(12))

    # 2. Day-of-week demand
    print("\n--- Day-of-Week Demand ---")

    weekday_sales = con.execute("""
        SELECT
            c.wday,
            c.weekday,
            SUM(s.sales) AS total_sales,
            AVG(s.sales) AS average_sales
        FROM sales s
        JOIN calendar c
            ON s.d = c.d
        GROUP BY c.wday, c.weekday
        ORDER BY c.wday
    """).fetchdf()

    print(weekday_sales)

    # 3. Yearly sales
    print("\n--- Yearly Sales ---")

    yearly_sales = con.execute("""
        SELECT
            c.year,
            SUM(s.sales) AS total_sales
        FROM sales s
        JOIN calendar c
            ON s.d = c.d
        GROUP BY c.year
        ORDER BY c.year
    """).fetchdf()

    print(yearly_sales)

    # 4. SNAP comparison by state
    print("\n--- SNAP Sales by State ---")

    snap_sales = con.execute("""
        SELECT
            s.state_id,
            SUM(
                CASE
                    WHEN s.state_id = 'CA' THEN c.snap_CA
                    WHEN s.state_id = 'TX' THEN c.snap_TX
                    WHEN s.state_id = 'WI' THEN c.snap_WI
                    ELSE 0
                END
            ) AS snap_days_observed,
            SUM(s.sales) AS total_sales
        FROM sales s
        JOIN calendar c
            ON s.d = c.d
        GROUP BY s.state_id
        ORDER BY s.state_id
    """).fetchdf()

    print(snap_sales)

    print("\nTrend and seasonality analysis completed successfully.")

    con.close()


if __name__ == "__main__":
    main()