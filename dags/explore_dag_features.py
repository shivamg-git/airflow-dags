from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.models.param import Param

def custom_success_callback(context):
    print("Task has completed successfully!")
    print(repr(context))
    print(context['ds'])
    return True

def custom_failure_callback(context):
    print("Task has Failed!")
    print(repr(context))
    print(context['ds'])
    return True

def custom_retry_callback(context):
    print("Retrying Task!")
    print(repr(context))
    print(context['ds'])
    return True

def custom_sla_miss_callback(context):
    print("Task has Missed sla!")
    print(repr(context))
    print(context['ds'])
    return True

# A dictionary of default parameters to be used by all tasks in the DAG.
# https://airflow.apache.org/docs/apache-airflow/1.10.9/tutorial.html
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args= {
    "owner" : "spider",                 # Owner of all tasks
    'depends_on_past': False,           # depends_on_past (boolean) when set to True, keeps a task from getting triggered if the previous schedule for the task hasn’t succeeded.
    'start_date': days_ago(2),
    'email': ['gupta.shivamg.work@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
    'execution_timeout': timedelta(seconds=10),
    # https://marclamberti.com/blog/airflow-trigger-rules-all-you-need-to-know/
    # all_success, all_failed, all_done, one_failed, one_success, none_failed, none_skipped, none_failed_min_one_success, dummy
    'trigger_rule': 'all_success',
    'sla': timedelta(minutes=2),
    'on_failure_callback': custom_failure_callback,
    'on_success_callback': custom_success_callback,
    'on_retry_callback': custom_retry_callback,
    'sla_miss_callback': custom_sla_miss_callback,

    # Resource pool to use
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'wait_for_downstream': False,
    # 'queue': 'bash_queue'
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
    default_args =  default_args,

    # https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/params.html
    # a dictionary of DAG level parameters that are made accessible in templates, namespaced under params. These params can be overridden at the task level.
    params= {
        "x" : Param(5, type="integer", minimum=3),
        "y":"YYYY"
    }
    




    ) as dag:

    bash_operator = BashOperator(
        task_id = "bash",
        bash_command="exit 123",
        dag=dag
    )

    bash_operator2 = BashOperator(
        task_id = "bash2",
        bash_command="echo '{{call | Hi }}'",
        dag=dag
    )
    
    bash_operator3 = BashOperator(
        task_id = "bash3",
        bash_command="sleep 11",
        dag=dag
    )

    bash_operator4 = BashOperator(
        task_id = "bash4",
        bash_command="echo '{{ params.x }},{{ params.y}}'",
        dag=dag
    )
