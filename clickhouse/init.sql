CREATE DATABASE IF NOT EXISTS companion;

CREATE TABLE IF NOT EXISTS companion.realtime_bookings (
    event_time DateTime,
    booking_id String,
    companion_id String,
    customer_id String,
    status LowCardinality(String),
    amount Float64
) ENGINE = MergeTree ORDER BY (event_time, booking_id);

CREATE TABLE IF NOT EXISTS companion.realtime_activity (
    event_time DateTime,
    event_type LowCardinality(String),
    user_id String,
    city String
) ENGINE = MergeTree ORDER BY (event_time, event_type);

CREATE TABLE IF NOT EXISTS companion.realtime_companion_stats (
    event_time DateTime,
    companion_id String,
    online UInt8,
    response_time_seconds UInt32,
    avg_rating Float32
) ENGINE = MergeTree ORDER BY (event_time, companion_id);

CREATE TABLE IF NOT EXISTS companion.gold_business_metrics (
    metric_date Date,
    category String,
    city String,
    user_count UInt64,
    booking_count UInt64,
    avg_rating Float32,
    revenue Float64,
    active_companions UInt64,
    subscription_type String,
    booking_status String
) ENGINE = MergeTree ORDER BY (metric_date, category, city);

INSERT INTO companion.gold_business_metrics VALUES
    (today(), 'прогулки', 'Москва', 120, 42, 4.9, 104000, 18, 'premium', 'completed'),
    (today(), 'спорт', 'Санкт-Петербург', 75, 27, 4.7, 58000, 11, 'basic', 'completed'),
    (today(), 'мероприятия', 'Казань', 62, 19, 4.8, 43000, 9, 'premium', 'pending');

INSERT INTO companion.realtime_activity VALUES
    (now(), 'user_registered', 'usr-seed-1', 'Москва'),
    (now(), 'message_sent', 'usr-seed-2', 'Санкт-Петербург');

INSERT INTO companion.realtime_bookings VALUES
    (now(), 'bkg-seed-1', 'cmp-001', 'usr-201', 'completed', 2400),
    (now(), 'bkg-seed-2', 'cmp-002', 'usr-202', 'pending', 950);

INSERT INTO companion.realtime_companion_stats VALUES
    (now(), 'cmp-001', 1, 120, 4.9),
    (now(), 'cmp-002', 1, 240, 4.7);
