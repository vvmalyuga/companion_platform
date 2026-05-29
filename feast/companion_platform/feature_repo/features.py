from datetime import timedelta
from feast import Entity, FeatureView, Field, FileSource
from feast.types import Float32, Int64, String

user = Entity(name="customer_id", join_keys=["customer_id"])
companion = Entity(name="companion_id", join_keys=["companion_id"])

userSource = FileSource(path="data/user_features.parquet", timestamp_field="event_timestamp")
companionSource = FileSource(path="data/companion_features.parquet", timestamp_field="event_timestamp")

user_features = FeatureView(
    name="user_features",
    entities=[user],
    ttl=timedelta(days=30),
    schema=[Field(name="total_bookings", dtype=Int64), Field(name="avg_session_duration", dtype=Float32), Field(name="avg_rating_given", dtype=Float32), Field(name="preferred_categories", dtype=String), Field(name="active_days", dtype=Int64)],
    online=True,
    source=userSource,
)

companion_features = FeatureView(
    name="companion_features",
    entities=[companion],
    ttl=timedelta(days=30),
    schema=[Field(name="avg_rating", dtype=Float32), Field(name="response_time", dtype=Float32), Field(name="booking_frequency", dtype=Int64), Field(name="cancellation_rate", dtype=Float32)],
    online=True,
    source=companionSource,
)
