from __future__ import annotations
from .electricity_mix import build_daily_mix
from .imports_exports import build_daily_flows, build_imports, build_exports


def build_products(silver_mix, silver_flows, interval_hours: float = 1.0, france_zone: str = "FR"):
    mix = build_daily_mix(silver_mix, interval_hours)
    flows = build_daily_flows(silver_flows, interval_hours)
    return mix, build_imports(flows, france_zone), build_exports(flows, france_zone)


def write_gold(df, delta_path: str, parquet_path: str):
    (df.write.format("delta").mode("overwrite").partitionBy("year", "month").save(delta_path))
    (df.write.format("parquet").mode("overwrite").partitionBy("year", "month").save(parquet_path))
