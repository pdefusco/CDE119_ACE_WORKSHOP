import os
import sys
import argparse
from pyspark.sql import SparkSession

def parseargs():
    # ENTER YOUR STORAGE LOCATION HERE
    #e.g. AWS storage = 's3a://go01-demo'
    #e.g. Azure: storage = 'abfs://data@go01demoazure.dfs.core.windows.net'
    storage = sys.argv[1]
    return storage

def session(storage):
    spark = SparkSession\
        .builder\
        .appName("PythonSQL")\
        .config("spark.kubernetes.access.hadoopFileSystems", storage)\
        .getOrCreate()

    return spark

def read_df_from_resource(spark):
    try:
        csvDF = spark.read.options(header = 'True', delimiter=',', inferSchema='True').csv("/app/mount/test_file.csv")
        print("DF read successfully from /app/mount")
        return csvDF
    except Exception as e:
        print(f'caught {type(e)}: e')

def test_write_to_cloud_storage(spark, csvDF, storage):
    try:
        csvDF.write.options(header = 'True', sep=',', inferSchema='True').mode("overwrite").csv("{}/test_file.csv".format(storage))
        print("DF written successfully to Cloud Storage {}".format(storage))
        csvDF.show()
    except Exception as e:
        print(f'caught {type(e)}: e')
        print("DF NOT written successfully to Cloud Storage {}".format(storage))

def test_read_from_cloud_storage(spark, storage):
    try:
        csvDF = spark.read.options(header = 'True', delimiter=',', inferSchema='True').csv("{}/test_file.csv".format(storage))
        print("DF read successfully from Cloud Storage: {}".format(storage))
        csvDF.show()
    except Exception as e:
        print(f'caught {type(e)}: e')
        print("DF NOT written successfully to Cloud Storage {}".format(storage))

def main():
    storage = parseargs()
    print("Launch Spark Session")
    spark = session(storage)
    print("Run Tests:\n")
    csvDF = read_df_from_resource(spark)
    test_write_to_cloud_storage(spark, csvDF, storage)
    test_read_from_cloud_storage(spark, storage)

if __name__ == "__main__":
    main()
