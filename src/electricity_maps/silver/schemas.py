from pyspark.sql.types import StructType, StructField, StringType, DoubleType, BooleanType, TimestampType, IntegerType

MIX_SCHEMA = StructType([
    StructField("timestamp", TimestampType(), False),
    StructField("updated_at", TimestampType(), True),
    StructField("zone", StringType(), False),
    StructField("energy_source", StringType(), False),
    StructField("generation_mw", DoubleType(), True),
    StructField("is_estimated", BooleanType(), True),
    StructField("unit", StringType(), True),
    StructField("ingestion_timestamp", TimestampType(), False),
    StructField("source_url", StringType(), False),
    StructField("request_id", StringType(), False),
    StructField("payload_checksum", StringType(), False),
    StructField("year", IntegerType(), False),
    StructField("month", IntegerType(), False),
    StructField("day", IntegerType(), False),
])

FLOW_SCHEMA = StructType([
    StructField("timestamp", TimestampType(), False),
    StructField("updated_at", TimestampType(), True),
    StructField("zone", StringType(), False),
    StructField("source_zone", StringType(), True),
    StructField("destination_zone", StringType(), True),
    StructField("flow_mw", DoubleType(), True),
    StructField("is_estimated", BooleanType(), True),
    StructField("unit", StringType(), True),
    StructField("ingestion_timestamp", TimestampType(), False),
    StructField("source_url", StringType(), False),
    StructField("request_id", StringType(), False),
    StructField("payload_checksum", StringType(), False),
    StructField("year", IntegerType(), False),
    StructField("month", IntegerType(), False),
    StructField("day", IntegerType(), False),
])
