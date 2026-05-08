from __future__ import annotations

import argparse
import subprocess
import sys


COMMAND_BY_MODE = {
    "full": ["scripts/run_full.py"],
    "incremental": ["scripts/run_incremental.py"],
    "streaming": ["scripts/run_streaming_ingestion.py"],
    "transform": ["scripts/run_pipeline.py"],
    "dq": ["scripts/run_data_quality_checks.py"],
    "check": ["scripts/check_results.py"],
}


def main() -> None:
    parser = argparse.ArgumentParser(description="NYC Taxi Streaming Medallion Pipeline")
    parser.add_argument(
        "--mode",
        choices=COMMAND_BY_MODE.keys(),
        required=True,
        help="Execution mode",
    )
    args = parser.parse_args()

    command = [sys.executable, *COMMAND_BY_MODE[args.mode]]
    print("[main] " + " ".join(command))
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
