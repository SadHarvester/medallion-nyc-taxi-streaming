from __future__ import annotations

from pathlib import Path

import duckdb

from streaming.config import DUCKDB_PATH, PROJECT_ROOT

SQL_FILES = [
    "sql/00_create_streaming_bronze.sql",
    "sql/01_bronze.sql",
    "sql/02_silver.sql",
    "sql/03_gold.sql",
]


def run_sql_file(con: duckdb.DuckDBPyConnection, sql_file: str) -> None:
    path = PROJECT_ROOT / sql_file
    print(f"[sql] running {sql_file}")
    con.execute(path.read_text(encoding="utf-8"))


def main() -> None:
    con = duckdb.connect(DUCKDB_PATH)
    try:
        for sql_file in SQL_FILES:
            run_sql_file(con, sql_file)
        print("Medallion transformations finished: Bronze -> Silver -> Gold.")
    finally:
        con.close()


if __name__ == "__main__":
    main()
