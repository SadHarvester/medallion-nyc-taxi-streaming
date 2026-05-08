from __future__ import annotations

import argparse
import subprocess
import sys

from scripts.download_data import download_taxi_zone_lookup
from streaming.config import DEFAULT_MAX_MESSAGES, DEFAULT_NYC_TAXI_MONTH
from streaming.kafka_utils import wait_for_kafka


def run_command(command: list[str]) -> None:
    print("[run] " + " ".join(command))
    subprocess.run(command, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run source -> queue -> Bronze ingestion.")
    parser.add_argument("--month", default=DEFAULT_NYC_TAXI_MONTH)
    parser.add_argument("--max-messages", type=int, default=DEFAULT_MAX_MESSAGES)
    parser.add_argument("--skip-download", action="store_true")
    args = parser.parse_args()

    wait_for_kafka()

    if not args.skip_download:
        download_taxi_zone_lookup()

    run_command(
        [
            sys.executable,
            "-m",
            "streaming.producer",
            "--month",
            args.month,
            "--max-messages",
            str(args.max_messages),
        ]
    )
    run_command(
        [
            sys.executable,
            "-m",
            "streaming.consumer_to_bronze",
            "--max-messages",
            str(args.max_messages),
            "--reset-offsets",
        ]
    )
    print("Streaming ingestion finished: source -> Kafka/Redpanda -> Bronze table.")


if __name__ == "__main__":
    main()
