# Local-first Companion Data Platform

This is the primary way to run the project. It does **not** require Yandex Cloud, AWS, GCP or paid managed services. Every required component runs as a Docker container on a laptop.

## Minimum laptop requirements

| Resource | Minimum | Recommended |
|---|---:|---:|
| CPU | 4 cores | 6-8 cores |
| RAM | 12 GB | 16-24 GB |
| Disk | 20 GB free | 40 GB free |
| OS | Linux, macOS, Windows + WSL2 | Linux or WSL2 |

## Install Docker

### Linux
```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker "$USER"
newgrp docker
docker version
docker compose version
```

### macOS / Windows
Install Docker Desktop, enable WSL2 integration on Windows, then verify:
```bash
docker version
docker compose version
```

## One-command local startup

```bash
cp .env.local .env
docker compose --env-file .env.local -f docker/docker-compose.yml up -d --build
```

Equivalent Make command:
```bash
make up
```

The startup automatically performs:
- Kafka topic creation: `booking-events`, `user-events`, `chat-events`, `companion-events`, `analytics-events`.
- MinIO bucket creation: `companion-bronze`, `companion-silver`, `companion-gold`, `companion-ml`, `companion-logs`.
- PostgreSQL initialization and FastAPI table creation/seed data.
- Airflow DB migration, admin user creation and MinIO connection registration.
- ClickHouse schema and demo metric seed insertion.
- Grafana datasource/dashboard provisioning.

## Service URLs

| Service | URL | Credentials |
|---|---|---|
| Frontend SPA | http://localhost:8082 | no login required |
| FastAPI OpenAPI | http://localhost:8000/docs | no login required |
| Airflow | http://localhost:8080 | `admin` / `admin` by default |
| Grafana | http://localhost:3000 | `admin` / `admin` by default |
| MinIO | http://localhost:9001 | `minioadmin` / `minioadmin` |
| Cube.js | http://localhost:4000 | token from `CUBEJS_API_SECRET` |
| Flink UI | http://localhost:8081 | no login required |
| ClickHouse | http://localhost:8123 | `default` / `clickhouse` |

## Verify the stack

```bash
make health
make smoke
make demo
make feast-samples
make feast-smoke
```

## Full local demo scenario

1. Open http://localhost:8082 and browse Home/Catalog/Profile/Booking.
2. Run `make demo` to create a booking through FastAPI and trigger Airflow ingestion.
3. Verify Kafka topics:
   ```bash
   docker compose --env-file .env.local -f docker/docker-compose.yml exec kafka kafka-topics --bootstrap-server kafka:9092 --list
   ```
4. Verify realtime ClickHouse rows:
   ```bash
   curl 'http://localhost:8123/?query=SELECT%20count()%20FROM%20companion.realtime_bookings'
   ```
5. Open Grafana dashboards and Cube.js API.
6. Run Spark jobs from the Spark container when Airflow has produced Bronze data:
   ```bash
   docker compose --env-file .env.local -f docker/docker-compose.yml exec spark spark-submit /opt/companion/spark/jobs/bronze_to_silver.py
   docker compose --env-file .env.local -f docker/docker-compose.yml exec spark spark-submit /opt/companion/spark/jobs/silver_to_gold.py
   ```

## Stop and reset

```bash
bash scripts/stop_local.sh
bash scripts/reset_local.sh
```

## Optional cloud module

Terraform under `terraform/` is optional and is not part of the default demo. The primary project runtime is Docker Compose + MinIO + local Kafka.
