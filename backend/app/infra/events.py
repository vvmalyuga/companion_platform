import json
from datetime import datetime, timezone
from uuid import uuid4
from backend.app.core.config import settings
from backend.app.domain.models import EventEnvelope


class EventPublisher:
    def publish(self, eventType: str, payload: dict) -> EventEnvelope:
        event = EventEnvelope(eventId=str(uuid4()), eventType=eventType, eventTime=datetime.now(timezone.utc), payload=payload)
        # Kafka is disabled by default for local tests; Docker enables it via env when needed.
        if settings.enableKafka:
            from kafka import KafkaProducer
            producer = KafkaProducer(bootstrap_servers=settings.kafkaBootstrapServers, value_serializer=lambda v: json.dumps(v, default=str).encode("utf-8"))
            topic = "booking-events" if eventType.startswith("booking") else "user-events"
            producer.send(topic, event.model_dump(mode="json"))
            producer.flush()
        return event
