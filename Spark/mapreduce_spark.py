from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count

db_ip = "database"
COUCHDB_URL = f"http://{db_ip}:5984"
USERNAME = "team"
PASSWORD = "cloudcomputing"
DB_NAME = "images_database"

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("IncorrectPredictionsCounter") \
        .config("cloudant.host", f"{db_ip}:5984") \
        .config("cloudant.username", USERNAME) \
        .config("cloudant.password", PASSWORD) \
        .config("cloudant.use._id", "true") \
        .getOrCreate()

    df = spark.read.format("org.apache.bahir.cloudant") \
        .option("database", DB_NAME) \
        .load()
    
    df = df.select("_id", "GroundTruth", "prediction") \
           .filter(col("GroundTruth").isNotNull() & col("prediction").isNotNull())

    df = df.withColumn("IsIncorrect", col("GroundTruth") != col("prediction"))

    total_incorrect = df.filter(col("IsIncorrect") == True).count()

    print(f"Total number of incorrect predictions: {total_incorrect}")

    spark.stop()