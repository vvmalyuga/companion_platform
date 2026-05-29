# Data Product: booking_management

## Domain ownership
- Domain: `booking_management`.
- Producer interfaces: Booking API (`POST /api/bookings`), Kafka topic `booking-events`, CSV backfill `data/csv/bookings.csv`.
- Consumers: gold analytics, ML features, semantic layer, embedded dashboard.

## Inputs
| Interface | Contract | Freshness |
|---|---|---|
| Booking API | `bookingId`, `customerId`, `companionId`, `bookingDate`, `status`, `amount` | real time |
| Kafka events | `booking_created`, `booking_cancelled` envelopes | ≤ 5 minutes |

## Outputs
| Output | Location | Consumers |
|---|---|---|
| Gold tables | `s3://companion-gold/top_companions`, `business_metrics` | Cube.js, Grafana |
| ML features | `s3://companion-ml/user_features`, `companion_features` | Feast |
| Analytics metrics | ClickHouse `companion.gold_business_metrics` | embedded analytics |

## SLA
- Freshness: ≤ 5 minutes for streaming and scheduled Airflow DAG.
- Uptime: 99% monthly target.
- Retry policy: 3 retries with exponential backoff in Airflow; Kafka consumers use committed offsets.

## Data quality metrics
- Duplicate rate by `booking_id`.
- Null rate for keys and `booking_date`.
- Invalid timestamps and future-date anomalies.
- Booking consistency: valid status transitions and amount > 0.
