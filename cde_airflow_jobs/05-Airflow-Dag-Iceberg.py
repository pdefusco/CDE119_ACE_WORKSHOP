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

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import BranchPythonOperator
from cloudera.cdp.airflow.operators.cde_operator import CDEJobRunOperator
from airflow.utils.trigger_rule import TriggerRule

username = "pauldefusco"

with DAG(
    dag_id='iceberg_dag',
    default_args={
        'depends_on_past': False,
        'retry_delay': timedelta(seconds=5),
        'schedule_interval':'*/5 * * * *',
        #'end_date': datetime(2024,9,30,8)
    },
    description='Dag with initial setup task that only runs on start_date',
    #start_date=datetime(2023, 12, 10),
    # Runs daily at 1 am
    #schedule_interval='0 1 * * *',
    # catchup must be true if start_date is before datetime.now()
    start_date= datetime(2023,12,10,0),
    catchup=False,
    max_active_runs=1,
    is_paused_upon_creation=False
) as dag:

    def branch_fn(**kwargs):
        # Have to make sure start_date will equal data_interval_start on first run
        # This dag is daily but since the schedule_interval is set to 1 am data_interval_start would be
        # 2000-01-01 01:00:00 when it needs to be
        # 2000-01-01 00:00:00
        date = kwargs['data_interval_start'].replace(hour=0, minute=0, second=0, microsecond=0)
        #date = context.get("execution_date")
        print("THE EXECUTION DATE IS")
        print(date)
        print("THE START DATE IS")
        print(dag.start_date)
        if date == dag.start_date:
            return 'migrate_to_iceberg'
        else:
            return 'skip_initial_task'

    start = DummyOperator(
        task_id="start"
    )

    branch_task = BranchPythonOperator(
        task_id='branch_task',
        python_callable=branch_fn,
        provide_context=True
    )

    iceberg_migration = CDEJobRunOperator(
        task_id="migrate_to_iceberg",
        job_name="IcebergMigration-"+username
    )

    skip_initial_task = DummyOperator(
        task_id="skip_initial_task"
    )

    iceberg_etl = CDEJobRunOperator(
          task_id='iceberg_etl',
          job_name='IcebergETL-'+username, #job_name needs to match the name assigned to the Spark CDE Job in the CDE UI
          trigger_rule=TriggerRule.ONE_SUCCESS
    )

    iceberg_report = CDEJobRunOperator(
        task_id='iceberg_report',
        job_name='IcebergReport-'+username #job_name needs to match the name assigned to the Spark CDE Job in the CDE UI
    )

    end = DummyOperator(
        task_id="end"
    )

    start >> branch_task >> [skip_initial_task, iceberg_migration] >> iceberg_etl >> iceberg_report >> end
