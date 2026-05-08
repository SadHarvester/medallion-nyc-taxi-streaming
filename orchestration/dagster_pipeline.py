from __future__ import annotations

import subprocess
import sys

from dagster import Definitions, ScheduleDefinition, job, op


def run_python_script(script_path: str) -> None:
    subprocess.run([sys.executable, script_path], check=True)


@op
def run_streaming_ingestion() -> None:
    """Read data automatically from source and inject it into Bronze through Kafka/Redpanda."""
    run_python_script("scripts/run_streaming_ingestion.py")


@op
def run_medallion_transformations() -> None:
    """Transform Bronze data into Silver and Gold layers."""
    run_python_script("scripts/run_pipeline.py")


@op
def run_data_quality_checks() -> None:
    """Create and display data quality check results."""
    run_python_script("scripts/run_data_quality_checks.py")


@job
def streaming_ingestion_job() -> None:
    run_streaming_ingestion()


@job
def streaming_medallion_job() -> None:
    run_streaming_ingestion()
    run_medallion_transformations()
    run_data_quality_checks()


@job
def medallion_transform_only_job() -> None:
    run_medallion_transformations()
    run_data_quality_checks()


streaming_medallion_schedule = ScheduleDefinition(
    job=streaming_medallion_job,
    cron_schedule="*/30 * * * *",
    name="streaming_medallion_every_30_minutes",
)


defs = Definitions(
    jobs=[
        streaming_ingestion_job,
        streaming_medallion_job,
        medallion_transform_only_job,
    ],
    schedules=[streaming_medallion_schedule],
)
