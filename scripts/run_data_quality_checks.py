from __future__ import annotations

import duckdb

from streaming.config import DUCKDB_PATH, PROJECT_ROOT


def main() -> None:
    con = duckdb.connect(DUCKDB_PATH)
    try:
        sql = (PROJECT_ROOT / "sql" / "04_data_quality_checks.sql").read_text(encoding="utf-8")
        con.execute(sql)
        rows = con.execute("SELECT * FROM data_quality_summary ORDER BY check_name").fetchall()
        print("Data quality summary:")
        for check_name, failed_records in rows:
            print(f"- {check_name}: {failed_records}")
    finally:
        con.close()


if __name__ == "__main__":
    main()
