from __future__ import annotations

import argparse
from pathlib import Path

import requests

from streaming.config import (
    DEFAULT_NYC_TAXI_MONTH,
    NYC_TAXI_ZONE_LOOKUP_URL,
    NYC_TRIP_DATA_BASE_URL,
    RAW_LOOKUPS_DIR,
    RAW_YELLOW_DIR,
)


def download_file(url: str, target: Path) -> Path:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and target.stat().st_size > 0:
        print(f"[skip] {target}")
        return target

    print(f"[download] {url}")
    with requests.get(url, stream=True, timeout=180) as response:
        response.raise_for_status()
        with target.open("wb") as output_file:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    output_file.write(chunk)
    return target


def download_yellow_tripdata(month: str = DEFAULT_NYC_TAXI_MONTH) -> Path:
    filename = f"yellow_tripdata_{month}.parquet"
    url = f"{NYC_TRIP_DATA_BASE_URL}/{filename}"
    return download_file(url, RAW_YELLOW_DIR / filename)


def download_taxi_zone_lookup() -> Path:
    return download_file(NYC_TAXI_ZONE_LOOKUP_URL, RAW_LOOKUPS_DIR / "taxi_zone_lookup.csv")


def main() -> None:
    parser = argparse.ArgumentParser(description="Download source data for the NYC Taxi streaming project.")
    parser.add_argument("--month", default=DEFAULT_NYC_TAXI_MONTH, help="Month in YYYY-MM format, for example 2024-01.")
    args = parser.parse_args()

    download_yellow_tripdata(args.month)
    download_taxi_zone_lookup()
    print("Source data is ready.")


if __name__ == "__main__":
    main()
