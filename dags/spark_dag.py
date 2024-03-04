from airflow import DAG
from airflow.decorators import task
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta 
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator

dag_owner = 'Spider'

default_args = {'owner': dag_owner,
        'depends_on_past': False,
        'retries': 100,
        'retry_delay': timedelta(seconds=20)
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

parallel_task = []
for i in range(1):
    taskX = KubernetesPodOperator(
        task_id=f"{i}_operator",
        dag=dag,
        kubernetes_conn_id="local_k8_connection",
        namespace="airflow",
        image="docker.io/library/python:latest",
        cmds=["sh","-c"],
        arguments=["sleep 60"],
        get_logs=True,
        deferrable=True
    )
    parallel_task.append(taskX)

end = EmptyOperator(task_id='end', dag=dag)

for i in range(1):
    start >> parallel_task[i] >> end        