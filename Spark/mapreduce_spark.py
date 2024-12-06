from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from pyspark import SparkFiles
import requests
import json

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("Incorrect Predictions Count") \
        .getOrCreate()

    # local_json_path = "file:///home/cc/team17/PA4/Spark/target/incorrect_count.json"
    local_json_path = "file:///app/incorrect_count.json"
    # spark.sparkContext.addFile(local_json_path)

    # json_file_path = SparkFiles.get("incorrect_count.json")

    schema = StructType([
        StructField("Latency", IntegerType(), True),
        StructField("IsCorrect", IntegerType(), True)
    ])

    df = spark.read.schema(schema).json(local_json_path)

    df.printSchema()

    # df_transformed = df.select(explode(df.columns[0]).alias("key", "data")) \
    #     .selectExpr("data.Latency as Latency", "data.IsCorrect as IsCorrect")

    # incorrect_count = df_transformed.filter(col("IsCorrect") == 0).count()

    incorrect_count = df.filter(col("IsCorrect") == 0).count()

    print(f"Total incorrect predictions: {incorrect_count}")

    spark.stop()