from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count

db_ip = "database"
COUCHDB_URL = f"http://{db_ip}:5984"
USERNAME = "team"
PASSWORD = "cloudcomputing"
DB_NAME = "images_database"

if __name__ == "__main__":
    spark = SparkSession.builder\
        .appName("MapReduce for incorrect inferences")\
        .config("spark.sql.warehouse.dir", "file:///tmp/spark-warehouse") \
        .getOrCreate()

    df = spark.read.format("jdbc") \
        .option("url", "http://team:cloudcomputing@database:5984") \
        .option("cloudant.username", USERNAME) \
        .option("cloudant.password", PASSWORD) \
        .option("database", DB_NAME) \
        .option("dbtable", DB_NAME) \
        .load()

    result_df = (
        df.filter(col("inference_result") == 1)
        .groupBy("producer")                  
        .agg(count("*").alias("incorrect_count"))
    )

    # Print results
    result_df.show()

    spark.stop()