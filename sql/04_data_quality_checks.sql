CREATE OR REPLACE TABLE data_quality_summary AS
SELECT
    'invalid_time_order' AS check_name,
    COUNT(*) AS failed_records
FROM bronze_yellow_trips
WHERE tpep_dropoff_datetime < tpep_pickup_datetime

UNION ALL

SELECT
    'invalid_distance' AS check_name,
    COUNT(*) AS failed_records
FROM bronze_yellow_trips
WHERE trip_distance <= 0 OR trip_distance IS NULL

UNION ALL

SELECT
    'missing_location_ids' AS check_name,
    COUNT(*) AS failed_records
FROM bronze_yellow_trips
WHERE PULocationID IS NULL OR DOLocationID IS NULL

UNION ALL

SELECT
    'negative_total_amount' AS check_name,
    COUNT(*) AS failed_records
FROM bronze_yellow_trips
WHERE total_amount < 0 OR total_amount IS NULL;
