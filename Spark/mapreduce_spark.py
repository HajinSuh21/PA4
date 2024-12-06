from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import requests
import json

spark = SparkSession.builder \
    .appName("Incorrect Predictions Count") \
    .getOrCreate()

# data = []
# for doc in documents:
#     if 'doc' in doc:
#         record = doc['doc']
#         # Ensure both ground_truth and prediction are present
#         if 'ground_truth' in record and 'prediction' in record:
#             data.append((record['ground_truth'], record['prediction']))

# df = spark.createDataFrame(data, ["ground_truth", "prediction"])

# incorrect_predictions_count = df.filter(col("ground_truth") != col("prediction")).count()

# print(f"Total incorrect predictions: {incorrect_predictions_count}")

# spark.stop()