# Security

- API credentials are runtime secrets only; never commit them.
- Use a managed secret store in cloud deployment.
- Encrypt data in transit and at rest.
- Apply least-privilege IAM/RBAC.
- Bronze is immutable and write-restricted; Silver/Gold are published by controlled service identities.
- AI access is read-only against curated Gold views.
- AI-generated SQL is never executed directly: use an allow-list of datasets/columns, SELECT-only validation, query timeout, row/scan limits and audit logging.
- The assignment data is expected to be operational electricity data, not a PII dataset. The framework nevertheless supports classification and deterministic hashing of sensitive identifiers if future datasets introduce them.
- Logs must never contain API keys or raw authorization headers.
