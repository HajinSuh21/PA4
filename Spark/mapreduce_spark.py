from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count

spark = SparkSession.builder \
    .appName("CouchDB MapReduce") \
    .getOrCreate()

couchdb_url = "http://team:cloudcomputing@database:5984/images_database/_all_docs?include_docs=true"

df = spark.read.format("json").load(couchdb_url)

documents_df = df.select("rows.doc.*")

incorrect_predictions_df = documents_df.filter(col("GroundTruth") != col("prediction"))

total_incorrect = incorrect_predictions_df.count()

print(f"Total incorrect predictions: {total_incorrect}")