from feast import Entity, Field, FeatureView, FileSource
from feast.value_type import ValueType
from feast.types import Float32, Int64, String

companion = Entity(name="companion_id", value_type=ValueType.STRING)

source = FileSource(
    path="/home/vvmalyuga/companion-dataplatform/feast/companion_performance/feature_repo/data/companion_features.parquet",
    timestamp_field="event_timestamp",
)

companion_features_view = FeatureView(
    name="companion_features",
    entities=[companion],
    ttl=None,
    schema=[
        Field(name="total_bookings", dtype=Int64),
        Field(name="avg_rating", dtype=Float32),
        Field(name="completion_rate", dtype=Float32),
        Field(name="response_time_min", dtype=Float32),
    ],
    source=source,
    online=True,
)
