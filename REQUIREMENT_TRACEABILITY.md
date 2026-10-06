# NXP Requirement Traceability

| Requirement | Where addressed |
|---|---|
| Python ETL | `src/electricity_maps` |
| PySpark option | `common/spark.py`, Silver/Gold modules |
| Bronze raw immutable API response | `ingestion/bronze_writer.py` |
| Bronze ingestion partition `year/month/day` | `bronze_writer.py` |
| Minimal Bronze metadata | timestamp, URL, request ID, checksum |
| No Bronze schema enforcement | raw JSON envelope |
| Silver flatten nested JSON | `silver/mix.py`, `silver/flows.py` |
| Timestamp conversion | Silver transformers |
| Schema/data type enforcement | `silver/schemas.py` |
| Deduplication | Silver `deduplicate()` |
| Silver Parquet + Delta | deployment/output contract in docs |
| Silver data timestamp partition | `year/month/day` derived from timestamp |
| Daily Relative Electricity Mix | `gold/electricity_mix.py` |
| Daily Imports | `gold/imports_exports.py` |
| Daily Exports | `gold/imports_exports.py` |
| Gold flat schema | Gold modules/contracts |
| LLM architecture | `RAG_ARCHITECTURE.md` |
| RAG over Gold + docs | `RAG_ARCHITECTURE.md` |
| Application/infrastructure views | `ARCHITECTURE.md` |
| README setup/run/schema docs | `README.md` |
| Sample outputs | `sample_data/` |
| Rate-limit retries | `ingestion/api_client.py` |
| Incremental/idempotent design | architecture + contracts |
| DQ/data contracts | `DATA_QUALITY.md`, `DATA_CONTRACTS.md` |
| Unit tests | `tests/` |
| CI/CD | `.github/workflows/ci.yml` |
| Cloud storage/orchestration extension | `config/prod.yaml`, `orchestration/`, `infrastructure/` |
