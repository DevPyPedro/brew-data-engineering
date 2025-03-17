from airflow.providers.amazon.aws.hooks.s3 import S3Hook #type: ignore
from airflow.exceptions import AirflowException  # type: ignore # Importa a exceção do Airflow
import logging

def upload_file_s3() -> None:
    """
    Esta função tem como objetivo fazer o upload de um arquivo para o S3 usando o boto3, que é uma biblioteca da AWS. 

    Como funciona:
    1. Conecta-se à AWS usando o hook configurado com as credenciais especificadas (no caso, 'aws_pedro').
    2. Cria um cliente do S3 que será usado para interagir com o serviço de armazenamento da AWS.
    3. Define o nome do bucket e a chave (caminho) onde o arquivo será armazenado no S3.
    4. Envia o arquivo para o S3 usando o método `upload_file`, passando o caminho local do arquivo, o nome do bucket e a chave no S3.

    Caso algum erro aconteça, a função vai levantar uma exceção do Airflow e marcar a DAG como falhada.

    Exemplo de uso:
    upload_file_s3()
    """
    try:
        s3_client = S3Hook(aws_conn_id='aws_pedro')

        bucket_name = 'datalakepedro'
        s3_key = 'datalake/bronze/brew_dados.json'
        local_path = 'dags/brew/temp/brew_dados.json'
        
        # Fazendo o upload do arquivo para o S3
        s3_client.load_file(local_path, s3_key, bucket_name, replace=True)

        logging.info(f"Arquivo {local_path} enviado com sucesso")

    except Exception as e:
        raise AirflowException(f'Ocorreu um erro ao tentar enviar o arquivo para o S3: {str(e)}')
