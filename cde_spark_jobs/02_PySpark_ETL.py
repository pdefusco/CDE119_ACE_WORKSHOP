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

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import pyspark.sql.functions as F
import configparser
import utils
from demo_utils import simple_udf

config = configparser.ConfigParser()
config.read('/app/mount/parameters.conf')
data_lake_name=config.get("general","data_lake_name")
s3BucketName=config.get("general","s3BucketName")
username=config.get("general","username")

print("Running as Username: ", username)

#---------------------------------------------------
#               CREATE SPARK SESSION
#---------------------------------------------------
spark = SparkSession.builder.appName('INGEST').config("spark.yarn.access.hadoopFileSystems", data_lake_name).getOrCreate()

#-----------------------------------------------------------------------------------
# LOAD DATA FROM .CSV FILES ON AWS S3 CLOUD STORAGE
#
# REQUIREMENT: Update variable s3BucketName
#              using storage.location.base attribute; defined by your environment.
#
#              For example, property storage.location.base
#                           has value 's3a://usermarketing-cdp-demo'
#                           Therefore, set variable as:
#                                 s3BucketName = "s3a://usermarketing-cdp-demo"
#-----------------------------------------------------------------------------------

car_installs  = spark.read.csv(s3BucketName + "/car_installs_119.csv",        header=True, inferSchema=True)
car_sales     = spark.read.csv(s3BucketName + "/car_sales_119.csv", header=True, inferSchema=True)
customer_data = spark.read.csv(s3BucketName + "/customer_data_119.csv",       header=True, inferSchema=True)
factory_data  = spark.read.csv(s3BucketName + "/factory_data_119.csv", header=True, inferSchema=True)
geo_data      = spark.read.csv(s3BucketName + "/geo_data_119.csv",        header=True, inferSchema=True)

#---------------------------------------------------
#       SQL CLEANUP: DATABASES, TABLES, VIEWS
#---------------------------------------------------
print("JOB STARTED...")
spark.sql("DROP DATABASE IF EXISTS CDE_WORKSHOP CASCADE")

##---------------------------------------------------
##                 CREATE DATABASES
##---------------------------------------------------
spark.sql("CREATE DATABASE IF NOT EXISTS CDE_WORKSHOP")

#---------------------------------------------------
#       RUNNING DATA QUALITY TESTS WITH PYTHON LIB
#---------------------------------------------------

# Test 1: Ensure Customer ID is Present so Join Can Happen
print("RUNNING DATA QUALITY TESTS WITH QUINN LIBRARY")
utils.test_column_presence(car_sales, ["customer_id"])
utils.test_column_presence(customer_data, ["customer_id"])

# Test 2: Spot Nulls or Blanks in Customer Data Sale Price Column:
car_sales = utils.test_null_presence_in_col(car_sales, "saleprice")

#---------------------------------------------------
#       RUNNING DATA QUALITY TESTS WITH PYTHON UDF
#---------------------------------------------------
print("SPARK UDF")

spark.udf.register("TSTAMP_TO_STRING", simple_udf.tstampToString)
spark.sql("SELECT TSTAMP_TO_STRING(timestamp) AS tstamp_str, timestamp FROM factory.experimental_motors_enriched LIMIT 10").show()

#---------------------------------------------------
#       TRANSFORM FUTURE JOIN KEYS
#---------------------------------------------------

car_sales = car_sales.withColumn("car_model", F.when(F.col("model") == "Model A","A") \
      .when(F.col("model") == "Model B","B") \
      .when(F.col("model") == "Model C","C") \
      .when(F.col("model") == "Model D","D") \
      .when(F.col("model") == "Model E","E")\
      .when(F.col("model") == "Model F","F") \
      .when(F.col("model") == "Model G","G") \
      .when(F.col("model") == "Model H","H") \
      .when(F.col("model") == "Model I","I"))\
      .drop(F.col("model"))\
      .withColumnRenamed("car_model","model")

#---------------------------------------------------
#                  APPLY FILTERS
# - Remove under aged drivers (less than 16 yrs old)
#---------------------------------------------------
#before = customer_data.count()

print(customer_data.dtypes)
print(customer_data.schema)

customer_data = customer_data.filter(col('birthdate') <= F.add_months(F.current_date(),-192))

#---------------------------------------------------
#               POPULATE TABLES
#---------------------------------------------------

#NB: The car sales table is partitioned by month
car_sales.write.mode("overwrite").partitionBy("month").saveAsTable('CDE_WORKSHOP.CAR_SALES_{}'.format(username), format="parquet")
car_installs.write.mode("overwrite").saveAsTable('CDE_WORKSHOP.CAR_INSTALLS_{}'.format(username), format="parquet")
factory_data.write.mode("overwrite").saveAsTable('CDE_WORKSHOP.EXPERIMENTAL_MOTORS_{}'.format(username), format="parquet")
customer_data.write.mode("overwrite").saveAsTable('CDE_WORKSHOP.CUSTOMER_DATA_{}'.format(username), format="parquet")
geo_data.write.mode("overwrite").saveAsTable('CDE_WORKSHOP.GEO_DATA_XREF_{}'.format(username), format="parquet")
print("\tPOPULATE TABLE(S) COMPLETED")
