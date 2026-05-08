from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

STATE_FILE = Path("state/pipeline_state.json")


def load_state() -> dict:
    if not STATE_FILE.exists():
        return {}
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))


def save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def run(command: list[str]) -> None:
    print("[run] " + " ".join(command))
    subprocess.run(command, check=True)


def main() -> None:
    state = load_state()
    print("STEP 1: Incremental streaming ingestion")
    run([sys.executable, "scripts/run_streaming_ingestion.py"])

    print("STEP 2: Rebuilding canonical medallion tables from current Bronze")
    run([sys.executable, "scripts/run_pipeline.py"])

    print("STEP 3: Running data quality checks")
    run([sys.executable, "scripts/run_data_quality_checks.py"])

    state["last_run_mode"] = "incremental"
    state["last_run_at_utc"] = datetime.now(timezone.utc).isoformat()
    save_state(state)
    print("INCREMENTAL streaming pipeline finished successfully.")


if __name__ == "__main__":
    main()
