# Part 4: Using the CDE Spark Migration Tool to Convert Spark Submits to CDE Spark Submits

## Objective

The spark-submit command is a utility to run or submit a Spark or PySpark application program (or job) to the cluster by specifying options and configurations, the application you are submitting can be written in Scala, Java, or Python (PySpark).

The CDE CLI provides a similar although not identical way of running "spark-submits" in CDE. However, adapting many spark-submita to CDE might become an obstacle in your migration. The Cloudera Engineering team created a Spark Migration tool to facilitate the conversion.

#### Step By Step Instructions

>**⚠ Warning**  
>The Spark Submit Migration tool requires having the CDE CLI installed on your machine. Please ensure you have completed the installation steps in Part 3.

>**⚠ Warning**  
>This tutorial utilizes Docker to streamline the installation process of the Spark Submit Migration tool. If you don't have Docker installed on your machine you will have to go through [this tutorial by Vish Rajagopalan](https://github.com/SuperEllipse/cde-spark-submit-migration) instead.

Navigate to the CDP Management Console and download your user credentials file. The credentials file includes a CDP Access Key ID and a CDP Private Key.

![alt text](../../img/mgt_console1.png)

![alt text](../../img/mgt_console2.png)

![alt text](../../img/mgt_console3.png)

![alt text](../../img/mgt_console4.png)

Next, navigate to the CDE Virtual Cluster Details and copy the JOBS_API_URL.

![alt text](../../img/jobsapiurl.png)

Launch the example Docker container.

```
docker run -it pauldefusco/cde_spark_submit_migration_tool:latest
```

You are now inside the running container. Next, activate the Spark Submit Migration tool by running the following shell command.

```
cde-env.sh activate -p vc-1
```

Navigate to the .cde folder and place the CDP Access Key ID and Private Key you downloaded earlier in the respective fields in the credentials file.

Next, open the config.yaml file located in the same folder. Replace the cdp console value at line 3 with the CDP Console URL (e.g. `https://console.us-west-1.cdp.cloudera.com/`).
Then, enter your JOBS_API_URL in the "vcluster-endpoint" field at line 8.

Finally, run the following spark-submit. This is a sample submit taken from a legacy CDH cluster.

```
spark-submit \
--master yarn \
--deploy-mode cluster \
--num-executors 2 \
--executor-cores 1 \
--executor-memory 2G \
--driver-memory 1G \
--driver-cores 1 \
--queue default \
06-pyspark-sql.py
```

Shortly you should get output in your terminal including a Job Run ID confirming successful job submission to CDE. In the screenshot example below the Job Run ID is 9.

![alt text](../../img/job_submit_confirm1.png)

Navigate to your CDE Virtual Cluster Job Runs page and validate the job is running or has run successfully.

![alt text](../../img/job_submit_confirm3.png)

>**⚠ Warning**  
>If you are unable to run the spark-submit you may have to remove the tls setting from config.yaml. In other words, completely erase line 4.

## Summary

The spark-submit is the single command used to submit a Spark Application to a cluster. The command provides with a wide variety of options and configurations for running the Application as a Job, for example the number and resources assigned to Spark Driver and Executors.

The CDE CLI provides a very similar command, the CDE spark-submit, which can be used to submit Spark Applications to CDE Virtual Clusters. The CDE Spark Submit Migration Tool was created to allow you to convert one or more spark-submit commands to CDE spark-submit. This requires a brief installation and is available to you from the Virtual Cluster Service Details page.

Congratulations for making it to the end of the core labs of this workshop! In [the next section](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part05_bonus_labs.md#part-5-bonus-labs) you can expand on CDE with four additional topics: a [more advanced CDE Airflow use case](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part05_bonus_labs.md#bonus-lab-1-cde-airflow-orchestration-in-depth); an [Airflow DAG leveraging the CDW Operator](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part05_bonus_labs.md#bonus-lab-2-using-cde-airflow-with-cdw) to orchestrate CDW queries from a CDE Airflow DAG; a more [in-depth view of the CDE CLI](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part05_bonus_labs.md#bonus-lab-3-using-the-cde-cli-to-streamline-cde-production-use-cases-in-depth); and a [Python Application to monitor multiple CDE clustwers leveraging the CDE API](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part05_bonus_labs.md#bonus-lab-4-using-python-with-the-cde-api).
