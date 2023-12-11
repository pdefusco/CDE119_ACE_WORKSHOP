#****************************************************************************
# (C) Cloudera, Inc. 2020-2022
#  All rights reserved.
#
#  Applicable Open Source License: GNU Affero General Public License v3.0
#
#  NOTE: Cloudera open source products are modular software products
#  made up of hundreds of individual components, each of which was
#  individually copyrighted.  Each Cloudera open source product is a
#  collective work under U.S. Copyright Law. Your license to use the
#  collective work is as provided in your written agreement with
#  Cloudera.  Used apart from the collective work, this file is
#  licensed for your use pursuant to the open source license
#  identified above.
#
#  This code is provided to you pursuant a written agreement with
#  (i) Cloudera, Inc. or (ii) a third-party authorized to distribute
#  this code. If you do not have a written agreement with Cloudera nor
#  with an authorized and properly licensed third party, you do not
#  have any rights to access nor to use this code.
#
#  Absent a written agreement with Cloudera, Inc. (“Cloudera”) to the
#  contrary, A) CLOUDERA PROVIDES THIS CODE TO YOU WITHOUT WARRANTIES OF ANY
#  KIND; (B) CLOUDERA DISCLAIMS ANY AND ALL EXPRESS AND IMPLIED
#  WARRANTIES WITH RESPECT TO THIS CODE, INCLUDING BUT NOT LIMITED TO
#  IMPLIED WARRANTIES OF TITLE, NON-INFRINGEMENT, MERCHANTABILITY AND
#  FITNESS FOR A PARTICULAR PURPOSE; (C) CLOUDERA IS NOT LIABLE TO YOU,
#  AND WILL NOT DEFEND, INDEMNIFY, NOR HOLD YOU HARMLESS FOR ANY CLAIMS
#  ARISING FROM OR RELATED TO THE CODE; AND (D)WITH RESPECT TO YOUR EXERCISE
#  OF ANY RIGHTS GRANTED TO YOU FOR THE CODE, CLOUDERA IS NOT LIABLE FOR ANY
#  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, PUNITIVE OR
#  CONSEQUENTIAL DAMAGES INCLUDING, BUT NOT LIMITED TO, DAMAGES
#  RELATED TO LOST REVENUE, LOST PROFITS, LOSS OF INCOME, LOSS OF
#  BUSINESS ADVANTAGE OR UNAVAILABILITY, OR LOSS OR CORRUPTION OF
#  DATA.
#
# #  Author(s): Paul de Fusco
#***************************************************************************/

# NB: THIS SCRIPT REQUIRES A SPARK 3 CLUSTER

#---------------------------------------------------
#               CREATE SPARK SESSION
#---------------------------------------------------

from pyspark.sql import SparkSession
from datetime import datetime
import sys
import configparser
import pyspark.sql.functions as F
from pyspark.sql.types import *
import pandas as pd

config = configparser.ConfigParser()
config.read('/app/mount/parameters.conf')
data_lake_name=config.get("general","data_lake_name")
data_path=config.get("general","data_path")
username=config.get("general","username")

cloudPath=data_lake_name+data_path

print("Running as Username: ", username)

spark = SparkSession \
    .builder \
    .appName("ICEBERG LOAD") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.iceberg.spark.SparkSessionCatalog")\
    .config("spark.sql.catalog.spark_catalog.type", "hive")\
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")\
    .config("spark.kubernetes.access.hadoopFileSystems", data_lake_name)\
    .getOrCreate()

#---------------------------------------------------
#               INSERT DATA
#---------------------------------------------------

# STORE TIMESTAMP BEFORE INSERTS
now = datetime.now()
timestamp = datetime.timestamp(now)
print("PRE-INSERT TIMESTAMP: ", timestamp)

print("PRE-INSERT TABLE SNAPSHOTS AND HISTORY")
spark.sql("SELECT * FROM spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0}.history".format(username)).show(20, False)
spark.sql("SELECT * FROM spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0}.snapshots".format(username)).show(20, False)

# PRE-INSERT COUNT
print("PRE-INSERT COUNT")
spark.sql("SELECT COUNT(*) FROM spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0}".format(username)).show()

# INSERT DATA APPROACH 1 - APPEND FROM DATAFRAME
temp_df = spark.sql("SELECT * FROM spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0}".format(username)).sample(fraction=0.1, seed=3)
temp_df.writeTo("spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0}".format(username)).append()

# INSERT DATA APPROACH 2 - INSERT VIA SQL
spark.sql("DROP TABLE IF EXISTS spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_SAMPLE_{0}".format(username))
temp_df.writeTo("spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_SAMPLE_{0}".format(username)).create()

print("INSERT DATA VIA SPARK SQL")
query_5 = """INSERT INTO spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0} SELECT * FROM spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_SAMPLE_{0}""".format(username)
print(query_5)
spark.sql(query_5)

#---------------------------------------------------
#               TIME TRAVEL
#---------------------------------------------------

# NOTICE SNAPSHOTS HAVE BEEN ADDED
#spark.read.format("iceberg").load("spark_catalog.{}_CAR_DATA.CAR_SALES.history".format(username)).show(20, False)
spark.sql("SELECT * FROM spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0}.history".format(username)).show(20, False)
spark.sql("SELECT * FROM spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0}.snapshots".format(username)).show(20, False)

# POST-INSERT COUNT
print("POST-INSERT COUNT")
spark.sql("SELECT COUNT(*) FROM spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0}".format(username)).show()

# TIME TRAVEL AS OF PREVIOUS TIMESTAMP
df = spark.read.option("as-of-timestamp", int(timestamp*1000)).format("iceberg").load("spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0}".format(username))

# POST TIME TRAVEL COUNT
print("POST-TIME TRAVEL COUNT")
print(df.count())

#---------------------------------------------------
#               INCREMENTAL REPORT
#---------------------------------------------------

# ICEBERG TABLE HISTORY (SHOWS EACH SNAPSHOT AND TIMESTAMP)
spark.sql("SELECT * FROM CDE_WORKSHOP_{0}.CAR_SALES_{0}.history;".format(username)).show()

# ICEBERG TABLE SNAPSHOTS (USEFUL FOR INCREMENTAL QUERIES AND TIME TRAVEL)
spark.sql("SELECT * FROM CDE_WORKSHOP_{0}.CAR_SALES_{0}.snapshots;".format(username)).show()

# STORE FIRST AND LAST SNAPSHOT ID'S FROM SNAPSHOTS TABLE
snapshots_df = spark.sql("SELECT * FROM CDE_WORKSHOP_{0}.CAR_SALES_{0}.snapshots;".format(username))

print("SHOWING SNAPSHOTS DF")
snapshots_df.show()

snapshots = snapshots_df.toPandas()

print("SHOWING PANDAS SNAPSHOTS DF")
snapshots.head()

last_snapshot = snapshots_df[["snapshot_id"]].iloc[1]
second_last_snapshot = snapshots_df[["snapshot_id"]].iloc[2]

print("PANDAS SNAPSHOTS")
print(last_snapshot)
print(second_last_snapshot)

#last_snapshot = snapshots_df.select("snapshot_id").tail(1)[0][0]
#first_snapshot = snapshots_df.select("snapshot_id").head(1)[0][0]

spark.read\
    .format("iceberg")\
    .option("start-snapshot-id", second_last_snapshot)\
    .option("end-snapshot-id", last_snapshot)\
    .load("spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0}".format(username)).show()

#---------------------------------------------------
#               ANALYTICAL QUERIES
#---------------------------------------------------

reports_df = spark.sql("SELECT * FROM CDE_WORKSHOP_{0}.SALES_REPORT_{0}".format(username))

print("GROUP TOTAL SALES BY MODEL")
model_sales_df = reports_df.groupBy("Model").sum("Saleprice").na.drop().sort(F.asc('sum(Saleprice)')).withColumnRenamed("sum(Saleprice)", "sales_by_model")
model_sales_df = model_sales_df.withColumn('total_sales_by_model', model_sales_df.sales_by_model.cast(DecimalType(18, 2)))
model_sales_df.select(["Model", "total_sales_by_model"]).sort(F.asc('Model')).show()

print("GROUP TOTAL SALES BY GENDER")
gender_sales_df = reports_df.groupBy("Gender").sum("Saleprice").na.drop().sort(F.asc('sum(Saleprice)')).withColumnRenamed("sum(Saleprice)", "sales_by_gender")
gender_sales_df = gender_sales_df.withColumn('total_sales_by_gender', gender_sales_df.sales_by_gender.cast(DecimalType(18, 2)))
gender_sales_df.select(["Gender", "total_sales_by_gender"]).sort(F.asc('Gender')).show()
