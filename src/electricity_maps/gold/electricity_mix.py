from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def build_daily_mix(silver_mix: DataFrame, interval_hours: float = 1.0) -> DataFrame:
    hourly = (silver_mix.withColumn("date", F.to_date("timestamp"))
        .withColumn("generation_mwh", F.col("generation_mw") * F.lit(interval_hours)))
    daily = hourly.groupBy("date", "zone", "energy_source").agg(
        F.sum("generation_mwh").alias("generation_mwh"),
        F.max("timestamp").alias("reference_timestamp"))
    total = daily.groupBy("date", "zone").agg(F.sum("generation_mwh").alias("total_generation_mwh"))
    return (daily.join(total, ["date", "zone"], "left")
        .withColumn("generation_percentage", F.when(F.col("total_generation_mwh") > 0,
            F.col("generation_mwh") / F.col("total_generation_mwh") * 100.0).otherwise(F.lit(0.0)))
        .withColumnRenamed("zone", "zone_code")
        .withColumn("year", F.year("date"))
        .withColumn("month", F.month("date")))
