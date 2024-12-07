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

    rdd = spark.read.text(sys.argv[1]).rdd.map(lambda r: r[0])

    incorrect_count = rdd.flatMap(lambda x: x.split(",")) \
                    .filter(lambda v: ": 1" in v) \
                    .count()

    print(f"Total number of incorrect predictions: {incorrect_count}")

    spark.stop()