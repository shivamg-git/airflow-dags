from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

# A dictionary of default parameters to be used by all tasks in the DAG.
# https://airflow.apache.org/docs/apache-airflow/1.10.9/tutorial.html
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args= {
    "owner" : "spider",                 # Owner of all tasks
    'depends_on_past': False,           # depends_on_past (boolean) when set to True, keeps a task from getting triggered if the previous schedule for the task hasn’t succeeded.
    'start_date': days_ago(2),
    'email': ['gupta.shivamg.work@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}


with DAG(
    # https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/dag/index.html

    dag_id              = "dag_test",
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
        "hello":lambda name: 'Hello %s' % name,
        "Hi":lambda name: 'Hi %s' % name,
    },

    #  A dictionary of default parameters to be used as constructor keyword parameters when initialising operators
    default_args =  default_args
    




    ) as dag:

    bash_operator = BashOperator(
        task_id = "bash",
        bash_command="echo '{{ call | hello }}'",
        dag=dag
    )
    bash_operator