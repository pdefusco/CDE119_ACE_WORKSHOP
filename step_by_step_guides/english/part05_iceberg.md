# Part 5: Apache Iceberg

## Table of Contents

* [Use Case: Orchestrate a Spark-Iceberg Pipeline with Airflow]()
* [Iceberg Concepts](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part04_airflow.md#airflow-concepts)
  * [Schema Evolution]()
  * [Partition Evolution]()
  * [Hidden Partitioning]()
  * [Time Travel]()
  * [Cloudera Open Lakehouse]()
* [Lab: Deploy and Orchestrate a Spark-Iceberg Pipeline with Airflow](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part04_airflow.md#deploying-orchestration-pipeline-with-airflow)
* [Summary](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part04_airflow.md#summary)

## Use Case: Orchestrate a Spark-Iceberg Pipeline with Airflow

In part 2 you created your first CDE batch Spark Jobs while in part 3 you orchestrated a Spark pipeline with Airflow. In this section we will build a similar workflow leveraging Spark and Airflow, but with data stored in Iceberg tables.

Iceberg is an open table format format for huge analytic datasets. It provides features that, coupled with Spark as the compute engine, allows you to build data processing pipelines with dramatic gains in terms of data processing and reporting capabilities, and overall developer productivity.

CDE Provides native Iceberg support by automatically loading all Iceberg dependencies on all CDE Spark Jobs. In the following labs you will build a Spark Job to migrate data from Spark tables to Iceberg and leverage the Iceberg Merge Into, rather than a simple join, to process and load large fresh data batches with reduce Spark application code complexity.

Then, you will build a second Spark job in order to build an incremental report between different data batches leveraging Iceberg Time Travel. Along the way you will learn about Iceberg Architecture and experiment first-hand with Iceberg Metadata, Partition and Schema evolution.

Finally, you will use Airflow to schedule the two Spark Jobs.  

## Iceberg Concepts

Apache Iceberg is an open table format for huge analytic datasets. Iceberg adds tables to compute engines including Spark, Trino, PrestoDB, Flink, Hive and Impala using a high-performance table format that works just like a SQL table.

#### Schema Evolution

Iceberg supports in-place table evolution. You can evolve a table schema just like SQL – even in nested structures – or change partition layout when data volume changes. Iceberg does not require costly distractions, like rewriting table data or migrating to a new table.

For example, Hive table partitioning cannot change so moving from a daily partition layout to an hourly partition layout requires a new table. And because queries are dependent on partitions, queries must be rewritten for the new table. In some cases, even changes as simple as renaming a column are either not supported, or can cause data correctness problems.

Schema evolution supports add, drop, update, or rename, and has no side-effects

#### Partition Evolution

Evolving a partition means changing it without rewriting data files. Iceberg table partitioning can be updated in an existing table because queries do not reference partition values directly.

When you evolve a partition spec, the old data written with an earlier spec remains unchanged. New data is written using the new spec in a new layout. Metadata for each of the partition versions is kept separately. Because of this, when you start writing queries, you get split planning. This is where each partition layout plans files separately using the filter it derives for that specific partition layout.

#### Hidden Partitioning

Hidden partitioning prevents user mistakes that cause silently incorrect results or extremely slow queries. Iceberg uses hidden partitioning, so you don’t need to write queries for a specific partition layout to be fast. Instead, you can write queries that select the data you need, and Iceberg automatically prunes out files that don’t contain matching data.

#### Time Travel

Time travel queries can be time-based or based on a snapshot ID. In the event of a problem with your table, you can reset a table to a good state as long as the snapshot of the good table is available. You can roll back the table data based on a snapshot id or a timestamp.

When you modify an Iceberg table, a new snapshot of the earlier version of the table is created. When you roll back a table to a snapshot, a new snapshot is created. The creation date of the new snapshot is based on the Timezone of your session. The snapshot id does not change.

Iceberg generates a snapshot when you create, or modify, a table. A snapshot stores the state of a table. You can specify which snapshot you want to read, and then view the data at that timestamp.

#### Cloudera Open Lakehouse

Cloudera’s data lakehouse powered by Apache Iceberg is 100% open—open source, open standards based, with wide community adoption. It can store multiple data formats and enables multiple engines to work on the same data. Cloudera offers the same data services with full portability on all clouds.

The Iceberg tables in CDP integrate within the SDX, allowing for unified security, fine-grained policies, governance, lineage and metadata management across multiple clouds, so you can focus on analyzing your data while we take care of the rest.

## Deploy an Iceberg Use Case with Spark and Airflow in CDE

In this section you will revist your Spark and Airflow Pipeline by adding Iceberg capabilities to your workflow. The pipeline will consist of three Spark-Iceberg jobs and one Airflow job for orchestration.

#### Iceberg Migration Job

In this job you will migrate two Spark tables to Iceberg table format. The code in this script is very straightforward and consists of two basic routines to complete the migration:

```
spark.sql("ALTER TABLE DB_NAME.TABLE_NAME UNSET TBLPROPERTIES ('TRANSLATED_TO_EXTERNAL')"
spark.sql("CALL spark_catalog.system.migrate('DB_NAME.TABLE_NAME')"
```

Once the tables are migrated you can query their History and Snapshots tables in order to gain useful insights on Iceberg metadata:

```
spark.read.format("iceberg").load("spark_catalog.DB_NAME.TABLE_NAME.history").show(20, False)
spark.read.format("iceberg").load("spark_catalog.DB_NAME.TABLE_NAME.snapshots").show(20, False)
```

#### Iceberg ETL Job

This job consists of an Iceberg ETL pipeline.

#### Iceberg Report Job

This job consists of an Iceberg report.

#### Deploy the Pipeline

Create the job (without running it) from the UI or CLI using the following command. Replace username with your username:

```
cde resource create --name iceberg_pipeline_pauldefusco

cde resource upload --name iceberg_pipeline_pauldefusco \
                    --local-path cde_spark_jobs/05_PySpark_Iceberg_Migration.py \
                    --local-path cde_spark_jobs/05_PySpark_Iceberg_ETL.py \
                    --local-path cde_spark_jobs/05_PySpark_Iceberg_Incremental_Report.py \
                    --local-path resources_files/parameters.conf

cde job create --name IcebergMigration-pauldefusco \
               --type spark \
               --mount-1-resource iceberg_pipeline_pauldefusco \
               --application-file 05_PySpark_Iceberg_Migration.py

cde job create --name IcebergETL-pauldefusco \
               --type spark \
               --mount-1-resource iceberg_pipeline_pauldefusco \
               --application-file 05_PySpark_Iceberg_ETL.py

cde job create --name IcebergReport-pauldefusco \
               --type spark \
               --mount-1-resource iceberg_pipeline_pauldefusco \
               --application-file 05_PySpark_Iceberg_Incremental_Report.py
```

Open the Airflow DAG "cde_airflow_jobs/05-Airflow-Dag-Iceberg.py" and update the start_date field with the current timestamp at line 61.

```
start_date= datetime(2023,12,9,0), #Enter your current date minus one day i.e. if you are running this on Dec 10, enter (2023,12,9,0)
```

Now create and run the Airflow Job:

```
cde resource upload --name iceberg_pipeline_pauldefusco \
                    --local-path cde_airflow_jobs/05-Airflow-Dag-Iceberg.py

cde job create --name IcebergPipeline-pauldefusco \
               --type airflow \
               --dag-file 05-Airflow-Dag-Iceberg.py \
               --mount-1-resource iceberg_pipeline_pauldefusco

cde job run --name IcebergPipeline-pauldefusco

# Optional: Update Airflow Job if necessary:

cde resource upload --name iceberg_pipeline_pauldefusco \
                    --local-path cde_airflow_jobs/05-Airflow-Dag-Iceberg.py

cde job update --name IcebergPipeline-pauldefusco --dag-file 05-Airflow-Dag-Iceberg.py
```

### Creating a CDE Spark Job with Apache Iceberg

In this final section of Part 2 you will finish by deploying a CDE Job of type Spark in the CDE UI using PySpark script "02_PySpark_Iceberg.py".

The script includes a lot of Iceberg-related code. Open it in your editor of choice and familiarize yourself with the code. In particular, notice:

* Lines 62-69: The SparkSession must be launched with the Iceberg Catalog. However, no Jars need to be referenced. These are already available as Iceberg is enabled at the CDE Virtual Cluster level. The Iceberg Catalog tracks table metadata.     

```
spark = SparkSession \
    .builder \
    .appName("ICEBERG LOAD") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.iceberg.spark.SparkSessionCatalog")\
    .config("spark.sql.catalog.spark_catalog.type", "hive")\
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")\
    .config("spark.yarn.access.hadoopFileSystems", data_lake_name)\
    .getOrCreate()
```

* Lines 82 - 98: You can migrate a Spark Table to Iceberg format with the "ALTER TABLE" and "CALL" SQL statements as shown below.

```
spark.sql("ALTER TABLE CDE_WORKSHOP.CAR_SALES_{} UNSET TBLPROPERTIES ('TRANSLATED_TO_EXTERNAL')".format(username))

spark.sql("CALL spark_catalog.system.migrate('CDE_WORKSHOP.CAR_SALES_{}')".format(username))

```

* Lines 125-126: Iceberg allows you to query Table metadata including history of changes and table snapshots.

```
spark.read.format("iceberg").load("spark_catalog.CDE_WORKSHOP.CAR_SALES_{}.history".format(username)).show(20, False)

spark.read.format("iceberg").load("spark_catalog.CDE_WORKSHOP.CAR_SALES_{}.snapshots".format(username)).show(20, False)
```

* Lines 146 and 150: You can create/update/append Iceberg tables from a Spark Dataframe via the Iceberg Dataframe API "writeTo" command.
At line 146 we append the Dataframe to the pre-existing table.
At line 150 we create a new Iceberg table from the Spark Dataframe.

```
temp_df.writeTo("spark_catalog.CDE_WORKSHOP.CAR_SALES_{}".format(username)).append()

temp_df.writeTo("spark_catalog.CDE_WORKSHOP.CAR_SALES_SAMPLE_{}".format(username)).create()
```

* Line 171: You can query tables as of a particular timestamp or snapshot. In this case we use the timestamp. This information is available in the history and snapshots table we queries at lines 125-126. The metadata tables are updated in real time as tables are modified.

```
df = spark.read.option("as-of-timestamp", int(timestamp*1000)).format("iceberg").load("spark_catalog.CDE_WORKSHOP.CAR_SALES_{}".format(username))
```

* Lines 193-197: You can query Iceberg table by selecting only data that has changed between two points in time or two snapshots. This is referred to as an "Iceberg Incremental Read".

```
spark.read\
    .format("iceberg")\
    .option("start-snapshot-id", first_snapshot)\
    .option("end-snapshot-id", last_snapshot)\
    .load("spark_catalog.CDE_WORKSHOP.CAR_SALES_{}".format(username)).show()
```

* Lines 234-251: While Spark provides partitioning capabilities, once a partitioning strategy is chosen the only way to change it is by repartitioning or in other words recomputing all partitions.

Iceberg introduces Partition Evolution i.e. the ability to change the partitioning scheme on new data without modifying it on the initial dataset. Thanks to this tables are not recomputed. This is achieved by Iceberg's improved way of tracking table metadata in the Iceberg Metadata Layer.

In this example, the data present in the CAR_SALES table is initially partitioned by Month. As more data flows into our table, we decided that partitioning by Day provides Spark with better opportunities for job parallelism. Thus we simply change the partitioning scheme to Day. The old data is still partitioned by Month, while the new data added to the table from this point in time and onwards will be partitioned by Day.  

```
spark.sql("ALTER TABLE spark_catalog.CDE_WORKSHOP.CAR_SALES_{} REPLACE PARTITION FIELD month WITH day".format(username))
```

* Line 260: similarly to partition evolution, Spark does not allow you to change table schema without recreating the table. Iceberg allows you to more flexibily ADD and DROP table columns via the ALTER TABLE statement.

```
spark.sql("ALTER TABLE spark_catalog.CDE_WORKSHOP.CAR_SALES_{} DROP COLUMN VIN".format(username))
```

* Line 275: The MERGE INTO statement allows you to more easily compare data between tables and proceed with flexible updates based on intricate logic. In comparison, Spark table inserts and updates are rigid as the MERGE INTO statement is not allowed in Spark SQL.

```
ICEBERG_MERGE_INTO = "MERGE INTO spark_catalog.CDE_WORKSHOP.CAR_SALES_{0} t USING (SELECT CUSTOMER_ID, MODEL, SALEPRICE, DAY, MONTH, YEAR FROM CAR_SALES_TEMP_{0}) s ON t.customer_id = s.customer_id WHEN MATCHED THEN UPDATE SET * WHEN NOT MATCHED THEN INSERT *".format(username)

spark.sql(ICEBERG_MERGE_INTO)
```

Once you have finished going through the code, run the script as a CDE Spark Job from the CDE UI. Monitor outputs and results from the CDE Job Runs page.

To learn more about Iceberg in CDE please visit [Using Apache Iceberg in Cloudera Data Engineering](https://docs.cloudera.com/data-engineering/cloud/manage-jobs/topics/cde-using-iceberg.html).
