DROP TABLE IF EXISTS companion_activity_queue;
DROP TABLE IF EXISTS companion_activity;
DROP VIEW IF EXISTS companion_activity_mv;

CREATE TABLE companion_activity_queue (
    companion_id String,
    window_start DateTime,
    total_events UInt32,
    unique_events UInt32
) ENGINE = Kafka
SETTINGS kafka_broker_list = 'kafka:9092',
         kafka_topic_list = 'companion_activity',
         kafka_group_name = 'clickhouse_reader',
         kafka_format = 'JSONEachRow';

CREATE TABLE companion_activity (
    companion_id String,
    window_start DateTime,
    total_events UInt32,
    unique_events UInt32
) ENGINE = MergeTree() ORDER BY (companion_id, window_start);

CREATE MATERIALIZED VIEW companion_activity_mv TO companion_activity AS
SELECT * FROM companion_activity_queue;
