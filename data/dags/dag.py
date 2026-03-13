import sys
sys.path.append("/opt/airflow/dags")

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
from data.bronze.staging import create_bronze_tables


def my_task():
    print("Hello from Airflow task!")
    return "Task complete"


with DAG(
    dag_id="etl_pipeline",        
    start_date=datetime(2026, 1, 1),  
    schedule="* * * * *",           
) as dag:

    task1 = PythonOperator(
        task_id="print_hello_task",
        python_callable=my_task
    )

    task2 = PythonOperator(
        task_id = "create_bronze_table",
        python_callable = create_bronze_tables
    )

    task1 >> task2