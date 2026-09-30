import duckdb

DB_PATH = "data/retail.duckdb"


def main():
    print("Connecting to DuckDB...")
    con = duckdb.connect(DB_PATH)

    print("\n========== EXPLORATORY DATA ANALYSIS ==========")

    # 1. Total sales by state
    print("\n--- Sales by State ---")

    state_sales = con.execute("""
        SELECT
            state_id,
            SUM(sales) AS total_sales
        FROM sales
        GROUP BY state_id
        ORDER BY total_sales DESC
    """).fetchdf()

    print(state_sales)

    # 2. Sales by category
    print("\n--- Sales by Category ---")

    category_sales = con.execute("""
        SELECT
            cat_id,
            SUM(sales) AS total_sales
        FROM sales
        GROUP BY cat_id
        ORDER BY total_sales DESC
    """).fetchdf()

    print(category_sales)

    # 3. Sales by department
    print("\n--- Top 10 Departments ---")

    department_sales = con.execute("""
        SELECT
            dept_id,
            SUM(sales) AS total_sales
        FROM sales
        GROUP BY dept_id
        ORDER BY total_sales DESC
        LIMIT 10
    """).fetchdf()

    print(department_sales)

    # 4. Top 10 items
    print("\n--- Top 10 Items by Sales ---")

    item_sales = con.execute("""
        SELECT
            item_id,
            SUM(sales) AS total_sales
        FROM sales
        GROUP BY item_id
        ORDER BY total_sales DESC
        LIMIT 10
    """).fetchdf()

    print(item_sales)

    # 5. Daily sales trend
    print("\n--- Daily Sales Trend Sample ---")

    daily_sales = con.execute("""
        SELECT
            c.date,
            SUM(s.sales) AS total_sales
        FROM sales s
        JOIN calendar c
            ON s.d = c.d
        GROUP BY c.date
        ORDER BY c.date
        LIMIT 10
    """).fetchdf()

    print(daily_sales)

    # 6. Overall sales statistics
    print("\n--- Overall Sales Statistics ---")

    statistics = con.execute("""
        SELECT
            SUM(sales) AS total_sales,
            AVG(sales) AS average_daily_record_sales,
            MAX(sales) AS maximum_sales
        FROM sales
    """).fetchdf()

    print(statistics)

    print("\nEDA completed successfully.")

    con.close()


if __name__ == "__main__":
    main()
    