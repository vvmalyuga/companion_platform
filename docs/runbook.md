# Local-first step-by-step launch runbook

## Prerequisites
- Docker Engine with Docker Compose plugin.
- 8+ GB RAM recommended for Airflow, Kafka, Flink, ClickHouse and Grafana.
- Optional only: Terraform CLI and Yandex Cloud credentials if you intentionally test the cloud module.

## Local startup
1. Build and start the full stack:
   ```bash
   bash scripts/start_local.sh
   ```
2. Check container health:
   ```bash
   bash scripts/healthcheck_stack.sh
   ```
3. Open services:
   - Frontend: http://localhost:8082
   - API/OpenAPI: http://localhost:8000/docs
   - Airflow: http://localhost:8080 (`admin` / `admin`)
   - Grafana: http://localhost:3000 (`admin` / `admin`)
   - Cube.js: http://localhost:4000
   - MinIO: http://localhost:9001 (`minioadmin` / `minioadmin`)

## Demo flow
1. Generate an operational booking through FastAPI:
   ```bash
   bash scripts/run_demo_flow.sh
   ```
2. Confirm Kafka topics exist:
   ```bash
   docker compose -f docker/docker-compose.yml exec kafka kafka-topics --bootstrap-server kafka:9092 --list
   ```
3. Trigger Airflow ingestion manually:
   ```bash
   docker compose -f docker/docker-compose.yml exec airflow-webserver airflow dags trigger companion_data_platform
   ```
4. Run Spark transformations:
   ```bash
   docker compose -f docker/docker-compose.yml exec spark spark-submit /opt/companion/spark/jobs/bronze_to_silver.py
   docker compose -f docker/docker-compose.yml exec spark spark-submit /opt/companion/spark/jobs/silver_to_gold.py
   ```
5. Query realtime ClickHouse metrics:
   ```bash
   curl 'http://localhost:8123/?query=SELECT%20count()%20FROM%20companion.realtime_bookings'
   ```
6. Prepare and verify Feast samples when running a local feature-store demo:
   ```bash
   make feast-samples
   make feast-smoke
   ```
7. Open Grafana dashboards and the SPA dashboard page (`#/dashboard`).

## Cloud provisioning
```bash
cd terraform
terraform init
terraform validate
terraform apply -var cloud_id=... -var folder_id=... -var public_key="$(cat ~/.ssh/id_rsa.pub)" -var ubuntu_2204_image_id=...
```
