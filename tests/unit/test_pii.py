import pytest
pytest.importorskip("pyspark")
from pyspark.sql import SparkSession
from electricity_maps.security.pii import detect_pii_columns, mask_columns

def test_pii_detection_and_masking():
    spark = SparkSession.builder.master("local[2]").appName("test").getOrCreate()
    df = spark.createDataFrame([("alice@example.com", "FR")], ["email", "zone"])
    assert "email" in detect_pii_columns(df)
    masked = mask_columns(df, ["email"]).collect()[0]["email"]
    assert masked == "***MASKED***"
    spark.stop()
