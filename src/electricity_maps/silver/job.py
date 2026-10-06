from __future__ import annotations
from pyspark.sql import SparkSession
from .mix import flatten_mix, deduplicate as dedup_mix
from .flows import flatten_flows, finalize_flows, deduplicate as dedup_flows


def read_bronze(spark: SparkSession, path: str):
    return spark.read.json(path)


def transform_mix(spark: SparkSession, bronze_path: str):
    return dedup_mix(flatten_mix(read_bronze(spark, bronze_path)))


def transform_flows(spark: SparkSession, bronze_path: str, positive_direction: str = "inbound"):
    return dedup_flows(finalize_flows(flatten_flows(read_bronze(spark, bronze_path), positive_direction)))


def write_delta_and_parquet(df, delta_path: str, parquet_path: str):
    (df.write.format("delta").mode("append").partitionBy("year", "month", "day").save(delta_path))
    (df.write.format("parquet").mode("append").partitionBy("year", "month", "day").save(parquet_path))
