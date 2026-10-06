# Sample Outputs

The Bronze examples show the required immutable envelope and `year/month/day` ingestion partition. The Gold examples are human-readable JSON representations of the expected flat products. The production Spark job writes the authoritative Silver/Gold outputs as Parquet and Delta Lake; binary Parquet/Delta artifacts are intentionally not fabricated in source control.
