from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def mix_percentage_check(gold: DataFrame, tolerance: float = 0.5) -> DataFrame:
    return (gold.groupBy("date", "zone_code").agg(F.sum("generation_percentage").alias("pct_sum"))
        .withColumn("passed", F.abs(F.col("pct_sum") - 100.0) <= F.lit(tolerance)))


def non_negative_generation_check(silver: DataFrame) -> DataFrame:
    return silver.select(F.col("generation_mw") >= 0.0).withColumnRenamed("(generation_mw >= 0.0)", "passed")


def flow_integrity_check(silver: DataFrame) -> DataFrame:
    return silver.select((F.col("source_zone") != F.col("destination_zone")).alias("passed"))
