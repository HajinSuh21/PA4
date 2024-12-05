from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import requests
import json

db_ip = "database"
COUCHDB_URL = f"http://{db_ip}:5984"
USERNAME = "team"
PASSWORD = "cloudcomputing"
DB_NAME = "images_database"

def get_all_documents(COUCHDB_URL, DB_NAME, USERNAME, PASSWORD):
    # Get all documents in the database
    response = requests.get(
        f"{COUCHDB_URL}/{DB_NAME}/_all_docs?include_docs=true", auth=(USERNAME, PASSWORD))
    if response.status_code == 200:
        print(f"SUCCESS FETCHING DOCS")
        return response.json()['rows']
    else:
        print(f"Error fetching documents: {response.json()}")
        return []

spark = SparkSession.builder \
    .appName("Incorrect Predictions Count") \
    .getOrCreate()

documents = get_all_documents(COUCHDB_URL, DB_NAME, USERNAME, PASSWORD)
# data = []
for doc in documents:
    print(doc)

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