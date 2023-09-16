# Introduction

This guide provides instructions for setting up the project in your local machine and a brief introduction to the main concepts related to the Cloudera Data Engineering Service.

## Requirements

In order to execute the Hands On Labs you need:

* A Spark 3 and Iceberg-enabled CDE Virtual Cluster (Azure, AWS and Private Cloud ok).

* Very few code changes are required but familiarity with Python and PySpark is highly recommended.

* Bonus Lab 1 requires a Hive CDW Virtual Warehouse. This lab is optional.

* A working installation of the CDE CLI. For this you have two options: installing the CLI with the provided steps or using Docker. More details are provided below in the CDE CLI Setup section.

## Recommendations Before you Start

Throughout the labs, this guide will instruct you to make minor edits to some of the scripts. Please be prepared to make changes in an editor and re-upload them to the same CDE File Resource after each change. Having all scripts open at all times in an editor such as Atom is highly recommended.

Your Cloudera Workshop Lead will load the required datasets to Cloud Storage ahead of the workshop. If you are reproducing these labs on your own, ensure you have placed all the contents of the data folder in a Cloud Storage path of your choice.

Each user will be assigned a username and cloud storage path. Each script will read your credentials from "parameters.conf" which you will have placed in your CDE File Resource. Before you start the labs, open the "parameters.conf" located in the "resources_files" folder and edit all three fields with values provided by your Cloudera ACE Workshop Lead. If you are reproducing these labs on your own you will have to ensure that these values reflect the Cloud Storage path where you loaded the data.

## Project Download

Clone this GitHub repository to your local machine or the VM where you will be running the script.

```
mkdir ~/Documents/cde_ace_hol
cd ~/Documents/cde_ace_hol
git clone https://github.com/pdefusco/CDE119_ACE_WORKSHOP.git
```

Alternatively, if you don't have `git` installed on your machine, create a folder on your local computer; navigate to [this URL](https://github.com/pdefusco/CDE119_ACE_WORKSHOP.git) and manually download the files.

## CDP User & Credentials

This HOL uses a parameters.conf file to store the necessary credentials. Each user is asked to enter their Workload Username at line 4 and Datalake paths at lines 2 and 3. The Workload Password is automatically inherited at the CDP Environment level and does not be set.

If you are participating in a Cloudera Event your Workshop Lead will provide you with the above credentials. The data will already have been uplaoded by your Workshop Lead.
If you are reproducing the labs in your CDE Environment without the help of a Cloudera Lead you will have to upload the data to an arbitrary Cloud path and obtain your Workload User from your CDP Admin.

## CDE CLI Setup

Throughout the labs you will be using the CDE CLI. To set up the CLI you have two options: using the provided Docker container or manually installing it in your local machine.
*We highly recommend using the provided Docker container* as the configuration is much simpler.

#### Configuring the CLI with the Provided Docker Container

In order to use the provided Docker container first pull with the following command:

```docker pull pauldefusco/cde_cli_workshop_1_19:latest```

Next run the container. The following command starts and logs you into the running container:

```docker run -it pauldefusco/cde_cli_workshop_1_19:latest```

To configure the CLI open the "config.yaml" file and add your credentials:

```vi ~/.cde/config.yaml ```

* user: this will be provided to you by your Cloudera Workshop Lead. If you are working in your company's CDP Environment you can obtain your CDP Workload User from the CDP Management Console or by asking your CDP Administrator.

* vcluster-endpoint: the JOBS API URL provided in the Cluster Details page. This can be accessed from the Administration tab and by clicking on the Cluster Details icon for your Virtual Cluster.

![alt text](../../img/cde_virtual_cluster_details.png)

Test the CLI by running the following command. If your cluster is new no job runs may be found, but the output will help you ensure that you can connect to the cluster.

```cde run list```

#### Installing the CLI in your Local Machine

To manually install the CLI in your local machine follow the steps below:

Step 1: Download the CLI Client:

    * Navigate to the Cloudera Data Engineering Overview page by clicking the Data Engineering tile in the Cloudera Data Platform (CDP) management console.
    * In the CDE web console, select an environment.
    * Click the Cluster Details icon for the virtual cluster you want to access.
    * Click the link under CLI TOOL to download the CLI client.
    * Change the permissions on the downloaded cde file to make it executable:

Step 2: Determine the Virtual Cluster Endpoint URL:

    * Navigate to the Cloudera Data Engineering Overview page.
    * In the Environments column, select the environment containing the virtual cluster you want to access using the CLI.
    * In the Virtual Clusters column on the right, click the Cluster Details icon for the virtual cluster you want to access.
    * Click JOBS API URL to copy the URL to your clipboard.

Step 3: On the host with the CLI client, create or edit the configuration file at ```~/.cde/config.yaml```. You can create multiple profiles in the ```~/.cde/config.yaml``` file and can be used while running commands.

Step 4: In the configuration file, specify the CDP user and virtual cluster endpoint as follows. The CDP user is your workload username:

```
user: <CDP_user>
vcluster-endpoint: <CDE_virtual_cluster_endpoint>
```

Step 5: Save the configuration file. If you have not done so already, make sure that the cde file is executable by running ```chmod +x /path/to/cde```. Test the CLI by running the following command. If your cluster is new no job runs may be found, but the output will help you ensure that you can connect to the cluster.

```cde run list```

For further information on the CLI please visit the [CDE Documentation](https://docs.cloudera.com/data-engineering/cloud/cli-access/topics/cde-cli.html)


## Index

* [Part 1](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part01_cde_architecture.md#cde-architecture) provides an introduction to the Architecture of the CDE Service. You will learn about the main components of CDE including the Environment, the Virtual Cluster, and more.
* In [Part 2](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part02_spark.md#part-2-developing-spark-jobs-in-cde) you will develop and deploy four Spark Jobs using the CDE UI, the CDE CLI and CDE Interactive Sessions. One of the Jobs will focus on Apache Iceberg.
* In [Part 3](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part03_airflow.md#part-3-orchestrating-pipelines-with-airflow) you will create an Airflow Pipeline to orchestrate multiple Spark Jobs.
* In [Part 4](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part04_spark_migration_tool.md#part-4-using-the-cde-spark-migration-tool-to-convert-spark-submits-to-cde-spark-submits) you will use the CDE Spark Migration tool to convert Spark Jobs into CDE Spark Jobs.
* In [Part 5](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part05_bonus_labs.md#part-5-bonus-labs) you will be able to explore a variety of topics in more detail including the CDE CLI, Airflow, and the CDE API.
* [Part 6](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part06_next_steps.md#conclusions-and-next-steps) provides a summary and a few related projects. If you are using or evaluating CDE today, please make sure to visit this page to learn about related projects.
