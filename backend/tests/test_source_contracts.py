from pathlib import Path


def testFastApiRoutesExposeRequiredBusinessEndpoints():
    source = Path("backend/app/api/routes.py").read_text(encoding="utf-8")
    assert '@router.post("/auth/register")' in source
    assert '@router.get("/companions")' in source
    assert '@router.post("/bookings")' in source
    assert '@router.get("/mock/events")' in source
    assert '@router.get("/health")' in source


def testRepositoryUsesSqlAlchemyAndSeedCatalog():
    source = Path("backend/app/infra/repository.py").read_text(encoding="utf-8")
    database = Path("backend/app/infra/database.py").read_text(encoding="utf-8")
    assert "SqlAlchemyRepository" in source
    assert "create_booking" in source
    assert "CompanionRecord" in database
    assert "cmp-001" in database


def testComposeDefinesIntegratedServingServices():
    compose = Path("docker/docker-compose.yml").read_text(encoding="utf-8")
    for service in ["airflow-webserver", "airflow-scheduler", "airflow-worker", "kafka", "clickhouse", "grafana", "cubejs", "frontend"]:
        assert f"{service}:" in compose
