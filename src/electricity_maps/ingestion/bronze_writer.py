from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
from ..common.hash import stable_hash


def write_raw_payload(payload: dict, root: str, dataset: str, source_url: str) -> str:
    """Persist an immutable envelope; payload itself is never transformed."""
    now = datetime.now(timezone.utc)
    partition = Path(root) / dataset / f"year={now:%Y}" / f"month={now:%m}" / f"day={now:%d}"
    partition.mkdir(parents=True, exist_ok=True)
    request_id = str(uuid4())
    envelope = {
        "payload": payload,
        "ingestion_timestamp": now.isoformat(),
        "source_url": source_url,
        "request_id": request_id,
        "payload_checksum": stable_hash(payload),
    }
    path = partition / f"{request_id}.json"
    path.write_text(json.dumps(envelope, separators=(",", ":")), encoding="utf-8")
    return str(path)
