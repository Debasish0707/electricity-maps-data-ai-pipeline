# Data-to-LLM and RAG Architecture

The assignment asks for a high-level design, not a production chatbot. The recommended design deliberately separates **analytics retrieval** from **document retrieval**.

## Query routing

1. Authenticate user and apply data entitlements.
2. Classify intent: numeric analytics, documentation/methodology, or hybrid.
3. Numeric analytics → controlled metrics/SQL tool over Gold.
4. Documentation → vector/hybrid retrieval over curated FAQs, API documentation and domain knowledge.
5. Hybrid → call both and provide citations/provenance.
6. LLM synthesizes only retrieved evidence.
7. Record prompt/model/retrieval/query metadata for audit.

## Why not pure vector RAG?

A vector database is not the source of truth for numerical aggregations. Asking a vector store for “France nuclear percentage last month” can retrieve context but should not calculate the metric. The Gold tables and a governed analytics tool should calculate it.

## Application components

- API gateway/authentication
- Conversational service
- Intent router
- SQL/metrics tool
- Retrieval service
- Reranker
- Prompt/policy layer
- LLM gateway
- Citation/provenance formatter
- Audit/observability service

## Infrastructure components

- Object storage + Delta Lake
- Catalog/metastore
- Spark compute
- Vector index for unstructured documentation
- Secret manager/KMS
- IAM/RBAC
- Monitoring/logging/tracing
- CI/CD

## Guardrails

Only allow approved Gold datasets and approved aggregate patterns. Reject DDL/DML, cross-tenant access and arbitrary table access. Enforce timeouts and result limits. If evidence is insufficient, the assistant must say so rather than inventing a value.
