import json
import os
import urllib.parse
import urllib.request
from datetime import datetime
from pyflink.common import Duration, Types
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaOffsetsInitializer, KafkaSource
from pyflink.datastream.functions import SinkFunction
from pyflink.datastream.window import SlidingProcessingTimeWindows


class ClickHouseWindowSink(SinkFunction):
    def invoke(self, value, context):
        eventTime = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        activeUsers = int(value[1])
        bookings = int(value[2])
        onlineCompanions = int(value[3])
        sql = "INSERT INTO companion.gold_business_metrics VALUES ('{}','realtime','all',{},{},0,0,{},'stream','completed')".format(eventTime[:10], activeUsers, bookings, onlineCompanions)
        url = os.getenv("CLICKHOUSE_URL", "http://clickhouse:8123") + "?" + urllib.parse.urlencode({"query": sql})
        request = urllib.request.Request(url, method="POST")
        urllib.request.urlopen(request, timeout=10).read()


def parseEvent(raw: str) -> tuple[str, int, int, int]:
    event = json.loads(raw)
    eventType = event.get("eventType")
    payload = event.get("payload", {})
    activeUser = 1 if eventType in {"user_registered", "message_sent", "booking_created"} else 0
    booking = 1 if eventType == "booking_created" else 0
    online = 1 if eventType == "companion_online" else 0
    response = 1 if int(payload.get("responseTimeSeconds", 0)) > 0 else 0
    return (eventType, activeUser, booking, online + response)


def main() -> None:
    env = StreamExecutionEnvironment.get_execution_environment()
    source = KafkaSource.builder().set_bootstrap_servers(os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")).set_topics("booking-events", "user-events", "chat-events", "companion-events").set_group_id("companion-flink").set_starting_offsets(KafkaOffsetsInitializer.latest()).set_value_only_deserializer(SimpleStringSchema()).build()
    stream = env.from_source(source, watermark_strategy=None, source_name="companion-kafka")
    metrics = stream.map(parseEvent, output_type=Types.TUPLE([Types.STRING(), Types.INT(), Types.INT(), Types.INT()])).window_all(SlidingProcessingTimeWindows.of(Duration.minutes(5), Duration.minutes(1))).reduce(lambda left, right: ("window", left[1] + right[1], left[2] + right[2], left[3] + right[3]))
    metrics.add_sink(ClickHouseWindowSink())
    metrics.print()
    env.execute("companion-realtime-aggregation")


if __name__ == "__main__":
    main()
