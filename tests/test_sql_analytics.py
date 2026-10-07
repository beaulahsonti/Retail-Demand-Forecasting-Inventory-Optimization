"""
Tests for DuckDB SQL analytics outputs.
"""

from pathlib import Path
import unittest

import duckdb


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATABASE_FILE = (
    PROJECT_ROOT / "data" / "retail_demand.duckdb"
)

SQL_DIR = PROJECT_ROOT / "sql"


class TestSQLAnalytics(unittest.TestCase):

    def test_database_exists(self):
        """Verify that the DuckDB database exists."""
        self.assertTrue(
            DATABASE_FILE.exists(),
            f"Database not found: {DATABASE_FILE}"
        )

    def test_sql_directory_exists(self):
        """Verify that the SQL directory exists."""
        self.assertTrue(
            SQL_DIR.exists(),
            f"SQL directory not found: {SQL_DIR}"
        )

    def test_required_sql_files_exist(self):
        """Verify that the project's SQL analysis files exist."""
        required_files = {
            "demand_summary.sql",
            "product_analysis.sql",
            "store_analysis.sql",
            "forecast_analysis.sql",
            "inventory_analysis.sql",
        }

        existing_files = {
            file.name
            for file in SQL_DIR.glob("*.sql")
        }

        self.assertTrue(
            required_files.issubset(existing_files),
            "One or more required SQL files are missing."
        )

    def test_database_can_connect(self):
        """Verify that DuckDB can open the project database."""
        connection = duckdb.connect(
            str(DATABASE_FILE),
            read_only=True
        )

        result = connection.execute(
            "SELECT 1"
        ).fetchone()

        connection.close()

        self.assertEqual(result[0], 1)

    def test_processed_data_contains_records(self):
        """Verify that the database contains demand records."""
        connection = duckdb.connect(
            str(DATABASE_FILE),
            read_only=True
        )

        tables = connection.execute(
            "SHOW TABLES"
        ).fetchall()

        self.assertGreater(
            len(tables),
            0,
            "No tables found in the DuckDB database."
        )

        connection.close()


if __name__ == "__main__":
    unittest.main()