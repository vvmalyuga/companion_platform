from kafka import KafkaProducer
import json, time, random
producer = KafkaProducer(bootstrap_servers='localhost:9093', value_serializer=lambda v: json.dumps(v).encode())
companions = [f"C{i}" for i in range(1, 50)]
while True:
    evt = {
        "event_id": f"evt-{int(time.time()*1000)}",
        "companion_id": random.choice(companions),
        "event_type": random.choice(["booking_created","booking_completed","profile_view"]),
        "event_time": int(time.time()*1000)
    }
    producer.send("events", evt)
    time.sleep(0.2)
