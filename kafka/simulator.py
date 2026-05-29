import json
import os
import random
import time
from datetime import datetime, timezone
from uuid import uuid4
from kafka import KafkaProducer

TOPIC_BY_EVENT = {
    "user_registered": "user-events",
    "booking_created": "booking-events",
    "booking_cancelled": "booking-events",
    "message_sent": "chat-events",
    "review_added": "companion-events",
    "companion_online": "companion-events",
}
EVENTS = list(TOPIC_BY_EVENT)


def makeEvent(eventType: str) -> dict:
    return {
        "eventId": str(uuid4()),
        "eventType": eventType,
        "eventTime": datetime.now(timezone.utc).isoformat(),
        "payload": {
            "userId": f"usr-{random.randint(100, 999)}",
            "customerId": f"usr-{random.randint(200, 999)}",
            "companionId": f"cmp-{random.randint(1, 20):03d}",
            "bookingId": f"bkg-{random.randint(1, 10000):05d}",
            "rating": random.randint(1, 5),
            "responseTimeSeconds": random.randint(30, 600),
        },
    }


def main() -> None:
    producer = KafkaProducer(bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9093"), value_serializer=lambda value: json.dumps(value, ensure_ascii=False).encode("utf-8"))
    while True:
        eventType = random.choice(EVENTS)
        producer.send(TOPIC_BY_EVENT[eventType], makeEvent(eventType))
        producer.flush()
        time.sleep(float(os.getenv("EVENT_INTERVAL_SECONDS", "1")))


if __name__ == "__main__":
    main()
