'''
DAG para cervejas
========================================================'
'''
from airflow import DAG #type: ignore
import pendulum #type: ignore 

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
) as dag: pass