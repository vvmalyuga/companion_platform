#!/usr/bin/env bash
set -euo pipefail
COMPOSE_FILE="${COMPOSE_FILE:-docker/docker-compose.yml}"
ENV_FILE="${ENV_FILE:-.env.local}"
if [[ ! -f "$ENV_FILE" ]]; then
  cp .env.local "$ENV_FILE"
fi
printf 'Starting Companion local platform with %s and %s\n' "$COMPOSE_FILE" "$ENV_FILE"
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" up -d --build
bash scripts/healthcheck_stack.sh
printf '\nLocal platform is ready:\n- Frontend: http://localhost:8082\n- API docs: http://localhost:8000/docs\n- Airflow: http://localhost:8080\n- Grafana: http://localhost:3000\n- MinIO: http://localhost:9001\n- Cube.js: http://localhost:4000\n'
