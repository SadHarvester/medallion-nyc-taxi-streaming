from __future__ import annotations

import duckdb

from streaming.config import DUCKDB_PATH

TABLES = [
    "bronze_yellow_trips_streaming",
    "bronze_yellow_trips",
    "silver_yellow_trips",
    "gold_monthly_borough_stats",
    "gold_daily_revenue",
    "data_quality_summary",
]


def table_exists(con: duckdb.DuckDBPyConnection, table_name: str) -> bool:
    return bool(
        con.execute(
            """
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_name = ?
            """,
            [table_name],
        ).fetchone()[0]
    )


def main() -> None:
    con = duckdb.connect(DUCKDB_PATH)
    try:
        print("Warehouse table counts:")
        for table in TABLES:
            if table_exists(con, table):
                count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                print(f"- {table}: {count}")
            else:
                print(f"- {table}: not created yet")

        if table_exists(con, "gold_monthly_borough_stats"):
            print("\nGold monthly borough stats preview:")
            rows = con.execute(
                """
                SELECT *
                FROM gold_monthly_borough_stats
                ORDER BY trip_month, trip_count DESC
                LIMIT 10
                """
            ).fetchall()
            for row in rows:
                print(row)
    finally:
        con.close()


if __name__ == "__main__":
    main()
