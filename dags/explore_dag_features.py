from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    # https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/dag/index.html

    dag_id              = "bash_operator",
    description         = "simple bash operator",

    # """https://crontab.guru/ => CRON Expression """
    # """https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dag-run.html => CRON PRESET"""
    # """timedelta eg. timedelta(minute=30)"""
    schedule            = "@once",
    
    # """The timestamp from which the scheduler will attempt to backfill"""
    start_date          = datetime.utcnow(), # datetime
    
    # A date beyond which your DAG won’t run, leave to None for open-ended scheduling
    end_date            = None, # datetime

    # template_searchpath=""
    # template_undefined=""

    # a dictionary of macros that will be exposed in your jinja templates.
    user_defined_macros = {
        "call" : "Hello Spider"
    },

    # a dictionary of filters that will be exposed in your jinja templates.
    user_defined_filters = {

    }



    ) as dag:

    bash_operator = BashOperator(
        task_id = "bash",
        bash_command="echo '{{ call }}'",
        dag=dag
    )
    bash_operator