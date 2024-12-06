from pyspark.sql import SparkSession
# from pyspark.sql.functions import col, explode
# from pyspark.sql.types import StructType, StructField, IntegerType, StringType
# from pyspark import SparkFiles
import json
import sys
from operator import add

# if __name__ == "__main__":
#     spark = SparkSession.builder \
#         .appName("Incorrect Predictions Count") \
#         .getOrCreate()

#     # local_json_path = "file:///home/cc/team17/PA4/Spark/target/incorrect_count.json"
#     # local_json_path = "file:///app/incorrect_count.json"
#     # spark.sparkContext.addFile(local_json_path)

#     # json_file_path = SparkFiles.get("incorrect_count.json")

#     schema = StructType([
#         StructField("Latency", IntegerType(), True),
#         StructField("IsCorrect", IntegerType(), True)
#     ])

#     df = spark.read.schema(schema).json(local_json_path)

#     df.printSchema()

#     # df_transformed = df.select(explode(df.columns[0]).alias("key", "data")) \
#     #     .selectExpr("data.Latency as Latency", "data.IsCorrect as IsCorrect")

#     df_transformed = df.select(explode("source").alias("key", "data")) \
#     .select(col("data.Latency").alias("Latency"), col("data.IsCorrect").alias("IsCorrect"))

#     incorrect_count = df_transformed.filter(col("IsCorrect") == 0).count()

#     # incorrect_count = df.filter(col("IsCorrect") == 0).count()

#     print(f"Total incorrect predictions: {incorrect_count}")

#     spark.stop()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: wordcount <file>", file=sys.stderr)
        sys.exit(-1)

    spark = SparkSession\
        .builder\
        .appName("PythonWordCount")\
        .getOrCreate()

    lines = spark.read.text(sys.argv[1]).rdd.map(lambda r: r[0])
    counts = lines.flatMap(lambda x: x.split(' ')) \
                  .map(lambda x: (x, 1)) \
                  .reduceByKey(add)
    output = counts.collect()
    for (word, count) in output:
        print("%s: %i" % (word, count))

    spark.stop()