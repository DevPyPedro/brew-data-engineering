from airflow.providers.amazon.aws.hooks.s3 import S3Hook  # type: ignore
from airflow.exceptions import AirflowException  # type: ignore # Importa a exceção do Airflow
import pandas as pd
from io import StringIO


def transform_data_bronze(r) -> pd.DataFrame:

    try:
        s3_hook = S3Hook(aws_conn_id='aws_pedro')
        s3_key = 'datalake/bronze/brew_dados.json'

        file_content = s3_hook.read_key(key=s3_key, bucket_name='datalakepedro')

        # Lê o conteúdo JSON diretamente para um DataFrame
        data = pd.DataFrame(StringIO(file_content))

        for state in data['state'].unique():
            data_state = data[data['state'].isin([state])]

        
    
    except Exception as e:
        raise AirflowException(f'Ocorreu um erro ao processar os dados: {str(e)}')

