FROM python:3.11-slim

# Evitar outputs interativos
ENV PYTHONUNBUFFERED=1

# Instalar dependências do sistema necessárias para spaCy
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir uvicorn

COPY main.py .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
