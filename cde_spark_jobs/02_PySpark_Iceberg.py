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
import utils

config = configparser.ConfigParser()
config.read('/app/mount/parameters.conf')
data_lake_name=config.get("general","data_lake_name")
s3BucketName=config.get("general","s3BucketName")
username=config.get("general","username")

print("Running as Username: ", username)

spark = SparkSession \
    .builder \
    .appName("ICEBERG LOAD") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.iceberg.spark.SparkSessionCatalog")\
    .config("spark.sql.catalog.spark_catalog.type", "hive")\
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")\
    .config("spark.yarn.access.hadoopFileSystems", data_lake_name)\
    .getOrCreate()

#print("TOP 20 ROWS IN CAR SALES TABLE")
#spark.sql("SELECT * FROM CDE_WORKSHOP.CAR_SALES_{}".format(username)).show()

#print("\n")
#print("CAR SALES TABLE PRE-ICEBERG MIGRATION PARTITIONS: ")
#print("SHOW PARTITIONS {}_CAR_DATA.CAR_SALES".format(username))
#spark.sql("SHOW PARTITIONS {}_CAR_DATA.CAR_SALES".format(username)).show()

#----------------------------------------------------
#               MIGRATE SPARK TABLES TO ICEBERG TABLE
#----------------------------------------------------
try:
    print("ALTER TABLE CDE_WORKSHOP_{0}.CAR_SALES_{0} UNSET TBLPROPERTIES ('TRANSLATED_TO_EXTERNAL')".format(username))
    spark.sql("ALTER TABLE CDE_WORKSHOP_{0}.CAR_SALES_{0} UNSET TBLPROPERTIES ('TRANSLATED_TO_EXTERNAL')".format(username))
    print("CALL spark_catalog.system.migrate('CDE_WORKSHOP_{0}.CAR_SALES_{0}')".format(username))
    spark.sql("CALL spark_catalog.system.migrate('CDE_WORKSHOP_{0}.CAR_SALES_{0}')".format(username))
    print("Migrated the Car Sales Table to Iceberg Format.")
except:
    print("The Car Sales table has already been migrated to Iceberg Format.")

try:
    print("ALTER TABLE CDE_WORKSHOP_{0}.CUSTOMER_DATA_{0} UNSET TBLPROPERTIES ('TRANSLATED_TO_EXTERNAL')".format(username))
    spark.sql("ALTER TABLE CDE_WORKSHOP_{0}.CUSTOMER_DATA_{0} UNSET TBLPROPERTIES ('TRANSLATED_TO_EXTERNAL')".format(username))
    print("CALL spark_catalog.system.migrate('CDE_WORKSHOP_{0}.CUSTOMER_DATA_{0}')".format(username))
    spark.sql("CALL spark_catalog.system.migrate('CDE_WORKSHOP_{0}.CUSTOMER_DATA_{0}')".format(username))
    print("Migrated the Customer Data table to Iceberg Format.")
except:
    print("The Customer Data table has already been migrated to Iceberg.")

#print("\n")
#print("LIST POST-ICEBERG MIGRATION PARTITIONS: ")
#print("SHOW PARTITIONS spark_catalog.{}_CAR_DATA.CAR_SALES".format(username))
#spark.sql("SHOW PARTITIONS spark_catalog.{}_CAR_DATA.CAR_SALES".format(username)).show()
#print("DESCRIBE TABLE spark_catalog.{}_CAR_DATA.CAR_SALES".format(username))
#spark.sql("DESCRIBE TABLE spark_catalog.{}_CAR_DATA.CAR_SALES".format(username)).show()

#---------------------------------------------------
#                READ SOURCE TABLES
#---------------------------------------------------
"""print("JOB STARTED...")
car_sales     = spark.sql("SELECT * FROM CDE_WORKSHOP_{0}.CAR_SALES_{0}".format(username)) #could also checkpoint here but need to set checkpoint dir
customer_data = spark.sql("SELECT * FROM CDE_WORKSHOP_{0}.CUSTOMER_DATA_{0}".format(username))
car_installs  = spark.sql("SELECT * FROM CDE_WORKSHOP_{0}.CAR_INSTALLS_{0}".format(username))
factory_data  = spark.sql("SELECT * FROM CDE_WORKSHOP_{0}.EXPERIMENTAL_MOTORS_{0}".format(username))
geo_data      = spark.sql("SELECT postalcode as zip, latitude, longitude FROM CDE_WORKSHOP_{0}.GEO_DATA_XREF_{0}".format(username))
print("\tREAD TABLE(S) COMPLETED")

print("CAR SALES TABLE POST-ICEBERG MIGRATION PARTITIONS: ")
spark.sql("SELECT * FROM spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0}.PARTITIONS".format(username)).show()"""

#---------------------------------------------------
#               SHOW ICEBERG TABLE SNAPSHOTS
#---------------------------------------------------

spark.read.format("iceberg").load("spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0}.history".format(username)).show(20, False)
spark.read.format("iceberg").load("spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0}.snapshots".format(username)).show(20, False)

#spark.sql("SELECT * FROM spark_catalog.{}_CAR_DATA.CAR_SALES.history".format(username)).show(20, False)
#spark.sql("SELECT * FROM spark_catalog.{}_CAR_DATA.CAR_SALES.snapshots".format(username)).show(20, False)

# STORE TIMESTAMP BEFORE INSERTS
now = datetime.now()
timestamp = datetime.timestamp(now)
print("PRE-INSERT TIMESTAMP: ", timestamp)

#---------------------------------------------------
#               INSERT DATA
#---------------------------------------------------

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
#               INCREMENTAL READ
#---------------------------------------------------

# ICEBERG TABLE HISTORY (SHOWS EACH SNAPSHOT AND TIMESTAMP)
spark.sql("SELECT * FROM CDE_WORKSHOP_{0}.CAR_SALES_{0}.history;".format(username)).show()

# ICEBERG TABLE SNAPSHOTS (USEFUL FOR INCREMENTAL QUERIES AND TIME TRAVEL)
spark.sql("SELECT * FROM CDE_WORKSHOP_{0}.CAR_SALES_{0}.snapshots;".format(username)).show()

# STORE FIRST AND LAST SNAPSHOT ID'S FROM SNAPSHOTS TABLE
snapshots_df = spark.sql("SELECT * FROM CDE_WORKSHOP_{0}.CAR_SALES_{0}.snapshots;".format(username))

last_snapshot = snapshots_df.select("snapshot_id").tail(1)[0][0]
first_snapshot = snapshots_df.select("snapshot_id").head(1)[0][0]

spark.read\
    .format("iceberg")\
    .option("start-snapshot-id", first_snapshot)\
    .option("end-snapshot-id", last_snapshot)\
    .load("spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0}".format(username)).show()

#---------------------------------------------------
#               SAVE DATA TO PARQUET
#---------------------------------------------------
#from datetime import datetime
#write_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#temp_df.write.mode("overwrite").option("header", "true").parquet(s3BucketName+write_time+"/car_sales_data.parquet")

#---------------------------------------------------
#            LOAD ICEBERG TABLES AS SPARK DATAFRAMES
#---------------------------------------------------

car_sales_df = spark.sql("SELECT * FROM spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0}".format(username))
customer_data_df = spark.sql("SELECT * FROM spark_catalog.CDE_WORKSHOP_{0}.CUSTOMER_DATA_{0}".format(username))

#---------------------------------------------------
#               LOAD NEW BATCH DATA
#---------------------------------------------------

batch_df = spark.read.csv(s3BucketName + "/10012020_car_sales.csv", header=True, inferSchema=True)
#batch_etl_df.write.mode("overwrite").saveAsTable('{}_CAR_DATA.CAR_SALES'.format(username), format="parquet")

# Creating Temp View for MERGE INTO command
batch_df.createOrReplaceTempView('CAR_SALES_TEMP_{}'.format(username))
print("\n")
print("COMPARING CAR SALES AND CAR SALES TEMP TABLES")
print("SELECT * FROM spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0}".format(username))
spark.sql("SELECT * FROM spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0}".format(username)).show()
print("\n")
print("SELECT * FROM CAR_SALES_TEMP_{0}".format(username))
spark.sql("SELECT * FROM CAR_SALES_TEMP_{0}".format(username)).show()

#---------------------------------------------------
#               ICEBERG PARTITION EVOLUTION
#---------------------------------------------------

print("CAR SALES TABLE PARTITIONS BEFORE ALTER PARTITION STATEMENT: ")
spark.sql("SELECT * FROM spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0}.PARTITIONS".format(username)).show()

testdf = spark.sql("SELECT * FROM spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0}".format(username))

print("-------")
print(testdf.schema)
print("-------")
print(testdf.dtypes)
print("-------")

print("REPLACE PARTITION FIELD MONTH WITH FIELD DAY:")
print("ALTER TABLE spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0} REPLACE PARTITION FIELD MONTH WITH DAY".format(username))
spark.sql("ALTER TABLE spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0} REPLACE PARTITION FIELD month WITH day".format(username))
#spark.sql("ALTER TABLE prod.db.sample ADD PARTITION FIELD month")

print("CAR SALES TABLE PARTITIONS AFTER ALTER PARTITION STATEMENT: ")
spark.sql("SELECT * FROM spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0}.PARTITIONS".format(username)).show()

#---------------------------------------------------
#               ICEBERG SCHEMA EVOLUTION
#---------------------------------------------------

# DROP COLUMNS
print("EXECUTING ICEBERG DROP COLUMN STATEMENT:")
print("ALTER TABLE spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0} DROP COLUMN VIN".format(username))
spark.sql("ALTER TABLE spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0} DROP COLUMN VIN".format(username))

# CAST COLUMN TO BIGINT
#print("EXECUTING ICEBERG TYPE CONVERSION STATEMENT")
#print("ALTER TABLE {}_CAR_DATA.CAR_SALES ALTER COLUMN CUSTOMER_ID TYPE BIGINT".format(username))
#spark.sql("ALTER TABLE {}_CAR_DATA.CAR_SALES ALTER COLUMN CUSTOMER_ID TYPE BIGINT".format(username))

#---------------------------------------------------
#               ICEBERG MERGE INTO
#---------------------------------------------------

# PRE-INSERT COUNT
print("\n")
print("PRE-MERGE COUNT")
spark.sql("SELECT COUNT(*) FROM spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0}".format(username)).show()

ICEBERG_MERGE_INTO = "MERGE INTO spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0} t USING (SELECT CUSTOMER_ID, MODEL, SALEPRICE, DAY, MONTH, YEAR FROM CAR_SALES_TEMP_{0}) s ON s.customer_id = t.customer_id WHEN MATCHED THEN UPDATE SET t.saleprice = s.saleprice".format(username)

#s.model = 'Model Q' THEN UPDATE SET t.saleprice = t.saleprice - 100\
#WHEN MATCHED AND s.model = 'Model R' THEN UPDATE SET t.saleprice = t.saleprice + 10\
print("\n")
print("EXECUTING ICEBERG MERGE INTO QUERY")
print(ICEBERG_MERGE_INTO)
spark.sql(ICEBERG_MERGE_INTO)

# PRE-INSERT COUNT
print("\n")
print("POST-MERGE COUNT")
spark.sql("SELECT COUNT(*) FROM spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0}".format(username)).show()

#---------------------------------------------------
#               ICEBERG TABLE HISTORY AND SNAPSHOTS
#---------------------------------------------------

# ICEBERG TABLE HISTORY (SHOWS EACH SNAPSHOT AND TIMESTAMP)
print("SHOW ICEBERG TABLE HISTORY")
print("SELECT * FROM spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0}.history;".format(username))
spark.sql("SELECT * FROM spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0}.history;".format(username)).show()

# ICEBERG TABLE SNAPSHOTS (USEFUL FOR INCREMENTAL QUERIES AND TIME TRAVEL)
print("SHOW ICEBERG TABLE SNAPSHOTS")
print("SELECT * FROM spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0}.snapshots;".format(username))
spark.sql("SELECT * FROM spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0}.snapshots;".format(username)).show()

#---------------------------------------------------
#               JOIN CUSTOMER AND SALES DATA
#---------------------------------------------------

#spark.sql("DROP TABLE IF EXISTS spark_catalog.{0}_CAR_DATA.CAR_SALES_REPORTS PURGE".format(username))
print("EXECUTING ICEBERG CREATE OR REPLACE TABLE STATEMENT")
print("CREATE OR REPLACE TABLE spark_catalog.CDE_WORKSHOP_{0}.SALES_REPORT_{0} USING ICEBERG AS SELECT s.MODEL, s.SALEPRICE, c.SALARY, c.GENDER, c.EMAIL FROM spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0} s INNER JOIN spark_catalog.CDE_WORKSHOP_{0}.CUSTOMER_DATA_{0} c on s.CUSTOMER_ID = c.CUSTOMER_ID".format(username))
spark.sql("CREATE OR REPLACE TABLE spark_catalog.CDE_WORKSHOP_{0}.SALES_REPORT_{0} USING ICEBERG AS SELECT s.MODEL, s.SALEPRICE, c.SALARY, c.GENDER, c.EMAIL FROM spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0} s INNER JOIN spark_catalog.CDE_WORKSHOP_{0}.CUSTOMER_DATA_{0} c on s.CUSTOMER_ID = c.CUSTOMER_ID".format(username))

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
