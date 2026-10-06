from pyspark.sql import DataFrame

def select_required(df: DataFrame, columns: list[str]) -> DataFrame:
    return df.select(*columns)

def maybe_repartition(df: DataFrame, partitions: int | None = None, *cols) -> DataFrame:
    if partitions is None:
        return df
    return df.repartition(partitions, *cols) if cols else df.repartition(partitions)
