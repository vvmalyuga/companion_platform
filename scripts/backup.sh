#!/usr/bin/env bash
set -euo pipefail
COMPOSE_FILE="${COMPOSE_FILE:-docker/docker-compose.yml}"
ENV_FILE="${ENV_FILE:-.env.local}"
[[ -f "$ENV_FILE" ]] || cp .env.local "$ENV_FILE"
BACKUP_ROOT="${BACKUP_ROOT:-backups}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
TARGET="$BACKUP_ROOT/$STAMP"
mkdir -p "$TARGET"

docker compose --env-file "${ENV_FILE:-.env.local}" -f "$COMPOSE_FILE" exec -T postgres pg_dump -U "${POSTGRES_USER:-airflow}" "${POSTGRES_DB:-airflow}" > "$TARGET/postgres.sql"
docker compose --env-file "${ENV_FILE:-.env.local}" -f "$COMPOSE_FILE" exec -T clickhouse clickhouse-client --password "${CLICKHOUSE_PASSWORD:-clickhouse}" --query "BACKUP DATABASE companion TO Disk('backups', '$STAMP-companion.zip')" || true
docker compose --env-file "${ENV_FILE:-.env.local}" -f "$COMPOSE_FILE" exec -T minio mc alias set local http://localhost:9000 "${MINIO_ROOT_USER:-minioadmin}" "${MINIO_ROOT_PASSWORD:-minioadmin}" >/dev/null
docker compose --env-file "${ENV_FILE:-.env.local}" -f "$COMPOSE_FILE" exec -T minio sh -c "mkdir -p /tmp/companion-backup && cp -a /data/. /tmp/companion-backup/"
docker cp companion-minio:/tmp/companion-backup "$TARGET/minio"
printf 'Backup created at %s\n' "$TARGET"
