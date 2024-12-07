from pyspark.sql import SparkSession
# from pyspark.sql.functions import col, explode
# from pyspark.sql.types import StructType, StructField, IntegerType, StringType
# from pyspark import SparkFiles
import json
import sys
from operator import add

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("Incorrect Producer Count") \
        .getOrCreate()

    rdd = spark.read.json(sys.argv[1]).rdd

    ones_count = rdd.flatMap(lambda x: json.loads(x[0]).values()) \
                    .filter(lambda v: v == 1) \
                    .count()

    print(f"Total number of incorrect predictions: {ones_count}")

    spark.stop()