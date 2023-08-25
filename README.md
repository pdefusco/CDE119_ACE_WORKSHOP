# CDE 1.19 ACE Workshop Hands-On-Lab

## About the Hands On Lab Workshops

The Hands-On Lab (HOL) Workshops are an initiative by Cloudera Solutions Engineering aimed at familiarizing CDP users with each Data Service. The content consists of a series of guides and exercises to quickly implement sample end-to-end use cases in the realm of Machine Learning, Datawarehousing, Data Engineering, Data Streaming and Operational Database.

The HOL is typically a three-hour event organized by Cloudera for CDP customers and prospects, where a small technical team from Cloudera Solutions Engineering provides cloud infrastructure for participants and guides them through the completion of the guides with the help of presentations and discussions.

The HOL contained in this GitHub repository is dedicated to Cloudera Data Engineering 1.19, the CDP Data Service for data engineering commonly known for Spark and Airflow use cases in Private and Public Clouds.

The content is primarily designed for developers, cloud administrators and big data software architects. However, little to no code changes are typically required and non-technical stakeholders such as project managers and analysts are encouraged to actively participate.

HOL events are open to all CDP users and customers. If you would like to host an event with your colleagues please contact your local Cloudera Representative or submit your information [through this portal](https://www.cloudera.com/contact-sales.html). Finally, if you have access to a CDE Virtual Cluster you are welcome to use this guide and go through the same concepts in your own time.

## Objective

CDE is the Cloudera Data Engineering Service, a containerized managed service for Cloudera Data Platform designed for Large Scale Batch Pipelines with Spark, Airflow and Iceberg. It allows you to submit batch jobs to auto-scaling virtual clusters. As a serverless service, CDE enables you to spend more time on your applications, and less time on infrastructure.

CDE allows you to create, manage, and schedule Apache Spark jobs without the overhead of creating and maintaining Spark clusters. With CDE, you define virtual clusters with a range of CPU and memory resources, and the cluster scales up and down as needed to run your Spark workloads, helping to control your cloud costs.

This Hands On Lab is designed to walk you through the Services's main capabilities. Throughout the exercises you will:

1. Deploy an Ingestion, Transformation and Reporting pipeline with Spark 3.2.
2. Learn about Iceberg's most popular features.
3. Orchestrate pipelines with Airflow.
4. Use the CDE CLI to execute Spark Submits and more from your local machine.
5. Use the CDE Spark Submit Migration Tool to automatically convert a Spark Submit to a CDE Spark Submit.

Throughout these labs, you are going to deploy an ELT (Extract, Load, Transform) data pipeline that extracts data stored on AWS S3 object storage, loads it into the Cloudera Data Lakehouse and transforms it for reporting purposes.

```mermaid
graph LR
    D1[/Raw Data Files/]
    D2[(Cloudera Data Lakehouse)]
    style D1 fill:#fff,stroke:#bbb
    style D2 fill:#fff,stroke:#bbb

    subgraph Ingest
    direction TB
    A(01_Ingest)
    A -. Extract .-> D1
    A -. Load .-> D2
    end    

    subgraph Transform
    B(02_Sales_Transform_Iceberg)
    B -- Data Quality Checks & Reporting --> C(03_Sales_Report)
    B-- Join Transformed Tables --> D(04_Motors_Enrich)
    end

    Ingest -- Iceberg Conversion --> B
```

The Sales_Report job will give us an aggregate overview of our sales by model and customer types:

```
GROUP TOTAL SALES BY MODEL
+-------+--------------------+
|  Model|total_sales_by_model|
+-------+--------------------+
|Model C|        136557721.36|
|Model D|        162208438.10|
|Model R|        201420946.00|
+-------+--------------------+

GROUP TOTAL SALES BY GENDER
+------+---------------------+
|Gender|total_sales_by_gender|
+------+---------------------+
|     F|         258522496.93|
|     M|         241664608.53|
+------+---------------------+
````

## Step by Step Instructions

Detailed instructions are provided in the [step_by_step_guides](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/) folder.

* [English Guide](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english)
* [Guia en Espanol](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espanol)
* [Guida in Italiano](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/italiano)
