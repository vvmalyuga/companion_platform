# Companion Data Platform — local-first demo

Production-like Data Platform for «Компаньон»: a web service for finding companions for walks, events, sport, communication, hobbies and leisure.

**Main goal:** the whole platform runs locally on a normal laptop with Docker Compose. Yandex Cloud/Terraform is optional only and is not required for the demo.

## Local-first architecture

- No paid cloud services are required.
- Managed Kafka is replaced by a local Kafka container.
- S3/Object Storage is replaced by MinIO.
- Cloud VM is replaced by the local Docker environment.
- Airflow, Kafka, Spark, Flink, Feast, ClickHouse, Grafana, Cube.js, FastAPI, frontend SPA, PostgreSQL, Redis and MinIO run through Docker Compose.

## Minimum laptop requirements

| Resource | Minimum | Recommended |
|---|---:|---:|
| CPU | 4 cores | 6-8 cores |
| RAM | 12 GB | 16-24 GB |
| Disk | 20 GB free | 40 GB free |
| Runtime | Docker Engine + Compose plugin | Docker Desktop or Linux Docker Engine |

## Install Docker

Linux:

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker "$USER"
newgrp docker
docker version
docker compose version
```

macOS/Windows: install Docker Desktop, enable WSL2 integration on Windows, then run `docker version` and `docker compose version`.

## One-command local startup

```bash
cp .env.local .env
make up
```

Equivalent raw Docker Compose command:

```bash
docker compose --env-file .env.local -f docker/docker-compose.yml up -d --build
```

The startup automatically creates Kafka topics, MinIO buckets, PostgreSQL tables/seed data, Airflow metadata/admin user/MinIO connection, ClickHouse schema/seed data, Grafana provisioning and local service healthchecks.

## Service URLs

| Service | URL | Credentials |
|---|---|---|
| Frontend SPA | http://localhost:8082 | no login required |
| FastAPI Swagger/OpenAPI | http://localhost:8000/docs | no login required |
| Airflow | http://localhost:8080 | `admin` / `admin` by default |
| Grafana | http://localhost:3000 | `admin` / `admin` by default |
| MinIO | http://localhost:9001 | `minioadmin` / `minioadmin` |
| Cube.js | http://localhost:4000 | token from `CUBEJS_API_SECRET` |
| Flink UI | http://localhost:8081 | no login required |
| ClickHouse HTTP | http://localhost:8123 | `default` / `clickhouse` |

## Verify everything works

```bash
make health
make smoke
make demo
make feast-samples
make feast-smoke
```

## Demo data flow

1. `event-generator` produces `user_registered`, `booking_created`, `booking_cancelled`, `message_sent`, `review_added`, `companion_online` into local Kafka topics.
2. `stream-clickhouse-sink` consumes Kafka and writes realtime rows into ClickHouse.
3. Flink can run 5-minute sliding-window aggregations into ClickHouse gold metrics.
4. Grafana and Cube.js read ClickHouse metrics.
5. Frontend SPA reads the operational API through nginx `/api` and analytics through `/cubejs-api`.
6. Airflow ingests API/CSV sources, runs Great Expectations validation, writes Bronze Parquet to MinIO and logs lineage.
7. Spark jobs transform Bronze → Silver → Gold and produce ML feature files.
8. Feast materializes feature files to Redis and supports retrieval.

## Repository structure

```text
/project
  docker/           local Docker Compose stack
  terraform/        optional cloud module only
  airflow/          DAGs, plugins, logs, data mounts
  spark/            bronze→silver and silver→gold PySpark jobs
  feast/            Feast feature repo and local Dockerfile
  flink/            PyFlink streaming job
  clickhouse/       realtime and gold serving tables
  cubejs/           semantic layer schemas
  frontend/         mobile-first SPA and nginx proxy
  backend/          FastAPI + SQLAlchemy modules
  grafana/          datasource and dashboard provisioning
  docs/             local runbook, ADR, architecture and data product docs
  scripts/          local start/stop/reset, health, demo, backup/restore
  .gitlab-ci.yml    CI/CD pipeline
```

## Data domains

1. `user_management`: registration, authorization, roles, profiles, subscriptions.
2. `companion_catalog`: companion profiles, categories, tags, schedules, ratings.
3. `booking_management`: bookings, statuses, cancellations, meeting history.
4. `messaging_engagement`: messages, activity, views and interactions.
5. `analytics_recommendation`: ML features, recommendations, aggregates and behavioral analytics.

## Documentation

- Local runbook: [`docs/local-development.md`](docs/local-development.md).
- Final architecture: [`docs/final-architecture.md`](docs/final-architecture.md).
- Defense demo scenario and complete data flow: [`docs/demo-defense-scenario.md`](docs/demo-defense-scenario.md).
- Requirements checklist: [`docs/requirements-compliance.md`](docs/requirements-compliance.md).
- Final ready-for-defense state: [`docs/final-ready-for-defense.md`](docs/final-ready-for-defense.md).

## Stop/reset

```bash
make down
make reset
```

## Optional Terraform

Terraform under `terraform/` is optional and intended only for users who want to provision a cloud lab manually. The default and supported project demonstration is fully local through Docker Compose.
