FROM python:3.12-slim

WORKDIR /app

# Copia os arquivos de dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos do projeto
COPY . .

# Expõe a porta internamente
EXPOSE 8501

# Comando padrão de inicialização
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]