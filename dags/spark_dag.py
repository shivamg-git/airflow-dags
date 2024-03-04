from airflow import DAG
from airflow.decorators import task
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta 

dag_owner = 'Spider'

default_args = {'owner': dag_owner,
        'depends_on_past': False,
        'retries': 100,
        'retry_delay': timedelta(minutes=5)
        }

dag = DAG(dag_id='test_k8_retries',
        default_args=default_args,
        description='',
        start_date=datetime.utcnow(),
        schedule_interval='@hourly',
        catchup=False,
        tags=['']
    )

start = EmptyOperator(task_id='start', dag=dag)

for i in range(100):
    EmptyOperator(
        task_id=f"{i}_operator",
        dag=dag
    )

end = EmptyOperator(task_id='end', dag=dag)

for i in range(100):
    start >> f"{i}_operator" >> end        