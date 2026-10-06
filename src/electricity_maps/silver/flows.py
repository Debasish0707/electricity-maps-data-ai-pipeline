from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F


def flatten_flows(raw: DataFrame, positive_direction: str = "inbound") -> DataFrame:
    """Normalize signed interconnector values. Direction is explicit in config."""
    p = F.col("payload")
    exploded = (raw
        .withColumn("timestamp", F.to_timestamp(p["datetime"]))
        .withColumn("updated_at", F.to_timestamp(p["updatedAt"]))
        .withColumn("zone", p["zone"])
        .withColumn("unit", p["unit"])
        .withColumn("is_estimated", p["isEstimated"])
        .withColumn("flow_point", F.explode(F.map_entries(p["flows"])))
        .select("timestamp", "updated_at", "zone", "unit", "is_estimated",
                F.col("flow_point.key").alias("counterparty_zone"),
                F.col("flow_point.value").cast("double").alias("signed_flow_mw"),
                "ingestion_timestamp", "source_url", "request_id", "payload_checksum")
    )
    if positive_direction == "inbound":
        # Positive signed value means counterparty -> France.
        return (exploded
            .withColumn("source_zone", F.when(F.col("signed_flow_mw") >= 0, F.col("counterparty_zone")).otherwise(F.col("zone")))
            .withColumn("destination_zone", F.when(F.col("signed_flow_mw") >= 0, F.col("zone")).otherwise(F.col("counterparty_zone")))
            .withColumn("flow_mw", F.abs("signed_flow_mw")))
    return (exploded
        .withColumn("source_zone", F.when(F.col("signed_flow_mw") >= 0, F.col("zone")).otherwise(F.col("counterparty_zone")))
        .withColumn("destination_zone", F.when(F.col("signed_flow_mw") >= 0, F.col("counterparty_zone")).otherwise(F.col("zone")))
        .withColumn("flow_mw", F.abs("signed_flow_mw")))


def finalize_flows(df: DataFrame) -> DataFrame:
    return (df.withColumn("year", F.year("timestamp"))
        .withColumn("month", F.month("timestamp"))
        .withColumn("day", F.dayofmonth("timestamp"))
        .withColumn("record_key", F.sha2(F.concat_ws("||", "timestamp", "source_zone", "destination_zone"), 256)))


def deduplicate(df: DataFrame) -> DataFrame:
    w = Window.partitionBy("record_key").orderBy(F.col("ingestion_timestamp").desc(), F.col("updated_at").desc_nulls_last())
    return df.withColumn("_rn", F.row_number().over(w)).filter("_rn = 1").drop("_rn")
