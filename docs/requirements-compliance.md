# Requirements compliance checklist

| Requirement | Implementation |
|---|---|
| Local-first infrastructure | `docker/docker-compose.yml`, `.env.local`, MinIO, local Kafka, local Docker environment; `terraform/` is optional only. |
| Docker Compose local runtime | `docker/docker-compose.yml` and service Dockerfiles for API, frontend, event generator and ClickHouse sink. |
| Data Mesh/Data Products | `docs/data-products/*`, especially `booking_management` SLA and quality metrics. |
| Airflow ETL/ELT | `airflow/dags/companion_data_platform.py` with API/CSV ingestion, retries and validation. |
| Spark lakehouse | `spark/jobs/bronze_to_silver.py`, `spark/jobs/silver_to_gold.py`. |
| Kafka + Flink streaming | Kafka topics/generator and `flink/jobs/companion_streaming_job.py`. |
| Great Expectations | Airflow DAG executes GE checks for bookings, companions and users. |
| Feast | `feast/companion_platform/feature_repo/*`, `feast/Dockerfile`, `make feast-samples`, `make feast-smoke`. |
| ClickHouse | `clickhouse/init.sql` realtime and gold serving tables with seed metrics. |
| Grafana | datasource and dashboards under `grafana/`. |
| Cube.js | `cubejs/schema/CompanionActivity.js` semantic measures/dimensions. |
| FastAPI/PostgreSQL/SQLAlchemy | backend uses FastAPI, SQLAlchemy repository and PostgreSQL connection in Compose. |
| Vanilla SPA | `frontend/` implements hash routing and responsive UI. |
| GitLab CI/CD | `.gitlab-ci.yml` stages test/lint/quality/build/deploy. |
| Observability | healthchecks, Grafana, lineage logger, DAG alerts, Prometheus scrape config. |
| Demo and run scripts | `scripts/start_local.sh`, `scripts/stop_local.sh`, `scripts/reset_local.sh`, `scripts/healthcheck_stack.sh`, `scripts/run_demo_flow.sh`, backup/restore and smoke scripts. |
