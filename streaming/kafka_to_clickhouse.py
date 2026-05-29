import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from kafka import KafkaConsumer
import requests

TOPICS = ["booking-events", "user-events", "chat-events", "companion-events"]
CLICKHOUSE_URL = os.getenv("CLICKHOUSE_URL", "http://clickhouse:8123")
CLICKHOUSE_AUTH = (os.getenv("CLICKHOUSE_USER", "default"), os.getenv("CLICKHOUSE_PASSWORD", "clickhouse"))
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='{"timestamp":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","message":"%(message)s"}')
logger = logging.getLogger("companion.kafka_to_clickhouse")


def chInsert(sql: str) -> None:
    response = requests.post(CLICKHOUSE_URL, params={"query": sql}, auth=CLICKHOUSE_AUTH, timeout=10)
    response.raise_for_status()


def quote(value: object) -> str:
    return str(value or "").replace("'", "''")


def handle(event: dict) -> None:
    eventType = event.get("eventType", "unknown")
    payload = event.get("payload", {})
    eventTime = event.get("eventTime", datetime.now(timezone.utc).isoformat()).replace("T", " ").replace("Z", "")[:19]
    if eventType.startswith("booking"):
        chInsert("INSERT INTO companion.realtime_bookings VALUES ('{}','{}','{}','{}','{}',{})".format(eventTime, quote(payload.get("bookingId")), quote(payload.get("companionId")), quote(payload.get("customerId")), quote(payload.get("status", eventType)), float(payload.get("amount", 0))))
    if eventType in {"user_registered", "message_sent", "booking_created"}:
        chInsert("INSERT INTO companion.realtime_activity VALUES ('{}','{}','{}','{}')".format(eventTime, quote(eventType), quote(payload.get("userId") or payload.get("customerId") or payload.get("senderId")), quote(payload.get("city", "unknown"))))
    if eventType in {"companion_online", "review_added", "message_sent"}:
        chInsert("INSERT INTO companion.realtime_companion_stats VALUES ('{}','{}',{},{},{})".format(eventTime, quote(payload.get("companionId") or payload.get("receiverId")), 1 if eventType == "companion_online" else 0, int(payload.get("responseTimeSeconds", 0)), float(payload.get("rating", 0))))
    logger.info("processed_event eventType=%s", eventType)


def waitForClickHouse() -> None:
    for _ in range(60):
        try:
            requests.get(f"{CLICKHOUSE_URL}/ping", auth=CLICKHOUSE_AUTH, timeout=2).raise_for_status()
            logger.info("clickhouse_ready url=%s", CLICKHOUSE_URL)
            return
        except Exception:
            time.sleep(2)
    raise RuntimeError("ClickHouse is not available")


def main() -> None:
    waitForClickHouse()
    consumer = KafkaConsumer(*TOPICS, bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"), group_id="companion-clickhouse-sink", auto_offset_reset="latest", value_deserializer=lambda raw: json.loads(raw.decode("utf-8")))
    logger.info("consumer_started topics=%s", ",".join(TOPICS))
    for message in consumer:
        handle(message.value)


if __name__ == "__main__":
    main()
