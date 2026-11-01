FROM python:3.12-slim

WORKDIR /app

# Instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código e os dados
COPY src/ ./src/
COPY dashboard/ ./dashboard/
COPY data/ ./data/

# Define os caminhos utilizados pelo pipeline
ENV LAKE_DIR=/app/lake \
    ENTRADA=/app/data/acidentes_2024_bruto.csv

# Executa o pipeline por padrão
CMD ["python", "-m", "src.pipeline"]