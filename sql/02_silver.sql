CREATE OR REPLACE TABLE silver_yellow_trips AS
SELECT
    VendorID,
    CAST(tpep_pickup_datetime AS TIMESTAMP) AS pickup_ts,
    CAST(tpep_dropoff_datetime AS TIMESTAMP) AS dropoff_ts,
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
    published_at,
    ingested_at
FROM bronze_yellow_trips
WHERE tpep_pickup_datetime IS NOT NULL
  AND tpep_dropoff_datetime IS NOT NULL
  AND tpep_dropoff_datetime >= tpep_pickup_datetime
  AND trip_distance > 0
  AND total_amount >= 0
  AND PULocationID IS NOT NULL
  AND DOLocationID IS NOT NULL
  AND tpep_pickup_datetime >= TIMESTAMP '2014-01-01 00:00:00'
  AND tpep_pickup_datetime < TIMESTAMP '2026-01-01 00:00:00'
  AND tpep_dropoff_datetime >= TIMESTAMP '2014-01-01 00:00:00'
  AND tpep_dropoff_datetime < TIMESTAMP '2026-01-01 00:00:00';
