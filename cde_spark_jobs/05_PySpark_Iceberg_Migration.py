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

#---------------------------------------------------
#               SHOW ICEBERG TABLE SNAPSHOTS
#---------------------------------------------------

spark.read.format("iceberg").load("spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0}.history".format(username)).show(20, False)
spark.read.format("iceberg").load("spark_catalog.CDE_WORKSHOP_{0}.CAR_SALES_{0}.snapshots".format(username)).show(20, False)
