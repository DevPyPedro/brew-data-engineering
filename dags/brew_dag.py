'''
DAG para cervejas
========================================================'
'''
from airflow.operators.python import PythonOperator#type: ignore
from airflow import DAG #type: ignore
import pendulum #type: ignore 

from brew.task.transform_data import transform_data_silver, transform_data_gold
from brew.task.extract_data import extract_data_api
from brew.task.load_data import upload_file_s3

default_args = {
    "retries":1,
    "retry_delay": pendulum.duration(minutes=1),
    "execution_timeout": pendulum.duration(hours=23), 
}

with DAG(
    "breweries_case",
    default_args=default_args,
    description="Tem o objetivo de extrair, tratar os dados e carregar particionados para um bucket",
    schedule_interval="@daily",
    start_date=pendulum.datetime(2024, 12, 11, tz="America/Sao_Paulo"),
    max_active_runs=1,
    catchup=False
) as dag:
     

    extract_info_api = PythonOperator(
        task_id='extract_info_api',
        python_callable=extract_data_api, 
    )

    upload_file_bronze = PythonOperator(
        task_id='upload_file_bronze',
        python_callable=upload_file_s3, 
    )

    transform_for_silver = PythonOperator(
        task_id='transform_for_silver',
        python_callable=transform_data_silver, 
    )

    transform_for_gold = PythonOperator(
        task_id='transform_for_gold',
        python_callable=transform_data_gold, 
    )

    extract_info_api >> upload_file_bronze >> transform_for_silver >> transform_for_gold
