# Performance and Scalability

## Spark

Enable AQE, adaptive partition coalescing and skew handling. Use predicate pushdown and partition pruning on `year/month/day`. Avoid `SELECT *`, `collect()` and `toPandas()` in production paths. Broadcast only genuinely small dimensions.

## Delta/Parquet

Write appropriately sized files, avoid tiny-file explosions, and use compaction/OPTIMIZE where the target runtime supports it. Keep Bronze append-only. Silver and Gold use partition-aware incremental writes.

## API

Use bounded retries, exponential backoff and jitter. Prefer source-supported time windows rather than repeatedly downloading overlapping history. Persist response checksums for replay/idempotency.

## Incremental Gold

Determine affected dates from newly processed Silver records and recompute only those dates. This prevents a full historical scan for each hourly ingestion.

## Scale-out

The design scales horizontally because transformation state is persisted in Delta/object storage and Spark handles distributed processing. The assessment's France dataset is small enough for modest compute; the architecture is intentionally reusable for broader zones/history.
