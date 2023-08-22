# Introduction to the Hands On Labs

This guide provides instructions for setting up the project in your local machine and a brief introduction to the main concepts related to the Cloudera Data Engineering Service.

## Recommendations Before you Start

Throughout the labs, this guide will instruct you to make minor edits to some of the scripts. Please be prepared to make changes in an editor and re-upload them to the same CDE File Resource after each change. Having all scripts open at all times in an editor such as Atom is highly recommended.

Your Cloudera ACE Workshop Lead will load the required datasets to Cloud Storage ahead of the workshop. If you are reproducing these labs on your own, ensure you have placed all the contents of the data folder in a Cloud Storage path of your choice.

Each user will be assigned a username and cloud storage path. Each script will read your credentials from "parameters.conf" which you will have placed in your CDE File Resource. Before you start the labs, open the "parameters.conf" located in the "resources_files" folder and edit all three fields with values provided by your Cloudera ACE Workshop Lead. If you are reproducing these labs on your own you will also have to ensure that these values reflect the Cloud Storage path where you loaded the data.

## Requirements

In order to execute the Hands On Labs you need:
* A Spark 3 and Iceberg-enabled CDE Virtual Cluster (Azure, AWS and Private Cloud ok).
* Very few code changes are required but familiarity with Python and PySpark is highly recommended.
* Bonus Lab 1 requires a Hive CDW Virtual Warehouse. This lab is optional.

## Project Setup

Clone this GitHub repository to your local machine or the VM where you will be running the script.

```
mkdir ~/Documents/cde_ace_hol
cd ~/Documents/cde_ace_hol
git clone https://github.com/pdefusco/CDE119_ACE_WORKSHOP.git
```

Alternatively, if you don't have `git` installed on your machine, create a folder on your local computer; navigate to [this URL](https://github.com/pdefusco/CDE119_ACE_WORKSHOP.git) and manually download the files.

## Index

* In Part 1 you will develop four Spark Jobs using the CDE UI, the CDE CLI and CDE Interactive Sessions. One of the Jobs will focus on Apache Iceberg.
* In Part 2 you will create an Airflow Pipeline to orchestrate multiple Spark Jobs.
* In Part 3 you will use the CDE Spark Migration tool to convert Spark Jobs into CDE Spark Jobs.
* In Part 4 you will be able to explore a variety of topics in more detail including the CDE CLI, Airflow, and the CDE API.