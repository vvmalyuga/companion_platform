import json
import logging
from datetime import datetime, timezone
from pathlib import Path


class LineageLogger:
    def __init__(self, path: str = "/opt/airflow/logs/lineage/lineage.jsonl") -> None:
        self.path = Path(path)

    def emit(self, source: str, target: str, dataset: str, runId: str) -> None:
        event = {"eventTime": datetime.now(timezone.utc).isoformat(), "source": source, "target": target, "dataset": dataset, "runId": runId}
        logging.info("lineage=%s", event)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False) + "\n")
