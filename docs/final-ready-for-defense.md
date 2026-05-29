# FINAL READY FOR DEFENSE state

## Working local services
| Service | Purpose | Validation |
|---|---|---|
| `frontend` | SPA, catalog, booking, dashboard drill-down | `GET http://localhost:8082` |
| `api` | FastAPI + SQLAlchemy operational API | `GET /api/health`, OpenAPI `/docs` |
| `postgres` | API persistence and Airflow metadata | `pg_isready` healthcheck, named volume |
| `minio` | S3-compatible bronze/silver/gold/ml/logs lakehouse | bucket init job and healthcheck |
| `kafka` | event bus with required topics | `kafka-topics --list` |
| `event-generator` | live platform events | continuously writes Kafka events |
| `stream-clickhouse-sink` | Kafka → ClickHouse realtime sink | rows appear in `realtime_*` tables |
| `jobmanager` / `taskmanager` | Flink runtime for sliding-window job | Flink UI `/overview` |
| `airflow-*` | DAG execution, retries, alerts, Great Expectations | `/health`, DAG `companion_data_platform` |
| `spark` | Bronze→Silver→Gold ELT jobs | `spark-submit spark/jobs/*.py` |
| `redis-feast` | Feast online store | Redis healthcheck |
| `clickhouse` | realtime/gold serving store | `/ping` and SQL count queries |
| `grafana` | live and business dashboards | `/api/health`, provisioned dashboards |
| `cubejs` | semantic layer API | `/readyz` and `/cubejs-api/v1/load` |

## Full demo flow
1. `event-generator` emits `user_registered`, `booking_created`, `booking_cancelled`, `message_sent`, `review_added`, `companion_online` to Kafka.
2. `stream-clickhouse-sink` consumes Kafka topics and writes realtime rows to ClickHouse.
3. Flink job can be submitted for 5-minute sliding-window aggregates into ClickHouse gold metrics.
4. Grafana reads ClickHouse realtime/gold tables.
5. Cube.js exposes semantic measures over ClickHouse.
6. Frontend reads API data through nginx `/api` proxy and displays embedded dashboard widgets.
7. Airflow reads API/CSV, validates with Great Expectations, writes Bronze Parquet, and logs lineage.
8. Spark jobs transform Bronze→Silver→Gold and write ML feature datasets for Feast.
9. Feast materializes features to Redis and supports online retrieval.

## Commands
```bash
cp .env.example .env
make up
make demo
make smoke
make feast-samples
make feast-smoke
make backup
```

## Requires external/cloud environment
- `terraform apply` requires optional Yandex Cloud credentials, folder/cloud IDs and an Ubuntu 22.04 image id.
- Optional GitLab CI deploy requires a GitLab Runner with Docker-in-Docker and deployment SSH credentials.
