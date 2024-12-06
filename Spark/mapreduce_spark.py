from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode
from pyspark import SparkFiles
import requests
import json

spark = SparkSession.builder \
    .appName("Incorrect Predictions Count") \
    .getOrCreate()

local_json_path = "file:///home/cc/team17/PA4/Spark/target/incorrect_count.json"
# spark.sparkContext.addFile(local_json_path)

# json_file_path = SparkFiles.get("incorrect_count.json")

df = spark.read.json(json_file_path)

df_transformed = df.select(explode(col("*")).alias("data")) \
    .selectExpr("data.Latency as Latency", "data.IsCorrect as IsCorrect")

incorrect_count = df_transformed.filter(col("IsCorrect") == 0).count()

print(f"Total incorrect predictions: {incorrect_count}")

spark.stop()