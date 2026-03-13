import sys
sys.path.insert(0, '/opt/airflow')
#sys.path.insert(0, '/opt/airflow/dags/etl')
#sys.path.insert(0, '/opt/airflow/dags/data/bronze')
import os 
from dotenv import load_dotenv
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
#from airflow.providers.postgres.sensors.postgres import PostgresTableSensor

load_dotenv()


def my_task():
    print("Hello from Airflow task!")
    return "Task complete"

#BRONZE LAYER
def create_bronze_table_task():
    from data.bronze.staging import create_bronze_table
    create_bronze_table()

def load_bronze_table_task():
    from data.bronze.load import load_bronze_table
    load_bronze_table()

#SILVER LAYER
def etl_silver():
    from data.silver.load import load
    load()

#GOLD LAYER
def create_gold_tables():
    from data.gold.load_models import load_models
    load_models()

def load_dim_drivers():
    from data.gold.load_data import load_dim_drivers
    load_dim_drivers()

def load_dim_constructors():
    from data.gold.load_data import load_dim_constructors
    load_dim_constructors()

def load_dim_circuits():
    from data.gold.load_data import load_dim_circuits
    load_dim_circuits()

def load_dim_races():
    from data.gold.load_data import load_dim_races
    load_dim_races()

def load_dim_date():
    from data.gold.load_data import load_dim_date
    load_dim_date()

def load_fact_results():
    from data.gold.load_data import load_fact_results
    load_fact_results()

def load_fact_pit_stops():
    from data.gold.load_data import load_fact_pit_stops
    load_fact_pit_stops()

def load_fact_lap_times():
    from data.gold.load_data import load_fact_lap_times
    load_fact_lap_times()

with DAG(
    dag_id="etl_pipeline",        
    start_date=datetime(2026, 1, 1),  
    schedule="*/30 * * * *",           
) as dag:
    

    task1 = PythonOperator(
        task_id="create_bronze_tables_task",
        python_callable=create_bronze_table_task
    )

    task2 = PythonOperator(
        task_id="load_bronze_table",
        python_callable=load_bronze_table_task
    )

    task3 = PythonOperator(
        task_id = "etl_silver",
        python_callable = etl_silver
    )

    task4 = PythonOperator(
        task_id="create_gold_tables",
        python_callable=create_gold_tables
    )

    task5 = PythonOperator(
        task_id="load_dim_drivers",
        python_callable=load_dim_drivers
    )

    task6 = PythonOperator(
        task_id="load_dim_constructors",
        python_callable=load_dim_constructors
    )

    task7 = PythonOperator(
        task_id="load_dim_circuits",
        python_callable=load_dim_circuits
    )

    task8 = PythonOperator(
        task_id="load_dim_races",
        python_callable=load_dim_races
    )

    task9 = PythonOperator(
        task_id="load_dim_date",
        python_callable=load_dim_date
    )

    task10 = PythonOperator(
        task_id="load_fact_results",
        python_callable=load_fact_results
    )

    task11 = PythonOperator(
        task_id="load_fact_pit_stops",
        python_callable=load_fact_pit_stops
    )

    task12 = PythonOperator(
        task_id="load_fact_lap_times",
        python_callable=load_fact_lap_times
    )


# wait_for_bronze_table = PostgresTableSensor(
#     task_id="wait_for_bronze_table",
#     postgres_conn_id="my_postgres_conn",
#     table="formula1_staging",
#     schema="bronze"
# )

task1 >> task2 >> task3 >> task4

task4 >> task5 >> task6 >> task7 >> task8

task8 >> task9 >> task10 >> task11 >> task12

