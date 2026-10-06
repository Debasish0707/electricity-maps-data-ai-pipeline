# Operations Runbook

## Failure classes

- API 4xx: fail fast except configured transient codes.
- API 429/5xx/timeouts: retry with bounded exponential backoff and jitter.
- Malformed payload: quarantine the response envelope and raise an ingestion alert.
- Silver DQ failure: stop Gold publication for affected partitions.
- Gold failure: preserve Silver and retry affected dates only.

## Audit

Every run should record run ID, zone, endpoint, start/end time, status, source response count, Bronze checksum, Silver rows, Gold rows, DQ status and error class.

## Replay

Replay from Bronze whenever possible. This prevents repeated API consumption and makes incident recovery deterministic.

## Deployment gates

Lint → unit tests → contract tests → security scan → build → integration tests → deployment. Production promotion requires passing DQ and security gates.
