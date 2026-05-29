# Demo scenario for project defense

1. **Architecture overview**: show `docs/final-architecture.md` and explain Data Mesh domains plus the `booking_management` data product SLA.
2. **Infrastructure**: show Terraform resources for buckets, Managed Kafka and VM, then start local compose with `bash scripts/full_start.sh`.
3. **Operational app**: open the SPA, filter catalog, open a companion profile and create a booking through FastAPI Swagger.
4. **Event flow**: point out API publishes booking events to Kafka and `event-generator` continuously produces user/booking/chat/review/online events.
5. **Batch flow**: trigger `companion_data_platform` in Airflow; show retries, Great Expectations validation and lineage JSONL logs.
6. **Lakehouse**: run Spark Bronze→Silver→Gold jobs and explain deduplication, schema normalization and business aggregates.
7. **Feature store**: show Feast entities and FeatureViews; run the materialization/retrieval example after Spark features are created.
8. **Streaming**: show Kafka topics, Flink sliding-window job and ClickHouse sink writing realtime rows.
9. **Analytics**: open Grafana platform/business dashboards, Cube.js schema, and embedded SPA dashboard with drill-down narrative.
10. **CI/CD**: show `.gitlab-ci.yml` stages: test, lint, quality, build and deploy.

## Full data flow
`FastAPI booking` → `Kafka booking-events` → `Flink / Kafka ClickHouse sink` → `ClickHouse realtime tables` → `Grafana + Cube.js + SPA dashboard`.

`CSV/API source` → `Airflow` → `Great Expectations` → `S3 Bronze Parquet` → `Spark Silver` → `Spark Gold + ML features` → `ClickHouse + Feast` → `semantic/embedded analytics`.
