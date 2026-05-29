from pathlib import Path

compose = Path("docker/docker-compose.yml").read_text(encoding="utf-8")
for token in [
    "healthcheck",
    "stream-clickhouse-sink",
    "event-generator",
    "feast:",
    "GF_INSTALL_PLUGINS",
    "ENABLE_KAFKA: \"true\"",
    "condition: service_healthy",
    "${DATABASE_URL",
    "minio/minio",
    "confluentinc/cp-kafka",
]:
    assert token in compose, token

for forbidden in ["yandex", "amazonaws.com", "s3.amazonaws.com"]:
    assert forbidden not in compose.lower(), forbidden

terraform = Path("terraform/main.tf").read_text(encoding="utf-8")
for token in ["yandex_storage_bucket", "yandex_mdb_kafka_cluster", "yandex_mdb_kafka_topic", "yandex_compute_instance", "yandex_vpc_security_group"]:
    assert token in terraform, token

dag = Path("airflow/dags/companion_data_platform.py").read_text(encoding="utf-8")
for token in ["retry_exponential_backoff", "great_expectations", "LineageLogger", "sendTelegramAlert", "sendSlackAlert"]:
    assert token in dag, token

for required in [
    ".env.local",
    ".env.example",
    "Makefile",
    "scripts/start_local.sh",
    "scripts/stop_local.sh",
    "scripts/reset_local.sh",
    "scripts/backup.sh",
    "scripts/restore.sh",
    "docs/local-development.md",
    "docs/final-ready-for-defense.md",
]:
    assert Path(required).exists(), required

backend = Path("backend/app/core/logging.py").read_text(encoding="utf-8")
assert "JsonFormatter" in backend

readme = Path("README.md").read_text(encoding="utf-8")
for token in ["Local-first", "No paid cloud services", "make up", "Docker Compose"]:
    assert token in readme, token

print("Static stack validation passed")
