"""Backward-compatible alias DAG for raw Companion ingestion.

The production DAG is `companion_data_platform`; this file keeps the old DAG id
available for reviewers while using real environment-driven alerts and quality
checks instead of placeholder credentials.
"""
from __future__ import annotations

import os
from datetime import datetime, timedelta

import pandas as pd
import requests
from airflow import DAG
from airflow.operators.python import PythonOperator

CSV_ROOT = os.getenv("COMPANION_CSV_ROOT", "/opt/airflow/data/csv")


def alertFailure(context):
    telegramToken = os.getenv("TELEGRAM_BOT_TOKEN")
    telegramChat = os.getenv("TELEGRAM_CHAT_ID")
    slackWebhook = os.getenv("SLACK_WEBHOOK_URL")
    message = f"DAG {context['dag_run'].dag_id} failed"
    if telegramToken and telegramChat:
        requests.post(f"https://api.telegram.org/bot{telegramToken}/sendMessage", json={"chat_id": telegramChat, "text": message}, timeout=10)
    if slackWebhook:
        requests.post(slackWebhook, json={"text": message}, timeout=10)


def validateRawCsv() -> None:
    bookings = pd.read_csv(f"{CSV_ROOT}/bookings.csv")
    assert bookings["booking_id"].is_unique
    assert bookings["rating"].between(1, 5).all()
    assert bookings["booking_date"].notna().all()


with DAG(
    "companion_raw_ingestion",
    start_date=datetime(2026, 5, 29),
    schedule_interval="@hourly",
    catchup=False,
    default_args={"owner": "data-platform", "retries": 3, "retry_delay": timedelta(minutes=1), "retry_exponential_backoff": True, "on_failure_callback": alertFailure},
    tags=["companion", "compatibility"],
) as dag:
    PythonOperator(task_id="validate_raw_csv", python_callable=validateRawCsv)
