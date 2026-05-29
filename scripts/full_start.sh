#!/usr/bin/env bash
set -euo pipefail
COMPOSE_FILE="${COMPOSE_FILE:-docker/docker-compose.yml}"
docker compose -f "$COMPOSE_FILE" up -d --build
bash scripts/healthcheck_stack.sh
