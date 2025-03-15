from airflow.exceptions import AirflowException  # Importa a exceção do Airflow
import pandas as pd # type: ignore
import requests # type: ignore
import os

from brew.config.settings import api_url

def extract_data_api() -> None:
    """
    Esta função tem como objetivo pegar os dados de uma API, transformar esses dados em um formato que seja fácil de trabalhar (Parquet) e salvar no seu computador.

    Como funciona:
    1. A função faz uma solicitação (chamada GET) para a API que você configurou.
    2. Se a resposta não for boa (ou seja, o código de status da resposta não for 200), ela vai lançar um erro.
    3. Caso a resposta seja boa, os dados são convertidos para um DataFrame do pandas, que é uma forma organizada de visualizar e manipular os dados.
    4. A função então cria uma pasta no seu computador, se ela não existir, e salva os dados na forma de um arquivo Parquet, que é ótimo para armazenar dados tabulares de forma compacta e eficiente.

    Se algo der errado em qualquer uma dessas etapas, um erro será mostrado no console para você saber o que aconteceu.

    Não é retornado nenhum valor, mas você vai encontrar o arquivo com os dados na pasta `tmp/dados.parquet`.

    Exemplo de uso:
    Vamos supor que você quer rodar essa função para pegar os dados e salvar em arquivo:
    extract_data_api()
    """
    try:
        response = requests.get(api_url)

        if not response.status_code == 200:
            raise AirflowException(f'Erro ao conectar com a API. Status code: {response.status_code}')
        
        brew_data = pd.DataFrame(response.json())

        local_path = "tmp/dados.parquet"
        
        os.makedirs(local_path.split('/')[0], exist_ok=True)
        
        brew_data.to_parquet(local_path, engine="pyarrow", index=False)

    except Exception as e:
        raise AirflowException(f'Ocorreu um erro ao processar os dados: {str(e)}')
