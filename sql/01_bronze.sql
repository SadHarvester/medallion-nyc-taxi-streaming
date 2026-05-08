-- Canonical Bronze layer.
-- The assignment extension loads data through the queue into bronze_yellow_trips_streaming.
-- This script exposes the queue-loaded data using the same canonical table name used later by Silver/Gold.

CREATE OR REPLACE TABLE bronze_yellow_trips AS
SELECT
    VendorID,
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    passenger_count,
    trip_distance,
    RatecodeID,
    store_and_fwd_flag,
    PULocationID,
    DOLocationID,
    payment_type,
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    improvement_surcharge,
    total_amount,
    congestion_surcharge,
    message_id,
    source_file,
    source_row_number,
    published_at,
    ingested_at
FROM bronze_yellow_trips_streaming;

CREATE OR REPLACE TABLE bronze_taxi_zones AS
SELECT *
FROM read_csv_auto('data/raw/lookups/taxi_zone_lookup.csv');
