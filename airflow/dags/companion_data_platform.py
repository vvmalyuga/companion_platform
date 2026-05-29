from __future__ import annotations

import io
import os
from datetime import datetime, timedelta
from pathlib import Path

import great_expectations as ge
import pandas as pd
import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from lineage_logger import LineageLogger

BUCKETS = ["companion-bronze", "companion-silver", "companion-gold", "companion-ml", "companion-logs"]
DATASETS = ["companions", "bookings", "reviews", "subscriptions", "users"]
CSV_ROOT = Path(os.getenv("COMPANION_CSV_ROOT", "/opt/airflow/data/csv"))


def sendTelegramAlert(context):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chatId = os.getenv("TELEGRAM_CHAT_ID")
    if token and chatId:
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id": chatId, "text": f"Airflow DAG failed: {context['dag'].dag_id}"}, timeout=10)


def sendSlackAlert(context):
    webhook = os.getenv("SLACK_WEBHOOK_URL")
    if webhook:
        requests.post(webhook, json={"text": f"Airflow DAG failed: {context['dag'].dag_id}"}, timeout=10)


def notifyFailure(context):
    sendTelegramAlert(context)
    sendSlackAlert(context)


def readApiEvents() -> pd.DataFrame:
    apiUrl = os.getenv("COMPANION_API_URL", "http://api:8000/api/mock/events")
    response = requests.get(apiUrl, timeout=10)
    response.raise_for_status()
    return pd.json_normalize(response.json())


def uploadFrameToBronze(dataset: str, frame: pd.DataFrame, ds: str, runId: str) -> None:
    buffer = io.BytesIO()
    frame.to_parquet(buffer, index=False)
    buffer.seek(0)
    hook = S3Hook(aws_conn_id="minio_conn")
    key = f"{dataset}/dt={ds}/data.parquet"
    hook.load_file_obj(buffer, key=key, bucket_name="companion-bronze", replace=True)
    LineageLogger().emit(source=f"api/csv:{dataset}", target=f"s3://companion-bronze/{key}", dataset=dataset, runId=runId)


def ingestSources(**context) -> None:
    ds = context["ds"]
    runId = context["run_id"]
    uploadFrameToBronze("api_events", readApiEvents(), ds, runId)
    for dataset in DATASETS:
        frame = pd.read_csv(CSV_ROOT / f"{dataset}.csv")
        uploadFrameToBronze(dataset, frame, ds, runId)


def validateBookings(frame: pd.DataFrame) -> None:
    gx = ge.from_pandas(frame)
    checks = [
        gx.expect_column_values_to_be_unique("booking_id"),
        gx.expect_column_values_to_be_between("rating", min_value=1, max_value=5),
        gx.expect_column_values_to_not_be_null("booking_date"),
    ]
    if not all(check["success"] for check in checks):
        raise ValueError("Booking quality validation failed")


def validateCompanions(frame: pd.DataFrame) -> None:
    gx = ge.from_pandas(frame)
    checks = [gx.expect_column_values_to_be_between("age", min_value=18, max_value=100), gx.expect_column_values_to_be_between("price_per_hour", min_value=0.01)]
    if not all(check["success"] for check in checks):
        raise ValueError("Companion quality validation failed")


def validateUsers(frame: pd.DataFrame) -> None:
    gx = ge.from_pandas(frame)
    checks = [gx.expect_column_values_to_match_regex("email", r"^[^@]+@[^@]+\\.[^@]+$"), gx.expect_column_values_to_be_in_set("role", ["customer", "companion"])]
    if not all(check["success"] for check in checks):
        raise ValueError("User quality validation failed")


def validateQuality(**context) -> None:
    validateBookings(pd.read_csv(CSV_ROOT / "bookings.csv"))
    validateCompanions(pd.read_csv(CSV_ROOT / "companions.csv"))
    validateUsers(pd.read_csv(CSV_ROOT / "users.csv"))
    LineageLogger().emit("s3://companion-bronze", "great_expectations", "quality_suite", context["run_id"])


def logLakehouseLineage(**context) -> None:
    logger = LineageLogger()
    for dataset in ["bookings", "companions", "users"]:
        logger.emit("s3://companion-bronze", "s3://companion-silver", dataset, context["run_id"])
        logger.emit("s3://companion-silver", "s3://companion-gold", dataset, context["run_id"])


default_args = {
    "owner": "data-platform",
    "retries": 3,
    "retry_delay": timedelta(minutes=1),
    "retry_exponential_backoff": True,
    "on_failure_callback": notifyFailure,
}

with DAG("companion_data_platform", start_date=datetime(2026, 5, 29), schedule_interval="*/5 * * * *", catchup=False, default_args=default_args, tags=["companion", "lakehouse", "data-product"]) as dag:
    ingest = PythonOperator(task_id="source_to_bronze", python_callable=ingestSources)
    quality = PythonOperator(task_id="great_expectations_quality", python_callable=validateQuality)
    lineage = PythonOperator(task_id="lineage_bronze_silver_gold", python_callable=logLakehouseLineage)
    ingest >> quality >> lineage
