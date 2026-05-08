from __future__ import annotations

import subprocess
import sys


def run(command: list[str]) -> None:
    print("[run] " + " ".join(command))
    subprocess.run(command, check=True)


def main() -> None:
    print("STEP 1: Streaming ingestion source -> Kafka/Redpanda -> Bronze")
    run([sys.executable, "scripts/run_streaming_ingestion.py"])

    print("STEP 2: Transforming Bronze -> Silver -> Gold")
    run([sys.executable, "scripts/run_pipeline.py"])

    print("STEP 3: Running data quality checks")
    run([sys.executable, "scripts/run_data_quality_checks.py"])

    print("FULL streaming medallion pipeline finished successfully.")


if __name__ == "__main__":
    main()
