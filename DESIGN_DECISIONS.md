# Design Decisions

1. **PySpark** was selected because it is explicitly permitted and provides a credible enterprise-scale transformation engine.
2. **Delta Lake + Parquet** are the Silver/Gold persistence contract required by the assignment.
3. **Cloud-neutral core** avoids making Databricks, Snowflake or a specific cloud mandatory where the assignment does not require one.
4. **Bronze immutability** protects source fidelity and enables replay without source re-ingestion.
5. **Deterministic keys** make Silver idempotent and deduplicatable.
6. **Explicit flow direction configuration** avoids silently assuming the sign convention of a source payload.
7. **Hourly interval configuration** makes MW→MWh conversion explicit rather than hiding a unit assumption in aggregation code.
8. **Analytics-first AI routing** ensures numerical answers come from governed Gold calculations, while RAG is used for semantic/documentation knowledge.
9. **Security-by-default** keeps credentials outside source control and makes AI access read-only.
