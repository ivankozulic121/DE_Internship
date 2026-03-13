import sys
sys.path.insert(0, '/opt/airflow')
#sys.path.insert(0, '/opt/airflow/dags/etl')
#sys.path.insert(0, '/opt/airflow/dags/data/bronze')
import os 
from dotenv import load_dotenv
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime

load_dotenv()


def my_task():
    print("Hello from Airflow task!")
    return "Task complete"

def create_bronze_tables_task():
    from data.bronze.staging import create_bronze_table
    create_bronze_table()

def load_bronze_tables_task():
    from data.bronze.load import load_bronze_table
    load_bronze_table()

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
        task_id="create_bronze_tables_task",
        python_callable=create_bronze_tables_task
    )

    task3 = PythonOperator(
        task_id="load_bronze_table",
        python_callable=load_bronze_tables_task
    )

    task1 >> task2 >> task3
