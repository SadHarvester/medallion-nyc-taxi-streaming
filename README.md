# Medallion NYC Taxi Streaming

This project extends the previous `medallion-nyc-taxi-orchestrated` pipeline with a queue-based streaming ingestion layer.

The main goal is to show that source data is no longer loaded directly into the Bronze layer. Instead, data is automatically read by a producer process, injected into a Kafka-compatible queue, consumed from that queue, and then written into the Bronze layer.

```text
NYC Taxi Source Data
        |
        v
Producer / Trigger
        |
        v
Kafka-compatible Queue: Redpanda topic nyc_taxi_raw
        |
        v
Consumer
        |
        v
Bronze Streaming Table in DuckDB
        |
        v
Silver Cleaning Layer
        |
        v
Gold Aggregation Layer
        |
        v
Data Quality Checks / Analytics
```

## Technology stack

- Python - producer, consumer, orchestration scripts
- Redpanda - Kafka-compatible queue system
- DuckDB - local analytical warehouse
- SQL - Bronze, Silver and Gold transformations
- Dagster - default trigger/orchestration layer
- Airflow DAG - optional example trigger
- NYC Yellow Taxi data - source dataset

## Project structure

```text
medallion-nyc-taxi-streaming/
├── airflow/dags/nyc_taxi_streaming_dag.py       # optional Airflow trigger
├── data/raw/lookups/.gitkeep                    # local lookup data folder
├── data/raw/yellow/.gitkeep                     # local source parquet folder
├── docs/architecture_streaming.md               # updated architecture
├── orchestration/dagster_pipeline.py            # Dagster jobs and schedule
├── scripts/
│   ├── download_data.py                         # downloads NYC source files
│   ├── generate_sample_source.py                # small offline demo source
│   ├── run_streaming_ingestion.py               # source -> queue -> Bronze
│   ├── run_pipeline.py                          # Bronze -> Silver -> Gold
│   ├── run_data_quality_checks.py               # data quality summary
│   ├── check_results.py                         # result inspection
│   └── main.py                                  # central entry point
├── sql/
│   ├── 00_create_streaming_bronze.sql
│   ├── 01_bronze.sql
│   ├── 02_silver.sql
│   ├── 03_gold.sql
│   └── 04_data_quality_checks.sql
├── streaming/
│   ├── config.py
│   ├── kafka_utils.py
│   ├── producer.py
│   └── consumer_to_bronze.py
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Assignment mapping

| Requirement | Implementation |
|---|---|
| Added queue system while moving the data | Redpanda/Kafka topic `nyc_taxi_raw` between source reader and Bronze |
| Data is read and injected automatically from the source | `streaming.producer` reads NYC Taxi Parquet data and sends messages to the queue |
| Airflow/trigger | Dagster jobs and schedule are included; optional Airflow DAG is also included |
| Updated architecture | `docs/architecture_streaming.md` describes the queue-based architecture |

## Quick start - recommended Windows flow

### 1. Open the project in VS Code

Open the folder `medallion-nyc-taxi-streaming`.

### 2. Create and activate virtual environment

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Start the queue system

Docker Desktop must be running.

```powershell
docker compose up -d
```

Redpanda Console will be available at:

```text
http://localhost:8080
```

### 5. Option A - run a small local demo first

This avoids downloading the real NYC file and lets you verify the whole pipeline quickly.

```powershell
python scripts/generate_sample_source.py --rows 1000 --month 2024-01
python scripts/main.py --mode full
python scripts/main.py --mode check
```

### 5. Option B - run with real NYC Taxi source data

This downloads the selected NYC Yellow Taxi Parquet file and the taxi zone lookup CSV.

```powershell
python scripts/main.py --mode full
python scripts/main.py --mode check
```

The default month is `2024-01`. To change it, set environment variable:

```powershell
$env:NYC_TAXI_MONTH="2024-02"
python scripts/main.py --mode full
```

## Main commands

```powershell
# Source -> Queue -> Bronze only
python scripts/main.py --mode streaming

# Bronze -> Silver -> Gold only
python scripts/main.py --mode transform

# Full flow: Streaming ingestion + transformations + DQ checks
python scripts/main.py --mode full

# Incremental-style flow with state update
python scripts/main.py --mode incremental

# Data quality checks only
python scripts/main.py --mode dq

# Inspect output tables
python scripts/main.py --mode check
```

## Dagster orchestration

Start Dagster UI:

```powershell
python -m dagster dev -f orchestration/dagster_pipeline.py
```

Available jobs:

- `streaming_ingestion_job`
- `streaming_medallion_job`
- `medallion_transform_only_job`

There is also a schedule named `streaming_medallion_every_30_minutes`.

## Optional Airflow trigger

An optional DAG is included in:

```text
airflow/dags/nyc_taxi_streaming_dag.py
```

The project does not require Airflow to run. Dagster is the default trigger/orchestration layer.

## What is created in DuckDB

The local warehouse file is:

```text
warehouse.duckdb
```

Main tables:

- `bronze_yellow_trips_streaming` - append-style records consumed from the queue
- `bronze_yellow_trips` - canonical Bronze table
- `bronze_taxi_zones` - lookup/reference data
- `silver_yellow_trips` - cleaned trip records
- `gold_monthly_borough_stats` - monthly borough-level aggregation
- `gold_daily_revenue` - daily revenue aggregation
- `data_quality_summary` - basic data quality check output

## GitHub setup as separate project

```powershell
git init
git add .
git commit -m "Add NYC Taxi streaming medallion pipeline"
git branch -M main
git remote add origin https://github.com/SadHarvester/medallion-nyc-taxi-streaming.git
git push -u origin main
```

Do not commit local generated files such as:

- `.venv/`
- `warehouse.duckdb`
- `data/raw/yellow/*.parquet`
- `data/raw/lookups/*.csv`
- `.tmp_dagster_home_*/`

They are already ignored in `.gitignore`.

## Troubleshooting

### Kafka/Redpanda is not reachable

Run:

```powershell
docker compose ps
docker compose up -d
```

### Docker is not running

Start Docker Desktop and then run:

```powershell
docker compose up -d
```

### Consumer reads zero messages

For local demos the consumer uses `--reset-offsets` through `scripts/run_streaming_ingestion.py`, so it should read from the beginning of the topic. If you run consumer manually, add:

```powershell
python -m streaming.consumer_to_bronze --reset-offsets
```

### Port conflict on 9092 or 8080

Another Kafka/Redpanda instance or web service may already be using the port. Stop it or change the mapped ports in `docker-compose.yml`.
