import requests
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count

db_ip = "database"
db_name = "images_database"
COUCHDB_URL = f"http://{db_ip}:5984"
USERNAME = "team"
PASSWORD = "cloudcomputing"
LOCAL_JSON_FILE = "/home/cc/team17/PA4/tmp/couchdb_data.json"

response = requests.get(f"{COUCHDB_URL}/{db_name}",
                            auth=(USERNAME, PASSWORD))
if response.status_code == 200:
    data = response.json()
    # Write JSON data to a file
    with open(LOCAL_JSON_FILE, "w") as file:
        json.dump(data["rows"], file)
else:
    raise Exception(f"Failed to fetch data from CouchDB: {response.status_code}, {response.text}")

spark = SparkSession.builder \
    .appName("Incorrect Prediction MapReduce") \
    .getOrCreate()

df = spark.read.format("json").load(LOCAL_JSON_FILE)

documents_df = df.select("doc.*")

incorrect_predictions_df = documents_df.filter(col("GroundTruth") != col("prediction"))

total_incorrect = incorrect_predictions_df.count()

print(f"Total incorrect predictions: {total_incorrect}")