from datetime import datetime
from airflow.models import DAG
from airflow.operators.python import PythonOperator

DEFAULT_DATE = datetime(2016, 1, 1)

default_args = {
    "owner": "airflow",
    "start_date": DEFAULT_DATE,
}

def hello_world():
    print("hellow World")

    
with DAG(dag_id="test_dag_with_no_tags", default_args=default_args, schedule_interval='@once') as dag:
    task_a = PythonOperator(
        task_id="test_task_a",
        python_callable=hello_world
    )
