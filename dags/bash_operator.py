from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id              = "bash_operator",
    description         = "simple bash operator",

    # """https://crontab.guru/ => CRON Expression """
    # """https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dag-run.html => CRON PRESET"""
    # """timedelta eg. timedelta(minute=30)"""
    schedule            = "@continuous",
    
    # """The timestamp from which the scheduler will attempt to backfill"""
    start_date          = datetime.utcnow(), # datetime
    
    # A date beyond which your DAG won’t run, leave to None for open-ended scheduling
    end_date            = None, # datetime
    ) as dag:

    bash_operator = BashOperator(
        task_id = "bash",
        bash_command="echo 'Hello World'",
        dag=dag
    )
    bash_operator