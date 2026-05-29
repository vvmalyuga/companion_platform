#!/usr/bin/env bash
set -euo pipefail
curl -fsS http://localhost:4000/readyz >/dev/null
curl -fsS -H 'Authorization: secret' 'http://localhost:4000/cubejs-api/v1/load?query={"measures":["CompanionActivity.BookingCount"],"timeDimensions":[],"dimensions":["CompanionActivity.category"]}' >/dev/null
curl -fsS 'http://localhost:8123/?query=SELECT%20count()%20FROM%20companion.gold_business_metrics' >/dev/null
