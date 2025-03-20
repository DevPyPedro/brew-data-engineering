"""
DAG para processamento de dados de cervejarias
========================================================

Esta DAG realiza um pipeline de ETL para processar dados de cervejarias. 
O processo inclui:
1. Extração dos dados de uma API
2. Upload dos dados brutos para o Amazon S3 (Bronze Layer)
3. Transformação dos dados para a camada Silver
4. Transformação dos dados para a camada Gold

Execução:
- Agendamento: Diário (`@daily`)
- Data de início: 11 de dezembro de 2024
- Fuso horário: America/Sao_Paulo
- Tolerância para reexecução: 1 tentativa com delay de 1 minuto
- Tempo limite para execução de cada tarefa: 23 horas
"""

from airflow.operators.python import PythonOperator #type: ignore
from airflow import DAG #type: ignore
import pendulum #type: ignore 

# Importação das funções responsáveis por cada etapa do ETL
from brew.task.transform_data import transform_data_silver, transform_data_gold
from brew.task.extract_data import extract_data_api
from brew.task.load_data import upload_file_s3

# Parâmetros padrões da DAG
default_args = {
    "retries": 1,  # Número de tentativas em caso de falha
    "retry_delay": pendulum.duration(minutes=1),  # Tempo entre as tentativas
    "execution_timeout": pendulum.duration(hours=23),  # Tempo máximo de execução da tarefa
}

# Definição da DAG
with DAG(
    "breweries_case",  # Nome da DAG
    default_args=default_args,
    description="Tem o objetivo de extrair, tratar os dados e carregar particionados para um bucket",
    schedule_interval="@daily",  # Agendamento diário
    start_date=pendulum.datetime(2024, 12, 11, tz="America/Sao_Paulo"),  # Data de início da DAG
    max_active_runs=1,  # Evita execuções concorrentes da DAG
    catchup=False  # Evita execução retroativa para datas passadas
) as dag:
    
    # Tarefa 1: Extração dos dados da API
    extract_info_api = PythonOperator(
        task_id='extract_info_api',
        python_callable=extract_data_api,  # Função de extração
    )

    # Tarefa 2: Upload dos dados extraídos para o S3 (Bronze Layer)
    upload_file_bronze = PythonOperator(
        task_id='upload_file_bronze',
        python_callable=upload_file_s3,  # Função de upload para o S3
    )

    # Tarefa 3: Transformar os dados na camada Silver
    transform_for_silver = PythonOperator(
        task_id='transform_for_silver',
        python_callable=transform_data_silver,  # Função de transformação para Silver
    )

    # Tarefa 4: Transformar os dados na camada Gold
    transform_for_gold = PythonOperator(
        task_id='transform_for_gold',
        python_callable=transform_data_gold,  # Função de transformação para Gold
    )

    # Definição da ordem de execução das tarefas
    extract_info_api >> upload_file_bronze >> transform_for_silver >> transform_for_gold