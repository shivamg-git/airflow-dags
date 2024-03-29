from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.http.sensors.http import HttpSensor

with DAG(
    dag_id= "http_sensor",
    schedule_interval=None,
    start_date=datetime.utcnow(),
    catchup=False

) as dag:
    
    http_sensor = HttpSensor(
        task_id="http_sensor_task",
        http_conn_id="rest_conn",
        method="GET",
        endpoint="/api/unknown/23",
        execution_timeout= timedelta(seconds=60),
        deferrable = True
    )