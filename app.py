import os
import pandas as pd
from sqlalchemy import create_engine, text
import streamlit as st
import time

# 1. Configuração da página Web
st.set_page_config(page_title="Gestão de Água - Condomínio", layout="centered")

# 2. Configuração Dinâmica da ligação com o Banco de Dados
db_host = os.getenv("DB_HOST", "postgres_agua")
db_user = os.getenv("DB_USER", "admin")
db_pass = os.getenv("DB_PASSWORD", "senha_agua_123")
db_name = os.getenv("DB_NAME", "gestao_agua")

DB_URL = f"postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}"
engine = create_engine(DB_URL)

# 3. Função de Validação do Banco
def conectar_com_retry(max_tentativas=3, aguardo_segundos=2):
    for tentativa in range(1, max_tentativas + 1):
        try:
            with engine.connect() as conexao:
                conexao.execute(text("SELECT 1;"))
                return True
        except Exception:
            time.sleep(aguardo_segundos)
    return False

# 4. Interface Gráfica Web (Streamlit)
st.title("💧 Sistema de Rateio de Água")
st.subheader("Atividade Extensionista - Prestação de Contas")

# Formulário para introdução de dados pelo utilizador/síndico
with st.form("formulario_rateio"):
    st.write("Insira os dados da fatura recebida da concessionária:")
    
    conta_do_mes = st.number_input("Valor Total da Fatura (R$)", min_value=0.0, value=1050.00, step=50.0)
    mes_atual = st.text_input("Mês de Referência (Formato: AAAA-MM)", value="2026-06")
    
    botao_calcular = st.form_submit_button("Calcular e Salvar no Banco")

# Lógica executada quando o botão é clicado
if botao_calcular:
    if not conectar_com_retry():
        st.error("Erro técnico: Não foi possível estabelecer conexão com o banco de dados postgres_agua.")
    else:
        # Busca a quantidade real de apartamentos cadastrados no init.sql
        with engine.connect() as conexao:
            qtd_apartamentos = conexao.execute(text("SELECT COUNT(*) FROM apartamentos;")).scalar()

        if qtd_apartamentos == 0:
            st.warning("Atenção: Nenhum apartamento foi encontrado cadastrado na tabela.")
        else:
            # Cálculo matemático do rateio individual
            valor_por_unidade = round(conta_do_mes / qtd_apartamentos, 2)

            # Grava ou atualiza os dados da fatura no banco de dados para fins de auditoria
            query_salvar = text("""
                INSERT INTO faturas_mes (mes_referencia, valor_total, valor_por_unidade)
                VALUES (:mes, :total, :por_unidade)
                ON CONFLICT (mes_referencia) 
                DO UPDATE SET valor_total = :total, valor_por_unidade = :por_unidade;
            """)
            
            with engine.begin() as conexao:
                conexao.execute(query_salvar, {"mes": mes_atual, "total": conta_do_mes, "por_unidade": valor_por_unidade})

            # Gera o relatório completo cruzando com a estrutura física dos apartamentos
            df_apto = pd.read_sql("SELECT apartamento, andar FROM apartamentos ORDER BY andar, apartamento", engine)
            df_apto['mes_referencia'] = mes_atual
            df_apto['valor_individual'] = valor_por_unidade

            # Renderiza os blocos visuais de sucesso e métricas na página
            st.success(f"Rateio do mês {mes_atual} processado com sucesso!")
            
            col1, col2 = st.columns(2)
            col1.metric("Valor Total da Conta", f"R$ {conta_do_mes:.2f}")
            col2.metric("Valor por Apartamento", f"R$ {valor_por_unidade:.2f}")

            st.write("### Relatório de Divisão por Unidade:")
            st.dataframe(df_apto[['andar', 'apartamento', 'valor_individual']], use_container_width=True)

            # Cria o botão de download dinâmico para gerar o arquivo CSV na hora
            csv_data = df_apto.to_csv(index=False, sep=';', encoding='utf-8-sig')
            
            st.download_button(
                label="📥 Baixar Relatório para o Excel (.CSV)",
                data=csv_data,
                file_name=f"rateio_agua_{mes_atual}.csv",
                mime="text/csv"
            )