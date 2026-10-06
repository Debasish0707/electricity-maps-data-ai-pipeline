from __future__ import annotations
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path

@dataclass
class RunAudit:
    run_id: str
    zone: str
    started_at: str
    status: str
    bronze_rows: int = 0
    silver_rows: int = 0
    gold_rows: int = 0
    dq_status: str = "NOT_RUN"
    error_class: str | None = None


def write_audit(audit: RunAudit, root: str) -> str:
    p = Path(root); p.mkdir(parents=True, exist_ok=True)
    out = p / f"{audit.run_id}.json"
    out.write_text(json.dumps(asdict(audit), indent=2), encoding="utf-8")
    return str(out)
