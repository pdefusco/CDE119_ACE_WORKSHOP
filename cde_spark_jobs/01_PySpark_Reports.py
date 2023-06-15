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
car_installs  = spark.read.csv(s3BucketName + "/car_installs.csv",        header=True, inferSchema=True)
car_sales     = spark.read.csv(s3BucketName + "/historical_car_sales.csv",           header=True, inferSchema=True)
customer_data = spark.read.csv(s3BucketName + "/customer_data.csv",       header=True, inferSchema=True)
factory_data  = spark.read.csv(s3BucketName + "/experimental_motors.csv", header=True, inferSchema=True)
geo_data      = spark.read.csv(s3BucketName + "/postal_codes.csv",        header=True, inferSchema=True)

#---------------------------------------------------
#       SQL CLEANUP: DATABASES, TABLES, VIEWS
#---------------------------------------------------
#print("JOB STARTED...")
#spark.sql("DROP DATABASE IF EXISTS CDE_WORKSHOP CASCADE")

##---------------------------------------------------
##                 CREATE DATABASES
##---------------------------------------------------
#spark.sql("CREATE DATABASE CDE_WORKSHOP")

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

#---------------------------------------------------
#               RUNNING DATA QUALITY TESTS
#---------------------------------------------------

# Test 1: Ensure Customer ID is Present so Join Can Happen
print("RUNNING DATA QUALITY TESTS WITH QUINN LIBRARY")
utils.test_column_presence(car_sales, ["customer_id"])
utils.test_column_presence(customer_data, ["customer_id"])

# Test 2: Spot Nulls or Blanks in Customer Data Sale Price Column:
car_sales = utils.test_null_presence_in_col(car_sales, "saleprice")

# Test 3:
#customer_data_df = utils.test_values_not_in_col(customer_data_df, ["99999", "11111", "00000"], "zip")

#---------------------------------------------------
#                  APPLY FILTERS
# - Remove under aged drivers (less than 16 yrs old)
#---------------------------------------------------
#before = customer_data.count()

print(customer_data.dtypes)
print(customer_data.schema)

customer_data = customer_data.filter(col('birthdate') <= F.add_months(F.current_date(),-192))
#after = customer_data.count()
print(f"\tFILTER DATA (CUSTOMER_DATA): Before({before}), After ({after}), Difference ({after - before}) rows")

#---------------------------------------------------
#             JOIN DATA INTO ONE TABLE
#---------------------------------------------------
# SQL way to do things
salesandcustomers_sql = "SELECT customers.*, sales.saleprice, sales.model, sales.VIN \
                            FROM CDE_WORKSHOP.CAR_SALES_{0} sales JOIN CDE_WORKSHOP.CUSTOMER_DATA_{0} customers \
                             ON sales.customer_id = customers.customer_id ".format(username)

tempTable = spark.sql(salesandcustomers_sql)
if (_DEBUG_):
    print("\tTABLE: CAR_SALES")
    car_sales.show(n=5)
    print("\tTABLE: CUSTOMER_DATA")
    customer_data.show(n=5)
    print("\tJOIN: CAR_SALES x CUSTOMER_DATA")
    tempTable.show(n=5)

# Add geolocations based on ZIP
tempTable = tempTable.join(geo_data, "zip")
if (_DEBUG_):
    print("\tTABLE: GEO_DATA_XREF")
    geo_data.show(n=5)
    print("\tJOIN: CAR_SALES x CUSTOMER_DATA x GEO_DATA_XREF (zip)")
    tempTable.show(n=5)

# Add installation information (What part went into what car?)
tempTable = tempTable.join(car_installs, ["VIN","model"])
if (_DEBUG_):
    print("\tTABLE: CAR_INSTALLS")
    car_installs.show(n=5)
    print("\tJOIN: CAR_SALES x CUSTOMER_DATA x GEO_DATA_XREF (zip) x CAR_INSTALLS (vin, model)")
    tempTable.show(n=5)

# Add factory information (For each part, in what factory was it made, from what machine, and at what time)
tempTable = tempTable.join(factory_data, ["serial_no"])
if (_DEBUG_):
    print("\tTABLE: EXPERIMENTAL_MOTORS")
    factory_data.show(n=5)
    print("\tJOIN QUERY: CAR_SALES x CUSTOMER_DATA x GEO_DATA_XREF (zip) x CAR_INSTALLS (vin, model) x EXPERIMENTAL_MOTORS (serial_no)")
    tempTable.show(n=5)

#---------------------------------------------------
#             CREATE NEW HIVE TABLE
#---------------------------------------------------
tempTable.write.mode("overwrite").saveAsTable('CDE_WORKSHOP.experimental_motors_enriched_{}'.format(username), format="parquet")
print("\tNEW ENRICHED TABLE CREATED: CDE_WORKSHOP.experimental_motors_enriched_{}".format(username))
tempTable.show(n=5)

spark.stop()
print("JOB COMPLETED!\n\n")
