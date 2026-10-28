# Esqueleto de imagem. Ajuste à sua stack (Python/Java/Spark...).
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY data/ ./data/

# O contrato de pastas (lake/bronze|silver|quarentena|gold) é montado como volume.
ENV LAKE_DIR=/app/lake \
    ENTRADA=/app/data/acidentes_2024_bruto.csv

CMD ["python", "-m", "src.pipeline"]
