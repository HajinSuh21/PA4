from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode
import requests
import json

spark = SparkSession.builder \
    .appName("Incorrect Predictions Count") \
    .getOrCreate()

incorrect_count_json = "./Spark/target/incorrect_count.json"
df = spark.read.json(incorrect_count_json)

df_transformed = df.select(explode(col("*")).alias("data")) \
    .selectExpr("data.Latency as Latency", "data.IsCorrect as IsCorrect")

incorrect_count = df_transformed.filter(col("IsCorrect") == 0).count()

print(f"Total incorrect predictions: {incorrect_count}")

spark.stop()