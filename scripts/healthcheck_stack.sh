#!/usr/bin/env bash
set -euo pipefail
COMPOSE_FILE="${COMPOSE_FILE:-docker/docker-compose.yml}"
ENV_FILE="${ENV_FILE:-.env.local}"
[[ -f "$ENV_FILE" ]] || cp .env.local "$ENV_FILE"
REQUIRED=(minio kafka postgres redis redis-feast api airflow-webserver airflow-scheduler airflow-worker clickhouse grafana cubejs frontend)
unhealthy=1
for attempt in {1..60}; do
  unhealthy=0
  for service in "${REQUIRED[@]}"; do
    status=$(docker compose --env-file "${ENV_FILE:-.env.local}" -f "$COMPOSE_FILE" ps --format json "$service" | python -c 'import json,sys; data=sys.stdin.read().strip(); obj=json.loads(data) if data else {}; obj=obj[0] if isinstance(obj,list) and obj else obj; print(obj.get("Health") or obj.get("State") or "missing")' 2>/dev/null || echo missing)
    if [[ "$status" != "healthy" && "$status" != "running" ]]; then unhealthy=1; fi
  done
  [[ "$unhealthy" == 0 ]] && break
  sleep 10
done
if [[ "$unhealthy" != 0 ]]; then
  docker compose --env-file "${ENV_FILE:-.env.local}" -f "$COMPOSE_FILE" ps
  echo "Some services are not healthy" >&2
  exit 1
fi
docker compose --env-file "${ENV_FILE:-.env.local}" -f "$COMPOSE_FILE" ps
curl -fsS http://localhost:8000/api/health >/dev/null
curl -fsS http://localhost:8080/health >/dev/null
curl -fsS http://localhost:3000/api/health >/dev/null
curl -fsS http://localhost:8123/ping >/dev/null
curl -fsS http://localhost:8082 >/dev/null
