CREATE STREAM events_stream (
    event_id VARCHAR,
    companion_id VARCHAR,
    event_type VARCHAR,
    event_time BIGINT
) WITH (KAFKA_TOPIC='events', VALUE_FORMAT='JSON');

CREATE TABLE companion_activity WITH (KAFKA_TOPIC='companion_activity', VALUE_FORMAT='JSON') AS
SELECT companion_id,
       COUNT(*) AS total_events,
       COUNT_DISTINCT(event_type) AS unique_events
FROM events_stream
WINDOW TUMBLING (SIZE 5 MINUTES)
GROUP BY companion_id;
