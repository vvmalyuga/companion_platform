from datetime import datetime, timezone
from feast import FeatureStore

store = FeatureStore(repo_path="feature_repo")
store.materialize_incremental(datetime.now(timezone.utc))
features = store.get_online_features(features=["user_features:total_bookings", "companion_features:avg_rating"], entity_rows=[{"customer_id": "usr-201", "companion_id": "cmp-001"}]).to_dict()
print(features)
