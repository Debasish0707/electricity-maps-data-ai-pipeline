# Solution Architecture

## Objective

Build a reusable PySpark ETL pipeline for France (`FR`) electricity mix and inter-zone flows using the required Bronze → Silver → Gold architecture. The assignment explicitly permits PySpark and requires Silver/Gold in Parquet + Delta Lake and Bronze/Silver partitioning by `year=YYYY/month=MM/day=DD`. See the NXP assignment for the authoritative requirements.

## Application view

```text
Electricity Maps API
       |
       v
[Ingestion Client] -- retry/timeout/rate-limit --> [Bronze immutable]
                                                     |
                                                     v
                                            [Silver normalization]
                                                     |
                                  +------------------+------------------+
                                  |                                     |
                                  v                                     v
                         [Gold Daily Mix]                 [Gold Imports/Exports]
                                  |                                     |
                                  +------------------+------------------+
                                                     |
                                                     v
                                      [Analytics / AI Data Agent]
                                          /                  \
                                  SQL metrics                RAG
                                  over Gold           docs/FAQs/methodology
                                          \                  /
                                           +------ LLM ------+
```

## Infrastructure view

Local execution is supported for assessment reproducibility. The same code can run on a managed Spark service with object storage. Production deployment should use an object store such as S3/ADLS/GCS, an orchestration service, secret manager, IAM/RBAC, centralized logs/metrics, and a Delta-compatible metastore/catalog.

Databricks and Snowflake are deliberately not mandatory because they are not specified by the assignment. They can be deployment options, not application contracts.

## Medallion contracts

### Bronze
Raw API response exactly as received, wrapped only with ingestion metadata: ingestion timestamp, source URL, request ID and checksum. Partition by ingestion date.

### Silver
One row per timestamp/source for mix and one row per timestamp/source/destination for flows. Strong types, flattened JSON, deterministic business keys, deduplication and data-timestamp partitioning.

### Gold
Flat daily products. Mix expresses source contribution percentages. Flow products express daily MWh for France imports and exports.

## Incremental and idempotent strategy

Bronze is append-only. A control/checkpoint store records source, zone, endpoint, requested interval, response checksum, run ID and processing status. Silver uses deterministic keys and keeps the latest valid ingestion. Gold recomputes only affected dates, allowing safe replay after failures.

## Failure isolation

API failures do not corrupt existing Bronze. Silver/Gold jobs consume persisted Bronze, so transformations can be replayed without repeatedly calling the source API. Failed records can be quarantined with reason codes.
