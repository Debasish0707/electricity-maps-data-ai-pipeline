# NXP Senior Principal Data & AI Engineer — Electricity Maps ETL

## What this repository delivers

A production-oriented PySpark implementation of the NXP Electricity Maps assessment for France (`FR`). It follows the required Bronze → Silver → Gold architecture and implements **all three Gold products** rather than only the minimum one:

1. Daily Relative Electricity Mix
2. Daily Net Imports to France
3. Daily Net Exports from France

It also includes the requested high-level Data-to-LLM/RAG architecture, plus bonus engineering practices: retries, incremental/idempotent design, data quality, contracts, tests, CI/CD, security, observability and cloud deployment guidance.

## Assignment alignment

The source assignment requires raw Bronze data, typed/deduplicated Silver Delta + Parquet, business-ready Gold Delta + Parquet, and a high-level RAG-enabled chatbot architecture. The repository maps each requirement in `REQUIREMENT_TRACEABILITY.md`.

## Technology choice

**PySpark + Delta Lake + Parquet**. Databricks/Snowflake are intentionally not mandatory dependencies because the assessment permits PySpark and does not require either platform.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
cp .env.example .env
```

Set a valid sandbox key at runtime:

```bash
export ELECTRICITY_MAPS_API_KEY='YOUR_ROTATED_KEY'
```

Never commit `.env` or an API key.

## Run a dependency-light sample contract check

```bash
PYTHONPATH=src python -m electricity_maps.main --config config/test.yaml --mode sample
```

## Run the live API ingestion

```bash
PYTHONPATH=src python -m electricity_maps.main --config config/dev.yaml --mode api
```

This writes immutable Bronze envelopes. Silver and Gold transformations are implemented as Spark modules and are intended to run in a Spark environment with Delta support.

## Tests

```bash
pytest -q
ruff check src tests
bandit -q -r src
```

The local execution environment used to assemble this package did not contain PySpark/Delta binaries, so Spark integration tests should be executed by the included CI workflow or a Spark-enabled developer environment. No false claim of local Spark execution is made.

## Data layout

```text
Bronze: year=YYYY/month=MM/day=DD  <- ingestion timestamp
Silver: year=YYYY/month=MM/day=DD  <- data timestamp
Gold:   date/year/month            <- daily business products
```

## Silver schema

See `src/electricity_maps/silver/schemas.py` and `DATA_CONTRACTS.md`.

### Mix
`timestamp, updated_at, zone, energy_source, generation_mw, is_estimated, unit, ingestion_timestamp, source_url, request_id, payload_checksum, year, month, day`

### Flows
`timestamp, updated_at, zone, source_zone, destination_zone, flow_mw, is_estimated, unit, ingestion_timestamp, source_url, request_id, payload_checksum, year, month, day`

## Gold schema

### Daily relative mix
`date, zone_code, energy_source, generation_mwh, total_generation_mwh, generation_percentage, reference_timestamp, year, month`

### Daily imports
`date, source_zone, target_zone, net_import_mwh, reference_timestamp, year, month`

### Daily exports
`date, source_zone, destination_zone, net_export_mwh, reference_timestamp, year, month`

## AI/RAG

See `RAG_ARCHITECTURE.md`. Numerical questions use governed analytics over Gold; documentation questions use RAG; hybrid questions use both. The LLM is not the system of record.

## Reviewer navigation

Start with `ARCHITECTURE.md`, then `REQUIREMENT_TRACEABILITY.md`, `DATA_CONTRACTS.md`, `DATA_QUALITY.md`, `SECURITY.md`, `PERFORMANCE.md` and `RAG_ARCHITECTURE.md`.
