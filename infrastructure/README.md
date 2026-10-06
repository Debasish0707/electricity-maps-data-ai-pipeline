# Infrastructure Reference

A cloud deployment can use:

- Object storage (S3/ADLS/GCS) for Bronze/Silver/Gold
- Spark cluster/serverless Spark for transformation
- Delta Lake + catalog/metastore
- Managed secret manager/KMS
- IAM/RBAC
- Airflow/MWAA or equivalent orchestration
- Centralized logs/metrics/traces
- CI/CD with GitHub Actions

The assignment does not mandate a cloud provider, so these are deployment choices rather than hard-coded application dependencies.
