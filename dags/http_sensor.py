from airflow import DAG
from datetime import datetime
from airflow.providers.http.sensors.http import HttpSensor

with DAG(
    dag_id= "http_sensor",
    schedule_interval="@once",
    start_date=datetime.utcnow(),
    catchup=False

) as dag:
    
    http_sensor = HttpSensor(
        http_conn_id="rest_conn",
        method="GET",
        endpoint="/api/unknown/23",
        execution_timeout=20
    )