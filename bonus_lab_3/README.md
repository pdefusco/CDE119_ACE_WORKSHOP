# CDE Alerter

## Objective

CDE is the Cloudera Data Engineering Service, a containerized managed service for Large Scale Batch Pipelines with Spark featuring Airflow and Iceberg.

The CDE Alerter is a Python script that can be used to monitor jobs in a CDE Virtual Cluster. It allows you to implement a set of rules to notify a set of recipients in case of a particular event. The Alerter relies on cde_python, a custom Python wrapper for the CDE API.

## Requirements

In order to use the script you need to have:
* A CDE Virtual Cluster (Azure, AWS and Private Cloud ok).
* A Virtual Machine or local computer that has the ability to reach the CDE Virtual Cluster where your CDE Jobs are running.
* Python 3.6 or above.
* A gmail account with 2-step authentication and an App password.
* No script code changes are required.

## Instructions

#### Step 0: Project setup

Clone this GitHub repository to your local machine or the VM where you will be running the script.

```
mkdir ~/Documents/CDE_Alerter
cd ~/Documents/CDE_Alerter
git clone https://github.com/pdefusco/CDE_Alerter.git
```

Alternatively, if you don't have GitHub create a folder on your local computer; navigate to [this URL](https://github.com/pdefusco/CDE_Alerter.git) and download the files.

#### Step 1: Create a Python Virtual Environment and Install Requirements

Although a Python Virtual Environment is optional, it is highly recommended. To create one and install requirements execute the following commands:

```
#Create
python3 -m venv venv

#Activate
source venv/bin/activate

#Install single package
pip install pandas #Optionally use pip3 install

#Install requirements
pip install -r requirements.txt #Optionally use pip3 install
```

![alt text](img/alerter_img01.png)


#### Step 2: Test CDE Connection

To test if your VM can reach the CDE Virtual Cluster, open your terminal and run the following command:

```
python3 connection_tester.py jobs_api_url cdpusername cdppassword
```

The output in the terminal should confirm that a test resource has been created successfully.


#### Step 3: Run the script

Before you can run the script you will need:
* The CDE JOBS API URL for the intended CDE Virtual Cluster you want to monitor.
* The Gmail APP password (not just the account login password). If you need help setting this up for the first time:
  1. Recommended: [Create a New Gmail Account](https://support.google.com/mail/answer/56256?hl=en)
  2. [Enable 2-step Authentication and Create an App Password](https://www.youtube.com/watch?v=hXiPshHn9Pw)
* The CDP User and Password you will authenticate into the CDE Virtual Cluster with.

To run the script, run the following python command in the directory where you cloned your project.

```
python3 alerter.py https://z4xgdztf.cde-6fr6l74r.go01-dem.ylcu-atmi.cloudera.site/dex/api/v1 cdpusername cdppwdhere mysecregapppwdhere 1800 me@myco.com mycolleague@myco.com
```

The Gmail App password should be entered as the fourth argument (for example replacing "mysecregapppwdhere" above).

The script will automatically detect whether more than 1800 seconds (30 minutes) have expired between the start and end time of any of your CDE Jobs.

If any CDE Jobs meet the criteria, the script will automatically send a notification to the provided emails. You can enter two email recipients by adding them as the last two arguments at script execution.

As an example, if we lower the time window from 1800 seconds to 18 seconds the script will detect some jobs and output the following to the terminal.

![alt text](img/alerter_img_02A.png)

If no CDE Jobs meet the criteria, nothing is done.

![alt text](img/alerter_img02.png)


#### Step 4: Schedule the Script as a Cron Job

The script can run as often as you would like. For example, you could schedule a cron job to execute the script every minute with the following command:

```
* * * * * /usr/bin/python ~/path/to/proj/cde_alerter/alerter.py
```


## Conclusions & Next Steps

CDE is the Cloudera Data Engineering Service, a containerized managed service for Spark and Airflow. With Python, CDE users can interact with their Virtual Clusters by means of Requests based on the CDE API and build applications for use cases including ML Ops, Web Apps, and many more.

In this tutorial we triggered an email to select recipients if a certain wait time is above threshold. This pattern can be used more broadly as an integration point between CDE Jobs and 3rd party orchestration systems.

If you are exploring CDE you may find the following tutorials relevant:

* [Spark 3 & Iceberg](https://github.com/pdefusco/Spark3_Iceberg_CML): A quick intro of Time Travel Capabilities with Spark 3.

* [Simple Intro to the CDE CLI](https://github.com/pdefusco/CDE_CLI_Simple): An introduction to the CDE CLI for the CDE beginner.

* [CDE CLI Demo](https://github.com/pdefusco/CDE_CLI_demo): A more advanced CDE CLI reference with additional details for the CDE user who wants to move beyond the basics.

* [CDE Resource 2 ADLS](https://github.com/pdefusco/CDEResource2ADLS): An example integration between ADLS and CDE Resource. This pattern is applicable to AWS S3 as well and can be used to pass execution scripts, dependencies, and virtually any file from CDE to 3rd party systems and viceversa.

* [Using CDE Airflow](https://github.com/pdefusco/Using_CDE_Airflow): A guide to Airflow in CDE including examples to integrate with 3rd party systems via Airflow Operators such as BashOperator, HttpOperator, PythonOperator, and more.

* [GitLab2CDE](https://github.com/pdefusco/Gitlab2CDE): a CI/CD pipeline to orchestrate Cross-Cluster Workflows for Hybrid/Multicloud Data Engineering.

* [CML2CDE](https://github.com/pdefusco/cml2cde_api_example): an API to create and orchestrate CDE Jobs from any Python based environment including CML. Relevant for ML Ops or any Python Users who want to leverage the power of Spark in CDE via Python requests.

* [Postman2CDE](https://github.com/pdefusco/Postman2CDE): An example of the Postman API to bootstrap CDE Services with the CDE API.

* [Oozie2CDEAirflow API](https://github.com/pdefusco/Oozie2CDE_Migration): An API to programmatically convert Oozie workflows and dependencies into CDE Airflow and CDE Jobs. This API is designed to easily migrate from Oozie to CDE Airflow and not just Open Source Airflow.

For more information on the Cloudera Data Platform and its form factors please visit [this site](https://docs.cloudera.com/).

For more information on migrating Spark jobs to CDE, please reference [this guide](https://docs.cloudera.com/cdp-private-cloud-upgrade/latest/cdppvc-data-migration-spark/topics/cdp-migration-spark-cdp-cde.html). 

If you have any questions about CML or would like to see a demo, please reach out to your Cloudera Account Team or send a message [through this portal](https://www.cloudera.com/contact-sales.html) and we will be in contact with you soon.

