from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def build_daily_flows(silver_flows: DataFrame, interval_hours: float = 1.0) -> DataFrame:
    return (silver_flows.withColumn("date", F.to_date("timestamp"))
        .withColumn("flow_mwh", F.col("flow_mw") * F.lit(interval_hours))
        .groupBy("date", "source_zone", "destination_zone")
        .agg(F.sum("flow_mwh").alias("net_mwh"), F.max("timestamp").alias("reference_timestamp"))
        .withColumn("year", F.year("date")).withColumn("month", F.month("date")))


def build_imports(daily_flows: DataFrame, france_zone: str = "FR") -> DataFrame:
    return (daily_flows.filter(F.col("destination_zone") == france_zone)
        .select("date", F.col("source_zone").alias("source_zone"),
                F.col("destination_zone").alias("target_zone"),
                F.col("net_mwh").alias("net_import_mwh"), "reference_timestamp", "year", "month"))


def build_exports(daily_flows: DataFrame, france_zone: str = "FR") -> DataFrame:
    return (daily_flows.filter(F.col("source_zone") == france_zone)
        .select("date", "source_zone", "destination_zone",
                F.col("net_mwh").alias("net_export_mwh"), "reference_timestamp", "year", "month"))
