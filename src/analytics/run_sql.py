"""
DuckDB SQL Runner

Executes all SQL analysis files against
the processed retail demand dataset.
"""

from pathlib import Path

import duckdb


# -------------------------------------------------------------------
# PROJECT PATHS
# -------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SQL_DIR = (
    PROJECT_ROOT
    / "sql"
)

DATABASE_FILE = (
    PROJECT_ROOT
    / "data"
    / "retail_demand.duckdb"
)

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "clean_train.csv"
)


# -------------------------------------------------------------------
# SQL FILES
# -------------------------------------------------------------------

SQL_FILES = [
    "demand_summary.sql",
    "product_analysis.sql",
    "store_analysis.sql",
    "forecast_analysis.sql",
    "inventory_analysis.sql",
]


# -------------------------------------------------------------------
# SPLIT SQL INTO STATEMENTS
# -------------------------------------------------------------------

def split_sql_statements(sql_text):

    statements = []

    for statement in sql_text.split(";"):

        statement = statement.strip()

        if not statement:
            continue

        # Remove SQL comment-only lines
        lines = []

        for line in statement.splitlines():

            stripped = line.strip()

            if stripped.startswith("--"):
                continue

            if stripped:
                lines.append(line)

        cleaned_statement = "\n".join(lines).strip()

        if cleaned_statement:
            statements.append(cleaned_statement)

    return statements


# -------------------------------------------------------------------
# EXECUTE ONE SQL FILE
# -------------------------------------------------------------------

def execute_sql_file(
    connection,
    sql_file
):

    print()
    print("=" * 70)
    print(f"SQL FILE: {sql_file.name}")
    print("=" * 70)

    if not sql_file.exists():

        raise FileNotFoundError(
            f"SQL file not found: {sql_file}"
        )

    sql_text = sql_file.read_text(
        encoding="utf-8"
    )

    statements = split_sql_statements(
        sql_text
    )

    print(
        f"SQL statements found: "
        f"{len(statements)}"
    )

    # ---------------------------------------------------------------
    # EXECUTE EACH QUERY
    # ---------------------------------------------------------------

    for index, statement in enumerate(
        statements,
        start=1
    ):

        print()
        print("-" * 70)
        print(
            f"QUERY {index}/{len(statements)}"
        )
        print("-" * 70)

        try:

            result = connection.execute(
                statement
            ).fetchdf()

            print(
                f"Rows returned: "
                f"{len(result):,}"
            )

            # Display first 10 rows
            if not result.empty:

                print(
                    result
                    .head(10)
                    .to_string(index=False)
                )

        except Exception as error:

            print()
            print(
                f"Query {index} failed "
                f"in {sql_file.name}:"
            )

            print(error)

            print()
            print("SQL statement:")
            print(statement)

            raise


# -------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------

def main():

    print("=" * 70)
    print("DUCKDB SQL ANALYSIS")
    print("=" * 70)

    # ---------------------------------------------------------------
    # CHECK DATA FILE
    # ---------------------------------------------------------------

    if not DATA_FILE.exists():

        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}"
        )

    # ---------------------------------------------------------------
    # CHECK SQL DIRECTORY
    # ---------------------------------------------------------------

    if not SQL_DIR.exists():

        raise FileNotFoundError(
            f"SQL directory not found: {SQL_DIR}"
        )

    # ---------------------------------------------------------------
    # CHECK ALL SQL FILES
    # ---------------------------------------------------------------

    print()
    print("Checking SQL files...")

    for filename in SQL_FILES:

        sql_file = SQL_DIR / filename

        if not sql_file.exists():

            raise FileNotFoundError(
                f"SQL file not found: {sql_file}"
            )

        print(f"✓ {filename}")

    # ---------------------------------------------------------------
    # CONNECT TO DUCKDB
    # ---------------------------------------------------------------

    print()
    print("Connecting to DuckDB...")

    connection = duckdb.connect(
        str(DATABASE_FILE)
    )

    print(
        "DuckDB connection successful."
    )

    # ---------------------------------------------------------------
    # CREATE MAIN DATA VIEW
    # ---------------------------------------------------------------

    print()
    print(
        "Loading processed demand data..."
    )

    connection.execute(
        f"""
        CREATE OR REPLACE VIEW demand_data AS
        SELECT *
        FROM read_csv_auto(
            '{DATA_FILE.as_posix()}'
        );
        """
    )

    row_count = connection.execute(
        "SELECT COUNT(*) FROM demand_data"
    ).fetchone()[0]

    print(
        f"Loaded records: {row_count:,}"
    )

    # ---------------------------------------------------------------
    # DISPLAY DATA STRUCTURE
    # ---------------------------------------------------------------

    columns = connection.execute(
        "DESCRIBE demand_data"
    ).fetchdf()

    print()
    print(
        f"Demand data columns: "
        f"{len(columns)}"
    )

    # ---------------------------------------------------------------
    # EXECUTE ALL SQL FILES
    # ---------------------------------------------------------------

    print()
    print("=" * 70)
    print("EXECUTING SQL ANALYSIS FILES")
    print("=" * 70)

    for filename in SQL_FILES:

        sql_file = SQL_DIR / filename

        execute_sql_file(
            connection,
            sql_file
        )

    # ---------------------------------------------------------------
    # CLOSE CONNECTION
    # ---------------------------------------------------------------

    connection.close()

    # ---------------------------------------------------------------
    # FINAL SUMMARY
    # ---------------------------------------------------------------

    print()
    print("=" * 70)
    print("SQL ANALYSIS COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print()
    print("SQL files executed:")

    for filename in SQL_FILES:

        print(
            f"  ✓ {filename}"
        )

    print()
    print(
        f"Total records analyzed: "
        f"{row_count:,}"
    )

    print()
    print("DuckDB database:")

    print(
        DATABASE_FILE
    )

    print()
    print(
        "DuckDB connection closed."
    )


# -------------------------------------------------------------------
# RUN PROGRAM
# -------------------------------------------------------------------

if __name__ == "__main__":
    main()