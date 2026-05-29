from datetime import datetime, timezone
from pathlib import Path

try:
    import pandas as pd
except ImportError as exc:
    raise SystemExit("pandas/pyarrow are required: pip install pandas pyarrow") from exc

root = Path("feast/companion_platform/feature_repo/data")
root.mkdir(parents=True, exist_ok=True)
now = datetime.now(timezone.utc)
pd.DataFrame([
    {"customer_id": "usr-201", "event_timestamp": now, "total_bookings": 4, "avg_session_duration": 85.0, "avg_rating_given": 4.8, "preferred_categories": "прогулки|музеи", "active_days": 3},
    {"customer_id": "usr-202", "event_timestamp": now, "total_bookings": 2, "avg_session_duration": 45.0, "avg_rating_given": 4.3, "preferred_categories": "спорт", "active_days": 2},
]).to_parquet(root / "user_features.parquet", index=False)
pd.DataFrame([
    {"companion_id": "cmp-001", "event_timestamp": now, "avg_rating": 4.9, "response_time": 120.0, "booking_frequency": 42, "cancellation_rate": 0.03},
    {"companion_id": "cmp-002", "event_timestamp": now, "avg_rating": 4.7, "response_time": 240.0, "booking_frequency": 27, "cancellation_rate": 0.07},
]).to_parquet(root / "companion_features.parquet", index=False)
print(f"Generated Feast samples in {root}")
