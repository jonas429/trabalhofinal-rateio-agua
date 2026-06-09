# 💧 Sistema de Gestão e Rateio de Água

Este projeto foi desenvolvido como **Atividade Extensionista** para o curso de **Ciência da Computação**. Trata-se de uma aplicação web moderna voltada para a automação do cálculo de rateio igualitário de faturas de água de condomínios residenciais, com persistência de dados em ambiente conteinerizado.

## 🛠️ Tecnologias e Arquitetura

O sistema adota uma arquitetura baseada em microsserviços e portabilidade de infraestrutura, utilizando:
* **Frontend/Interface:** [Streamlit](https://streamlit.io/) (Interface Web interativa e responsiva em Python).
* **Processamento de Dados:** [Pandas](https://pandas.pydata.org/) (Modelagem matemática e exportação de relatórios customizados em formato `.csv` compatível com Excel).
* **Persistência de Dados:** [PostgreSQL](https://www.postgresql.org/) (Banco de dados relacional para auditoria de histórico).
* **Orquestração de Infraestrutura:** [Docker & Docker Compose](https://www.docker.com/) (Isolamento completo da stack de serviços e rede virtual interna).

---

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
* Docker Desktop instalado e configurado com suporte a WSL 2.

### Passo a Passo
1. Clone este repositório na sua máquina local:
   ```bash
     git clone [https://github.com/jonas429/trabalhofinal-rateio-agua.git](https://github.com/jonas429/trabalhofinal-rateio-agua.git)
 2. Navegue até a pasta do projeto:

    Bash
    cd trabalhofinal-rateio-agua

3. Suba a infraestrutura completa (Compilação do Python + Inicialização do PostgreSQL):

       Bash
       docker compose up -d --build

4. Acesse o sistema no seu navegador de preferência através do endereço:
http://localhost:8501

📈 Funcionalidades Desenvolvidas
[x] Formulário interativo para lançamento do valor da fatura e mês de competência.

[x] Integração automatizada com tabela de apartamentos via ORM SQLAlchemy.

[x] Upsert dinâmico para evitar duplicidade de registros de faturas no banco de dados.

[x] Tabela de visualização em tempo real do espelho do relatório.

[x] Exportação de relatório em lote via botão de download em CSV estruturado.
