# Streaming Assignment Requirements Mapping

Deadline: 10 May 2026, 23:59

## 1. Added queue system while moving the data in or out

Implemented.

The project uses Redpanda, a Kafka-compatible queue system, started with Docker Compose.

Relevant files:

- `docker-compose.yml`
- `streaming/producer.py`
- `streaming/consumer_to_bronze.py`
- `streaming/kafka_utils.py`

Queue topic:

```text
nyc_taxi_raw
```

Flow:

```text
NYC Taxi source data -> Producer -> Redpanda/Kafka topic -> Consumer -> DuckDB Bronze table
```

## 2. Data is read and injected automatically from the source

Implemented.

The producer reads NYC Yellow Taxi Parquet source files and publishes row-level events into the queue.

Relevant files:

- `scripts/download_data.py`
- `streaming/producer.py`
- `scripts/run_streaming_ingestion.py`

The whole ingestion can be triggered through:

```bash
python scripts/main.py --mode streaming
```

or as a complete flow:

```bash
python scripts/main.py --mode full
```

## 3. Airflow/trigger

Implemented through Dagster by default and Airflow optionally.

Default trigger/orchestration:

- `orchestration/dagster_pipeline.py`

Included jobs:

- `streaming_ingestion_job`
- `streaming_medallion_job`
- `medallion_transform_only_job`

Included schedule:

- `streaming_medallion_every_30_minutes`

Optional Airflow DAG:

- `airflow/dags/nyc_taxi_streaming_dag.py`

## 4. Updated Architecture

Implemented.

Architecture documentation:

- `docs/architecture_streaming.md`

Main update:

```text
source -> queue -> bronze -> silver -> gold
```

instead of:

```text
source -> bronze -> silver -> gold
```

## 5. How to demonstrate during review

Recommended demo sequence:

```bash
docker compose up -d
python scripts/generate_sample_source.py --rows 1000 --month 2024-01
python scripts/main.py --mode full
python scripts/main.py --mode check
python -m dagster dev -f orchestration/dagster_pipeline.py
```

In Redpanda Console open:

```text
http://localhost:8080
```

Show topic:

```text
nyc_taxi_raw
```

Show DuckDB tables:

- `bronze_yellow_trips_streaming`
- `bronze_yellow_trips`
- `silver_yellow_trips`
- `gold_monthly_borough_stats`
- `data_quality_summary`
