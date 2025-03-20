# 🍺 brew-data-engineering

## 📌 Descrição
O **brew-data-engineering** é um pipeline de engenharia de dados que extrai informações da API [Open Brewery DB](https://www.openbrewerydb.org/), transforma os dados e os armazena em um Data Lake seguindo a arquitetura de medalhão (Bronze, Prata e Ouro). O objetivo é estruturar os dados de maneira eficiente para análise e consumo posterior.

## 🏗️ Arquitetura
O pipeline segue a arquitetura de dados em camadas:
- 🟤 **Bronze**: Dados brutos extraídos da API e armazenados no Data Lake (AWS S3).
- ⚪ **Prata**: Dados limpos e padronizados.
- 🟡 **Ouro**: Dados agregados e enriquecidos para análise.

## 🚀 Tecnologias Utilizadas
- 🐍 **Python**: Para desenvolvimento do pipeline de extração e transformação de dados.
- 🎈 **Apache Airflow**: Para orquestração do pipeline de dados.
- ☁️ **AWS S3**: Para armazenamento dos dados estruturados.
- 🐼 **Pandas**: Para manipulação e transformação dos dados.
- 🌍 **Requests**: Para extração dos dados da API.


## 🔧 Instalação e Configuração
1. Clone o repositório:
   ```sh
   git clone https://github.com/seu-usuario/brew-data-engineering.git
   cd brew-data-engineering
   ```

2. Crie e ative um ambiente virtual:
   ```sh
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows
   ```

3. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```

4. Configure suas credenciais da AWS para acesso ao S3.

5. Inicie o Apache Airflow:
   ```sh
   airflow standalone
   ```

## ▶️ Execução do Pipeline
1. Acesse a interface web do Airflow (http://localhost:8080) e ative a DAG do pipeline.
2. O pipeline extrairá os dados da API, transformará e armazenará no S3.
3. Os dados processados podem ser utilizados para análises e visualização.

## 🐳 Como Usar com Docker
Para rodar o projeto usando Docker, basta executar:
```sh
docker compose up -d
```
Isso iniciará todos os serviços necessários automaticamente.

Para visualizar os logs em tempo real:
```sh
docker compose logs -f
```

Para parar e remover os contêineres:
```sh
docker compose down
```

## 🤝 Contribuição
Sinta-se à vontade para abrir issues e pull requests para melhorias.

