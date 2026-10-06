from pyspark.sql import SparkSession


def create_spark(app_name: str = "electricity-maps-etl") -> SparkSession:
    return (
        SparkSession.builder.appName(app_name)
        .config("spark.sql.adaptive.enabled", "true")
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
        .config("spark.sql.adaptive.skewJoin.enabled", "true")
        .config("spark.sql.parquet.filterPushdown", "true")
        .config("spark.sql.files.maxPartitionBytes", 134217728)
        .getOrCreate()
    )
