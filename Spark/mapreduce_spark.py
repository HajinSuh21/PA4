from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import requests
import json

COUCHDB_URL = "http://10.0.0.15:5984/team17database"
USERNAME = "team"
PASSWORD = "cloudcomputing"

def fetch_documents():
    response = requests.get(COUCHDB_URL, auth=(USERNAME, PASSWORD))
    if response.status_code == 200:
        print(f"Success fetching documents")
        return response.json()['rows']
    else:
        print(f"Error fetching documents: {response.status_code}")
        return []

spark = SparkSession.builder \
    .appName("Incorrect Predictions Count") \
    .getOrCreate()

documents = fetch_documents()

data = []
for doc in documents:
    if 'doc' in doc:
        record = doc['doc']
        # Ensure both ground_truth and prediction are present
        if 'ground_truth' in record and 'prediction' in record:
            data.append((record['ground_truth'], record['prediction']))

df = spark.createDataFrame(data, ["ground_truth", "prediction"])

incorrect_predictions_count = df.filter(col("ground_truth") != col("prediction")).count()

print(f"Total incorrect predictions: {incorrect_predictions_count}")

spark.stop()