#!/usr/bin/env bash
set -euo pipefail
COMPOSE_FILE="${COMPOSE_FILE:-docker/docker-compose.yml}"
ENV_FILE="${ENV_FILE:-.env.local}"
[[ -f "$ENV_FILE" ]] || cp .env.local "$ENV_FILE"
BOOKING_DATE=$(date -u +%Y-%m-%dT%H:%M:%SZ)
curl -fsS -X POST http://localhost:8000/api/bookings \
  -H 'Content-Type: application/json' \
  -d "{\"customerId\":\"usr-201\",\"companionId\":\"cmp-001\",\"category\":\"прогулки\",\"bookingDate\":\"$BOOKING_DATE\",\"durationHours\":2}"
echo

docker compose --env-file "${ENV_FILE:-.env.local}" -f "$COMPOSE_FILE" exec -T airflow-webserver airflow dags trigger companion_data_platform
sleep 10
docker compose --env-file "${ENV_FILE:-.env.local}" -f "$COMPOSE_FILE" exec -T airflow-webserver airflow dags state companion_data_platform "$(date -u +%Y-%m-%d)" || true
curl -fsS 'http://localhost:8123/?query=SELECT%20count()%20FROM%20companion.realtime_bookings'
echo
