# Data Quality

## Structural
- Required fields present.
- Schema and data types match the contract.
- No malformed timestamps.
- No null business keys.

## Completeness and freshness
- Expected hourly observations are compared with observed observations.
- Latest successful source timestamp is compared with the configured SLA.
- Missing intervals are surfaced rather than silently filled.

## Integrity
- Mix generation must be non-negative unless the source contract explicitly documents otherwise.
- Daily relative mix should sum to approximately 100%, within configured tolerance.
- Flow source and destination must differ.
- France imports have `destination_zone = FR`.
- France exports have `source_zone = FR`.

## Duplicate detection

Silver deduplicates using deterministic business keys and latest-ingestion ordering.

## Anomaly detection

Production deployments should add rolling mean/stddev or robust median/MAD checks per energy source and interconnector. Anomalies are quarantined/flagged; they are not silently deleted.

## Data-quality disposition

`PASS`, `WARN`, `QUARANTINE`, `FAIL`. Contract failures stop publication of downstream Gold data; non-blocking anomalies remain observable.
