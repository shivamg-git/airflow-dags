from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
        dag_id              = "bash_operator",
        description         = "simple bash operator",
        schedule            = "@continuous",
        max_active_runs     = 1,
        start_date          = datetime.utcnow(), # datetime
        end_date            = None, # datetime
    ) as dag:

    bash_operator = BashOperator(
        task_id = "bash",
        bash_command="echo 'Hello World'",
        dag=dag
    )
    bash_operator