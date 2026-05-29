#!/usr/bin/env bash
set -euo pipefail
COMPOSE_FILE="${COMPOSE_FILE:-docker/docker-compose.yml}"
ENV_FILE="${ENV_FILE:-.env.local}"
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" down -v --remove-orphans
rm -rf airflow/logs/* backups/local-reset-* 2>/dev/null || true
bash scripts/start_local.sh
