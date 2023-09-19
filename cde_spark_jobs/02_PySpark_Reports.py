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
data_path=config.get("general","data_path")
username=config.get("general","username")

cloudPath=data_lake_name+data_path

print("Running as Username: ", username)

_DEBUG_ = False

#---------------------------------------------------
#               CREATE SPARK SESSION
#---------------------------------------------------
spark = SparkSession.builder.appName('INGEST').config("spark.kubernetes.access.hadoopFileSystems", data_lake_name).getOrCreate()

#---------------------------------------------------
#               READ TABLES
#---------------------------------------------------
car_installs_df  = spark.sql("SELECT * FROM CDE_WORKSHOP_{0}.CAR_INSTALLS_{0}".format(username))
car_sales_df  = spark.sql("SELECT * FROM CDE_WORKSHOP_{0}.CAR_SALES_{0}".format(username))
factory_data_df  = spark.sql("SELECT * FROM CDE_WORKSHOP_{0}.EXPERIMENTAL_MOTORS_{0}".format(username))
customer_data_df  = spark.sql("SELECT * FROM CDE_WORKSHOP_{0}.CUSTOMER_DATA_{0}".format(username))
geo_data_df = spark.sql("SELECT * FROM CDE_WORKSHOP_{0}.GEO_DATA_XREF_{0}".format(username))

print("\tPOPULATE TABLE(S) COMPLETED")

#---------------------------------------------------
#             JOIN DATA INTO ONE TABLE
#---------------------------------------------------
# SQL way to do things
salesandcustomers_sql = "SELECT customers.*, sales.saleprice, sales.model, sales.VIN \
                            FROM CDE_WORKSHOP_{0}.CAR_SALES_{0} sales JOIN CDE_WORKSHOP_{0}.CUSTOMER_DATA_{0} customers \
                             ON sales.customer_id = customers.customer_id".format(username)

tempTable = spark.sql(salesandcustomers_sql)
if (_DEBUG_):
    print("\tTABLE: CAR_SALES")
    car_sales.show(n=5)
    print("\tTABLE: CUSTOMER_DATA")
    customer_data.show(n=5)
    print("\tJOIN: CAR_SALES x CUSTOMER_DATA")
    tempTable.show(n=5)

# Add geolocations based on ZIP
tempTable = tempTable.withColumn("postalcode", F.col("zip"))
tempTable = tempTable.join(geo_data_df, geo_data_df.postalcode == tempTable.postalcode).drop(tempTable.postalcode).drop(geo_data_df.id)
if (_DEBUG_):
    print("\tTABLE: GEO_DATA_XREF")
    geo_data_df.show(n=5)
    print("\tJOIN: CAR_SALES x CUSTOMER_DATA x GEO_DATA_XREF (zip)")
    tempTable.show(n=5)

# Add installation information (What part went into what car?)
#tempTable = tempTable.join(car_installs_df.drop("id"), ["VIN"])
#tempTable = tempTable.join(car_installs_df, car_installs_df.VIN == tempTable.VIN).drop(car_installs_df.model).drop(car_installs_df.VIN).drop(car_installs_df.id)

# Add installation information (What part went into what car?)
tempTable.join(car_installs_df, car_installs_df.id == tempTable.id).drop(car_installs_df.model).drop(car_installs_df.VIN).drop(car_installs_df.id)
if (_DEBUG_):
    print("\tTABLE: CAR_INSTALLS")
    car_installs_df.show(n=5)
    print("\tJOIN: CAR_SALES x CUSTOMER_DATA x GEO_DATA_XREF (zip) x CAR_INSTALLS (vin)")
    tempTable.show(n=5)

# Add factory information (For each part, in what factory was it made, from what machine, and at what time)
tempTable = tempTable.join(factory_data_df, factory_data_df.serial_no == tempTable.serial_no).drop(factory_data_df.serial_no).drop(factory_data_df.id)
if (_DEBUG_):
    print("\tTABLE: EXPERIMENTAL_MOTORS")
    factory_data_df.show(n=5)
    print("\tJOIN QUERY: CAR_SALES x CUSTOMER_DATA x GEO_DATA_XREF (zip) x CAR_INSTALLS (vin, model) x EXPERIMENTAL_MOTORS (serial_no)")
    tempTable.show(n=5)

#---------------------------------------------------
#             CREATE NEW HIVE TABLE
#---------------------------------------------------
tempTable.write.mode("overwrite").saveAsTable('CDE_WORKSHOP_{0}.experimental_motors_report_{0}_tuned'.format(username), format="parquet")
print("\tNEW ENRICHED TABLE CREATED: CDE_WORKSHOP_{0}.experimental_motors_report_{0}".format(username))
tempTable.show(n=5)
print("\n")
tempTable.dtypes

spark.stop()
print("JOB COMPLETED!\n\n")
