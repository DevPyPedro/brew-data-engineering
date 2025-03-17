from airflow.providers.amazon.aws.hooks.s3 import S3Hook  # type:ignore
from airflow.exceptions import AirflowException  # type:ignore
import pandas as pd # type:ignore
import logging
import io

def transform_data_silver():
    """
    Esta função pega um arquivo JSON da camada Bronze no S3, processa os dados separando por estado
    e salva os resultados na camada Silver, também no S3, em formato Parquet.
    
    O fluxo é o seguinte:
    1. Baixamos o JSON do S3 e transformamos em um DataFrame do Pandas.
    2. Separamos os dados por estado.
    3. Salvamos cada conjunto de dados em formato Parquet.
    4. Enviamos os arquivos Parquet para a camada Silver no S3.
    
    Se algo der errado, levantamos uma exceção para que o Airflow capture o erro.
    """
    try:
        s3_hook = S3Hook(aws_conn_id='aws_pedro')
        
        s3_key = 'datalake/bronze/brew_dados.json'
        bucket_name = 'datalakepedro'

        file_content = s3_hook.read_key(key=s3_key, bucket_name=bucket_name)
        
        # Transformamos o JSON em um DataFrame do Pandas para facilitar a manipulação
        data = pd.read_json(io.StringIO(file_content))
        

        for state in data['state'].unique():
            data_state = data[data['state'] == state]

            # Criamos um buffer de memória para armazenar o arquivo Parquet
            csv_buffer = io.BytesIO()
            data_state.to_parquet(csv_buffer, index=False, engine='pyarrow', compression='snappy')
            
            output_key = f'datalake/silver/{state}_brew_dados.csv'
            
            # Enviamos o arquivo Parquet para o S3
            s3_hook.load_bytes(
                bytes_data=csv_buffer.getvalue(),  # Pegando os bytes do arquivo
                key=output_key,
                bucket_name=bucket_name,
                replace=True  # Se já existir um arquivo com esse nome, ele será substituído
            )
            logging.info('Tranformação concluida com sucesso')
    except Exception as e:
        raise AirflowException(f'Ocorreu um erro ao processar os dados: {str(e)}')


def transform_data_gold():
    try:
        s3_hook = S3Hook(aws_conn_id='aws_pedro')

        # Lista os arquivos no S3 a partir do prefixo especificado
        file_names = s3_hook.list_keys(bucket_name='datalakepedro', prefix='datalake/silver/')
        logging.info(f"Arquivos encontrados no bucket: {file_names}")

        if not file_names:
            raise AirflowException("Nenhum arquivo encontrado no prefixo especificado.")

        for file in file_names[1:]:  # Ignorando o primeiro arquivo (por exemplo, um diretório ou arquivo temporário)
            bucket_name = 'datalakepedro'
            
            # Baixa o arquivo como binário usando o método get_key
            file_content = s3_hook.get_key(key=file, bucket_name=bucket_name).get()['Body'].read()

            # Lê o arquivo Parquet a partir dos bytes usando io.BytesIO
            data = pd.read_parquet(io.BytesIO(file_content))

            # Filtra as colunas necessárias
            df_filter_columns = data[['id', 'name', 'city', 'brewery_type']]
            
            # Agrupando e agregando os dados conforme necessário
            df_resultado = (
                df_filter_columns
                .groupby(['city', 'brewery_type'])
                .agg({'brewery_type': 'count'})
                .rename(columns={'brewery_type': 'total_cervejarias'})
                .reset_index()
            )

            # Cria um buffer de memória para armazenar o arquivo Parquet
            parquet_buffer = io.BytesIO()
            df_resultado.to_parquet(parquet_buffer, index=False, engine='pyarrow', compression='snappy')

            # Define o caminho de saída com a extensão correta
            output_key = f'datalake/gold/{data['state_province'].iloc[0]}_brew_dados_agregados.parquet'

            # Envia o arquivo Parquet para o S3
            s3_hook.load_bytes(
                bytes_data=parquet_buffer.getvalue(),
                key=output_key,
                bucket_name=bucket_name,
                replace=True  # Se já existir um arquivo com esse nome, ele será substituído
            )

    except Exception as e:
        logging.error(f'Ocorreu um erro ao processar os dados: {str(e)}')
        raise AirflowException(f'Ocorreu um erro ao processar os dados: {str(e)}')

