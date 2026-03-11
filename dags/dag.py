import sys
import os

# Add the parent directory of dags to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
from data.bronze.staging import create_bronze_tables


def my_task():
    print("Hello from Airflow task!")
    return "Task complete"

def create_bronze_tables_task():
    try:
        create_bronze_tables()
    except Exception as e:
        raise RuntimeError(f"Bronze table creation failed: {e}")


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
        task_id = "create_bronze_tables_task",
        python_callable = create_bronze_tables_task
    )

    task1 >> task2