#****************************************************************************
# (C) Cloudera, Inc. 2022
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

from __future__ import print_function
import os, uuid, sys
from pyspark.sql import SparkSession
from pyspark.sql.types import Row, StructField, StructType, StringType, IntegerType
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core._match_conditions import MatchConditions
from azure.storage.filedatalake._models import ContentSettings

spark = SparkSession\
    .builder\
    .appName("WorkshopDataSetup")\
    .getOrCreate()

#-----------------------------------------------------------------
#               HELPER METHODS TO CREATE REQUIRED ADLS RESOURCES
#-----------------------------------------------------------------

def initialize_storage_account(storage_account_name, storage_account_key):
    try:
        global service_client

        service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
            "https", storage_account_name), credential=storage_account_key)

        print("Connection to ADLS Initialized")
        print('\n')
    except:
        print("Error During Connection Initialization")
        print('\n')
        print(e)

def create_file_system(file_system_name):
    try:
        global file_system_client

        file_system_client = service_client.create_file_system(file_system=file_system_name)
        print("File System Creation Successful")
        print('\n')
    except:
        print("File System Cretion Failed")
        print('\n')
        print(e)

def create_directory(directory_name):
    try:
        file_system_client.create_directory(directory_name)
        print("ADLS Directory Creation Successful")
        print('\n')
    except:
        print("ADLS Directory Creation Failed")
        print('\n')
        print(e)

def session(ADLS_ACCOUNT_NAME):

    storage = 'abfs://{}.dfs.core.windows.net'.format(ADLS_ACCOUNT_NAME)
    spark = SparkSession\
        .builder\
        .appName("PythonSQL")\
        .config("spark.kubernetes.access.hadoopFileSystems", storage)\
        .getOrCreate()

    return spark

def read_df_from_resource(spark, file_name):
    try:
        csvDF = spark.read.options(header = 'True', delimiter=',', inferSchema='True').csv("/app/mount/"+file_name)
        print("DF read successfully from /app/mount")
        print('\n')
        return csvDF
    except Exception as e:
        print(f'caught {type(e)}: e')
        print('\n')

def write_to_cloud_storage(spark, csvDF, storage, file_name):
    try:
        csvDF.write.options(header = 'True', sep=',', inferSchema='True').mode("overwrite").csv("{0}/{1}".format(storage, file_name))
        print("DF written successfully to Cloud Storage {}".format(storage))
        print('\n')
        csvDF.show()
    except Exception as e:
        print(f'caught {type(e)}: e')
        print("DF NOT written successfully to Cloud Storage {}".format(storage))
        print('\n')

def list_directory_contents(file_system_name, directory_name):
    try:

        file_system_client = service_client.get_file_system_client(file_system=file_system_name)

        paths = file_system_client.get_paths(path=directory_name)
        print("PRINTING DIRECTORY {} CONTENTS".format(directory_name))
        for path in paths:
            print(path.name + '\n')

    except Exception as e:
         print(e)
         print("UNABLE TO PREVIEW Cloud Storage {}".format(storage))
         print('\n')

#----------------------------------------------------------------
#               CDE JOB ARGS
#----------------------------------------------------------------

## YOUR ADLS INFO HERE
ADLS_ACCOUNT_NAME = storage = sys.argv[1]
ADLS_STORAGE_ACCOUNT_KEY = storage = sys.argv[2]
FILE_SYSTEM_NAME = storage = sys.argv[3]
DIRECTORY_NAME = storage = sys.argv[4]

#-----------------------------------------------------------------
#               UPLOADING FILE TO ADLS
#-----------------------------------------------------------------

## Not all steps are required
## If you run this script multiple times the file system and directory steps will be skipped

def main(ADLS_ACCOUNT_NAME, ADLS_STORAGE_ACCOUNT_KEY, FILE_SYSTEM_NAME, DIRECTORY_NAME):

    initialize_storage_account(ADLS_ACCOUNT_NAME, ADLS_STORAGE_ACCOUNT_KEY)
    create_file_system(FILE_SYSTEM_NAME)
    create_directory(DIRECTORY_NAME)

    spark = session(ADLS_ACCOUNT_NAME)
    storage = 'abfs://{}.dfs.core.windows.net'.format(ADLS_ACCOUNT_NAME)

    data_files = os.listdir("/app/mount")

    for file in data_files:
        csvDF = read_df_from_resource(spark, file)
        write_to_cloud_storage(spark, csvDF, storage, file_name)

if __name__ == "__main__":
    main(ADLS_ACCOUNT_NAME, ADLS_STORAGE_ACCOUNT_KEY, FILE_SYSTEM_NAME, DIRECTORY_NAME)
