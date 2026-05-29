#!/usr/bin/env bash
set -euo pipefail
COMPOSE_FILE="${COMPOSE_FILE:-docker/docker-compose.yml}"
ENV_FILE="${ENV_FILE:-.env.local}"
[[ -f "$ENV_FILE" ]] || cp .env.local "$ENV_FILE"
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" down
