from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import pandas as pd, io, great_expectations as ge, requests

default_args = {
    'owner': 'data-eng',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'on_failure_callback': lambda ctx: requests.post(
        "https://api.telegram.org/bot<TOKEN>/sendMessage",
        json={"chat_id": "<CHAT_ID>", "text": f"DAG {ctx['dag_run'].dag_id} failed!"})
}

def fetch_companion_data():
    df = pd.DataFrame([
        {"booking_id": "b001", "companion_id": "C1", "customer_id": "U1", "event_date": "2026-05-29", "status": "completed", "rating": 5},
        {"booking_id": "b002", "companion_id": "C2", "customer_id": "U2", "event_date": "2026-05-29", "status": "cancelled", "rating": 0}
    ])
    buf = io.BytesIO()
    df.to_parquet(buf, index=False)
    buf.seek(0)
    hook = S3Hook(aws_conn_id='minio_conn')
    hook.load_file_obj(buf, key="raw/companion/bookings/{{ ds }}/data.parquet", bucket_name="companion-lake", replace=True)

def validate_data():
    df = pd.read_parquet("s3://companion-lake/raw/companion/bookings/{{ ds }}/data.parquet",
        storage_options={"key": "minioadmin", "secret": "minioadmin", "client_kwargs": {"endpoint_url": "http://minio:9000"}})
    ge_df = ge.from_pandas(df)
    ge_df.expect_column_values_to_not_be_null("booking_id")
    ge_df.expect_column_values_to_be_unique("booking_id")
    ge_df.expect_column_values_to_be_in_set("status", ["completed","cancelled","pending"])
    result = ge_df.validate()
    if not result["success"]:
        raise ValueError("Data quality checks failed")

with DAG('companion_ingestion', start_date=datetime(2026,5,29), schedule_interval='@hourly', catchup=False, default_args=default_args) as dag:
    PythonOperator(task_id='fetch_and_upload', python_callable=fetch_companion_data) >> \
    PythonOperator(task_id='validate_ge', python_callable=validate_data)
