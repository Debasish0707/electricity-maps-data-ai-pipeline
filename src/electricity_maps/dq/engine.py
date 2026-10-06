from dataclasses import dataclass
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

@dataclass(frozen=True)
class CheckResult:
    name: str
    passed: bool
    observed: int
    detail: str = ""


def null_check(df: DataFrame, column: str) -> CheckResult:
    n = df.filter(F.col(column).isNull()).limit(1).count()
    return CheckResult(f"not_null:{column}", n == 0, n, "null rows" if n else "ok")


def duplicate_key_check(df: DataFrame, key: str) -> CheckResult:
    n = df.groupBy(key).count().filter(F.col("count") > 1).limit(1).count()
    return CheckResult(f"unique:{key}", n == 0, n, "duplicate keys" if n else "ok")
