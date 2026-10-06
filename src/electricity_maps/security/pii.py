from __future__ import annotations
import hashlib

SENSITIVE_NAME_HINTS = {"email", "phone", "address", "ssn", "passport", "national_id"}


def classify_column(name: str) -> str:
    return "restricted" if name.lower() in SENSITIVE_NAME_HINTS else "internal"


def hash_identifier(value: str, salt: str) -> str:
    return hashlib.sha256(f"{salt}:{value}".encode()).hexdigest()


def detect_pii_columns(df) -> list[str]:
    return [c for c in df.columns if c.lower() in SENSITIVE_NAME_HINTS]


def mask_columns(df, columns: list[str]):
    from pyspark.sql import functions as F
    result = df
    for column in columns:
        result = result.withColumn(column, F.lit("***MASKED***"))
    return result
