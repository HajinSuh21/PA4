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

    rdd = spark.read.text(sys.argv[1]).rdd

    pairs_rdd = rdd.flatMap(lambda x: [(k, v) for k, v in eval(x[0]).items()])

    counts_rdd = pairs_rdd.map(lambda x: (x, 1)) \
                          .reduceByKey(lambda a, b: a + b)

    results = counts_rdd.collect()
    for pair, count in results:
        print(f"{pair}: {count}")

    spark.stop()