# Introduction

This page provides instructions for setting up the necessary data assets. Follow the steps below as a checklist to ensure you are good to go.

## Table of Contents

* [1. Requirements](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part00_setup.md#1-requirements)
* [2. Recommendations Before you Start](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part00_setup.md#2-recommendations-before-you-start)
* [3. Project Download](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part00_setup.md#3-project-download)
* [4. CDP User & Credentials](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part00_setup.md#4-cdp-user--credentials)
* [5. Jobs API URL]()
* [6. CDE CLI Setup]()
  * [6A. Configuring the CLI with the Provided Docker Container]()
  * [6B. Installing the CLI in your Local Machine]()
* [7. Connectivity Test]()
* [8. Data Upload to Cloud Storage]()
* [9. parameters.conf Configuration]()

* [Index](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part00_setup.md#index)

## 1. Requirements

In order to execute the Labs you need:

* A Spark 3, Iceberg-enabled, All-Purpose CDE Virtual Cluster. The CDE Service must be on version 1.19.3 (Azure, AWS and Private Cloud ok).

* Very few code changes are required but familiarity with Python and PySpark is highly recommended.

* Bonus Lab 2 requires a Hive CDW Virtual Warehouse. This lab is optional.

* A working installation of the CDE CLI. For this you have two options: pulling the provided Docker image or installing the CLI on your local machine. More details are provided below in step 7.

## 2. Recommendations Before you Start

This guide will instruct you to make minor edits to some of the scripts as you go along with the labs. Please be prepared to make changes in an editor and re-upload them to the same CDE File Resource after each change. Having all scripts open at all times in an editor such as Atom or Sublime Text is highly recommended.

## 3. Project Download

Clone this Git repository to your local machine.

```
mkdir ~/Documents/cde_ace_hol
cd ~/Documents/cde_ace_hol
git clone https://github.com/pdefusco/CDE119_ACE_WORKSHOP.git
```

Alternatively, if you don't have `git` installed on your machine, create a folder on your local computer; navigate to [this URL](https://github.com/pdefusco/CDE119_ACE_WORKSHOP.git) and manually download the files.

## 4. CDP User & Credentials

If you are participating in a Cloudera Event your Workshop Lead will provide you with the above credentials.

If you are reproducing the labs in your CDE Environment without the help of a Cloudera Lead you will have to upload the data to an arbitrary Cloud path and obtain your Workload User from your CDP Admin.

## 5. Jobs API URL

The Jobs API URL is the entry point to the cluster for the API and CLI. It will become necessary in the CDE CLI Setup and other parts of the labs.

Take note of your cluster's JOBS API URL by navigating to the Administration tab and by clicking on the Cluster Details icon for your Virtual Cluster.

![alt text](../../img/cde_virtual_cluster_details.png)

![alt text](../../img/jobsapiurl.png)

## 6. CDE CLI Setup

Throughout the labs you will be using the CDE CLI. To set up the CLI you have two options: using the provided Docker container or manually installing it in your local machine.

*We highly recommend using the provided Docker container* as the configuration is much simpler.

#### 6A. Configuring the CLI with the Provided Docker Container

In order to use the provided Docker container first pull with the following command:

```docker pull pauldefusco/cde_cli_hol_1193:latest```

Next run the container. The following command starts and logs you into the running container:

```docker run -it pauldefusco/cde_cli_hol_1193:latest```

To configure the CLI open the "config.yaml" file and add your credentials:

```vi ~/.cde/config.yaml ```

* user: this will be provided to you by your Cloudera Workshop Lead. If you are working in your company's CDP Environment you can obtain your CDP Workload User from the CDP Management Console or by asking your CDP Administrator.

* vcluster-endpoint: the JOBS API URL provided in the Cluster Details page.

Test the CLI by running the following command. If your cluster is new no job runs may be found, but the output will help you ensure that you can connect to the cluster.

```cde run list```

#### 6B. Installing the CLI in your Local Machine

To manually install the CLI in your local machine follow the steps below:

Step 1: Download the CLI Client:

    * Navigate to the Cloudera Data Engineering Overview page by clicking the Data Engineering tile in the Cloudera Data Platform (CDP) management console.
    * In the CDE web console, select an environment.
    * Click the Cluster Details icon for the virtual cluster you want to access.
    * Click the link under CLI TOOL to download the CLI client.
    * Change the permissions on the downloaded cde file to make it executable:

Step 2: On the host with the CLI client, create or edit the configuration file at ```~/.cde/config.yaml```. You can create multiple profiles in the ```~/.cde/config.yaml``` file and can be used while running commands.

Step 3: In the configuration file, specify the CDP user and virtual cluster endpoint as follows. The CDP user is your workload username:

```
user: <CDP_user>
vcluster-endpoint: <JOBS API URL>
```

Step 4: Save the configuration file. If you have not done so already, make sure that the cde file is executable by running ```chmod +x /path/to/cde```. Test the CLI by running the following command. If your cluster is new no job runs may be found, but the output will help you ensure that you can connect to the cluster.

```cde run list```

For further information on the CLI please visit the [CDE Documentation](https://docs.cloudera.com/data-engineering/cloud/cli-access/topics/cde-cli.html)

## 7. Connectivity Test

In this test you will run a simple CDE Job from the CLI and ensure that your CDP User is able to read and write data from Cloud Storage via Spark. Typically, if this test fails you haven't set up your CDP Workload User correctly in the CDP Management Console. This test requires Docker.

#### Step 1: Pull Docker Image and Run it locally

```docker pull pauldefusco/cde_cli_hol_1193```

```docker run -it pauldefusco/cde_cli_hol_1193```

You will be directly logged into the container as cdeuser. Run the next steps from the shell inside the running container: 

#### Step 2: Create a CDE Resource

```cde resource create --type files --name precheck_resource```

#### Step 3: Upload files to the Resource

```cde resource upload --local-path precheck/test_file.csv --name precheck_resource```
```cde resource upload --local-path precheck/cloud_precheck.py --name precheck_resource```

#### Step 4: Create a CDE Job and Run it

```cde job create --name precheck_job --type spark --application-file cloud_precheck.py --mount-1-resource precheck_resource```

Replace the --arg value with the ADLS/S3 location you intend to use for the workshop. If you don't know it you can obtain it from the CDP Management Console -> Data Lake tab or ask your CDP Administrator.

#e.g. AWS 's3a://go01-demo'
#e.g. Azure 'abfs://data@go01demoazure.dfs.core.windows.net'

```cde job run --name precheck_job --arg *abfs://data@go01demoazure.dfs.core.windows.net*```

Validate that the job is able to write and read data to Cloud Storage by checking the logs in the CDE UI.

#### Connectivity Test Troubleshooting

The connectivity test most commonly fails for the following reasons:

* IDBroker Mappings were not set correctly: go to the CDP Management Console -> Actions -> Manage Access -> IDBroker Mappings tab and ensure your user has been added to the group and then in the IDBroker Mapping section.

* Access Roles are not set correctly: go to the CDP Management Console -> Actions -> Manage Access -> Access tab and ensure your user has been given all CDE Roles.

* Unset Workload Password: go to the CDP Management Console -> Actions -> Manage Access -> Workload Password tab and ensure that you have created a Workload Password for your user.

## 8. Data Upload to Cloud Storage

Upload the data folder in a Cloud Storage location of your choice.

If you are attending a Public HOL event with infrastructure provided by Cloudera the data will already have been uplaoded by your Workshop Lead.

If you are reproducing these labs in your own CDE deployment ensure you have placed all the contents of the data folder in a Cloud Storage location of your choice.

## 9. parameters.conf Configuration

Each script will read your credentials from "parameters.conf". Instructions for uploading this in your CDE File Resource are provided in part 2.

Before you start the labs, open "parameters.conf" located in the "resources_files" folder and edit all three fields with values provided by your Cloudera ACE Workshop Lead.

If you are reproducing these labs on your own you will have to ensure that these values reflect the Cloud Storage path where you loaded the data.

## Index

* [Part 1](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part01_cde_architecture.md#cde-architecture) provides an introduction to the Architecture of the CDE Service. You will learn about the main components of CDE including the Environment, the Virtual Cluster, and more.
* In [Part 2](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part02_spark.md#part-2-developing-spark-jobs-in-cde) you will develop and deploy four Spark Jobs using the CDE UI, the CDE CLI and CDE Interactive Sessions. One of the Jobs will focus on Apache Iceberg.
* In [Part 3](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part03_airflow.md#part-3-orchestrating-pipelines-with-airflow) you will create an Airflow Pipeline to orchestrate multiple Spark Jobs.
* In [Part 4](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part04_spark_migration_tool.md#part-4-using-the-cde-spark-migration-tool-to-convert-spark-submits-to-cde-spark-submits) you will use the CDE Spark Migration tool to convert Spark Jobs into CDE Spark Jobs.
* In [Part 5](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part05_bonus_labs.md#part-5-bonus-labs) you will be able to explore a variety of topics in more detail including the CDE CLI, Airflow, and the CDE API.
* [Part 6](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part06_next_steps.md#conclusions-and-next-steps) provides a summary and a few related projects. If you are using or evaluating CDE today, please make sure to visit this page to learn about related projects.
