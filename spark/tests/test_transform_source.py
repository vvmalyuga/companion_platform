from pathlib import Path


def testSparkJobsDeclareRequiredFeatureOutputs():
    source = Path("spark/jobs/silver_to_gold.py").read_text(encoding="utf-8")
    assert "user_features" in source
    assert "companion_features" in source
    assert "booking_conversion" in source
