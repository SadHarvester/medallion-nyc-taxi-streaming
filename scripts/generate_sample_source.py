from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from streaming.config import RAW_LOOKUPS_DIR, RAW_YELLOW_DIR


def generate_trips(rows: int, target: Path) -> Path:
    target.parent.mkdir(parents=True, exist_ok=True)
    base = pd.Timestamp("2024-01-01 08:00:00")
    df = pd.DataFrame(
        {
            "VendorID": [(i % 2) + 1 for i in range(rows)],
            "tpep_pickup_datetime": [base + pd.Timedelta(minutes=i) for i in range(rows)],
            "tpep_dropoff_datetime": [base + pd.Timedelta(minutes=i + 10) for i in range(rows)],
            "passenger_count": [(i % 4) + 1 for i in range(rows)],
            "trip_distance": [round(1.0 + (i % 25) * 0.3, 2) for i in range(rows)],
            "RatecodeID": [1 for _ in range(rows)],
            "store_and_fwd_flag": ["N" for _ in range(rows)],
            "PULocationID": [(i % 5) + 1 for i in range(rows)],
            "DOLocationID": [((i + 1) % 5) + 1 for i in range(rows)],
            "payment_type": [1 for _ in range(rows)],
            "fare_amount": [round(8.0 + (i % 20) * 0.7, 2) for i in range(rows)],
            "extra": [1.0 for _ in range(rows)],
            "mta_tax": [0.5 for _ in range(rows)],
            "tip_amount": [round(1.0 + (i % 8) * 0.25, 2) for i in range(rows)],
            "tolls_amount": [0.0 for _ in range(rows)],
            "improvement_surcharge": [0.3 for _ in range(rows)],
            "total_amount": [round(10.8 + (i % 20) * 0.9, 2) for i in range(rows)],
            "congestion_surcharge": [2.5 for _ in range(rows)],
        }
    )
    df.to_parquet(target, index=False)
    return target


def generate_zones(target: Path) -> Path:
    target.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(
        {
            "LocationID": [1, 2, 3, 4, 5],
            "Borough": ["Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island"],
            "Zone": ["Midtown Center", "Williamsburg", "Astoria", "Mott Haven", "St. George"],
            "service_zone": ["Yellow Zone", "Boro Zone", "Boro Zone", "Boro Zone", "Boro Zone"],
        }
    )
    df.to_csv(target, index=False)
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a small local sample source for quick offline tests.")
    parser.add_argument("--rows", type=int, default=1000)
    parser.add_argument("--month", default="2024-01")
    args = parser.parse_args()

    trip_path = RAW_YELLOW_DIR / f"yellow_tripdata_{args.month}.parquet"
    zone_path = RAW_LOOKUPS_DIR / "taxi_zone_lookup.csv"
    generate_trips(args.rows, trip_path)
    generate_zones(zone_path)
    print(f"Generated sample trip data: {trip_path}")
    print(f"Generated sample lookup data: {zone_path}")


if __name__ == "__main__":
    main()
