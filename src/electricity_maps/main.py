from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
from .common.config import load_config
from .ingestion.api_client import ElectricityMapsClient
from .ingestion.bronze_writer import write_raw_payload
from .observability.logging import configure_logging


def run_api(cfg: dict) -> None:
    api = cfg["source"]
    key = os.getenv(api["api_key_env"])
    if not key:
        raise RuntimeError(f"Missing required API key environment variable: {api['api_key_env']}")
    client = ElectricityMapsClient(api["base_url"], key,
        timeout=api.get("timeout_seconds", 30), max_retries=api.get("max_retries", 4),
        backoff_seconds=api.get("backoff_seconds", 1.0))
    params = {"zone": api.get("zone", "FR"),
              "temporalGranularity": api.get("temporal_granularity", "hourly")}
    for dataset, endpoint in (("mix", "/electricity-mix/latest"), ("flows", "/electricity-flows/latest")):
        response = client.get(endpoint, params=params)
        print(write_raw_payload(response.payload, cfg["storage"]["bronze"], dataset, response.url))


def run_sample(cfg: dict) -> None:
    """Validate the Bronze contract without requiring a Spark installation."""
    root = Path(cfg["storage"]["bronze"])
    for dataset in ("mix", "flows"):
        files = sorted(Path("sample_data/bronze", dataset).glob("*.json"))
        if not files:
            raise FileNotFoundError(f"No sample Bronze payload for {dataset}")
        payload = json.loads(files[0].read_text(encoding="utf-8"))
        if not {"zone", "temporalGranularity", "data"}.issubset(payload):
            raise ValueError(f"Invalid sample payload for {dataset}")
        print(f"SAMPLE OK {dataset}: zone={payload['zone']} rows={len(payload['data'])} -> {root}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Electricity Maps FR enterprise ETL")
    parser.add_argument("--config", required=True)
    parser.add_argument("--mode", choices=("api", "sample"), default="api")
    args = parser.parse_args()
    configure_logging()
    cfg = load_config(args.config)
    (run_sample if args.mode == "sample" else run_api)(cfg)

if __name__ == "__main__":
    main()
