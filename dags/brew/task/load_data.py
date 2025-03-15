from airflow.providers.amazon.aws.hooks.base_aws import AwsBaseHook  # type: ignore
from airflow.exceptions import AirflowException  # type: ignore # Importa a exceção do Airflow

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
        aws_hook = AwsBaseHook(aws_conn_id='aws_pedro', client_type='s3')
        s3_client = aws_hook.get_client_type('s3')

        # Definindo o bucket e o caminho do arquivo no S3
        bucket_name = 'datalakepedro'
        s3_key = 'datalake/bronze/dados.parquet'
        local_path = 'tmp/dados.parquet'  # Caminho do arquivo local que será enviado
        
        # Fazendo o upload do arquivo para o S3
        s3_client.upload_file(local_path, bucket_name, s3_key)

        print(f"Arquivo {local_path} enviado com sucesso para o S3 no caminho {s3_key}.")

    except Exception as e:
        # Se ocorrer qualquer erro, o Airflow vai marcar a tarefa como falhada
        raise AirflowException(f'Ocorreu um erro ao tentar enviar o arquivo para o S3: {str(e)}')
