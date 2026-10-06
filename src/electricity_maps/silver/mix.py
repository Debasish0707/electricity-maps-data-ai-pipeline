from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F


def flatten_mix(raw: DataFrame) -> DataFrame:
    """Normalize an hourly mix response into one row per timestamp/source."""
    payload = F.col("payload")
    base = (raw
        .withColumn("timestamp", F.to_timestamp(payload["datetime"]))
        .withColumn("updated_at", F.to_timestamp(payload["updatedAt"]))
        .withColumn("zone", F.col("payload.zone"))
        .withColumn("unit", F.col("payload.unit"))
        .withColumn("is_estimated", F.col("payload.isEstimated"))
    )
    # API payloads may expose the mix as a map; explode keeps the implementation extensible.
    return (base
        .withColumn("point", F.explode(F.map_entries(F.col("payload.mix"))))
        .select("timestamp", "updated_at", "zone", "unit", "is_estimated",
                F.col("point.key").alias("energy_source"),
                F.col("point.value").cast("double").alias("generation_mw"),
                "ingestion_timestamp", "source_url", "request_id", "payload_checksum")
        .withColumn("year", F.year("timestamp"))
        .withColumn("month", F.month("timestamp"))
        .withColumn("day", F.dayofmonth("timestamp"))
        .withColumn("record_key", F.sha2(F.concat_ws("||", "timestamp", "zone", "energy_source"), 256))
    )


def deduplicate(df: DataFrame) -> DataFrame:
    w = Window.partitionBy("record_key").orderBy(F.col("ingestion_timestamp").desc(), F.col("updated_at").desc_nulls_last())
    return df.withColumn("_rn", F.row_number().over(w)).filter("_rn = 1").drop("_rn")
