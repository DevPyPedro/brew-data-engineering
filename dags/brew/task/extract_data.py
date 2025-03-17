from airflow.exceptions import AirflowException # type: ignore
import requests # type: ignore
import logging
import os
import json


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
        response = requests.get("https://api.openbrewerydb.org/breweries")

        if not response.status_code == 200:
            raise AirflowException(f'Erro ao conectar com a API. Status code: {response.status_code}')
        
        brew_data = response.json()


        local_path = "dags/brew/temp/"
        
        os.makedirs(local_path, exist_ok=True)
        
        with open(os.path.join(local_path, 'brew_dados.json'), 'w')as file: json.dump(brew_data, file)

        logging.info('Extração feita com sucesso')

    except Exception as e:
        raise AirflowException(f'Ocorreu um erro ao processar os dados: {str(e)}')
