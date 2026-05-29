COMPOSE_FILE ?= docker/docker-compose.yml

.PHONY: up down restart ps logs health demo smoke test lint quality validate docker-config terraform-validate backup restore reset clean

up:
	bash scripts/start_local.sh

down:
	bash scripts/stop_local.sh

restart:
	docker compose --env-file .env.local -f $(COMPOSE_FILE) restart

ps:
	docker compose --env-file .env.local -f $(COMPOSE_FILE) ps

logs:
	docker compose --env-file .env.local -f $(COMPOSE_FILE) logs -f --tail=200

health:
	bash scripts/healthcheck_stack.sh

demo:
	bash scripts/run_demo_flow.sh

smoke:
	bash scripts/smoke_analytics.sh

feast-samples:
	python scripts/generate_feast_samples.py

feast-smoke:
	docker compose --env-file .env.local -f $(COMPOSE_FILE) --profile feast run --rm feast

test:
	pytest backend/tests spark/tests

lint:
	python -m compileall backend airflow/dags airflow/plugins spark/jobs flink/jobs kafka streaming scripts

quality:
	python scripts/validate_csv_quality.py
	python scripts/validate_stack_static.py

validate: lint quality test

docker-config:
	docker compose --env-file .env.local -f $(COMPOSE_FILE) config

terraform-validate:
	terraform -chdir=terraform init -backend=false
	terraform -chdir=terraform validate

backup:
	bash scripts/backup.sh

restore:
	bash scripts/restore.sh "$${BACKUP_DIR:?Set BACKUP_DIR=/path/to/backup}"

reset:
	bash scripts/reset_local.sh

clean:
	docker compose --env-file .env.local -f $(COMPOSE_FILE) down -v --remove-orphans
