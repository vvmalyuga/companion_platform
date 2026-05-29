#!/usr/bin/env bash
set -euo pipefail
COMPOSE_FILE="${COMPOSE_FILE:-docker/docker-compose.yml}"
ENV_FILE="${ENV_FILE:-.env.local}"
[[ -f "$ENV_FILE" ]] || cp .env.local "$ENV_FILE"
BACKUP_DIR="${1:?Usage: scripts/restore.sh backups/YYYYmmddTHHMMSSZ}"

test -f "$BACKUP_DIR/postgres.sql"
docker compose --env-file "${ENV_FILE:-.env.local}" -f "$COMPOSE_FILE" exec -T postgres psql -U "${POSTGRES_USER:-airflow}" "${POSTGRES_DB:-airflow}" < "$BACKUP_DIR/postgres.sql"
if [[ -d "$BACKUP_DIR/minio" ]]; then
  docker cp "$BACKUP_DIR/minio/." companion-minio:/data/
fi
printf 'Restore completed from %s\n' "$BACKUP_DIR"
