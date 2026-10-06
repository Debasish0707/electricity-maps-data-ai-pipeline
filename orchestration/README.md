# Orchestration

Recommended production schedule: hourly ingestion → Bronze → Silver → affected-date Gold.

The DAG should:

1. Generate run ID.
2. Read last successful watermark.
3. Request only required source interval.
4. Persist Bronze.
5. Validate Bronze contract.
6. Transform Silver.
7. Run DQ.
8. Publish affected Gold dates transactionally.
9. Persist audit metrics and watermark.

Any orchestrator may implement this boundary: Airflow/MWAA, Dagster, Prefect, managed cloud workflow services, or a CI-triggered scheduler.
