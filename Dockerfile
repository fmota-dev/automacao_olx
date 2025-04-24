FROM python:3.12-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    curl build-essential libglib2.0-0 libnss3 libgconf-2-4 \
    libxss1 libappindicator1 libasound2 fonts-liberation \
    libatk-bridge2.0-0 libgtk-3-0 ca-certificates \
    chromium chromium-driver git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Instala o Poetry
ENV POETRY_VERSION=1.8.2
RUN curl -sSL https://install.python-poetry.org | python3 - 

# Adiciona o path do Poetry
ENV PATH="/root/.local/bin:$PATH"

# Cria diretório de trabalho
WORKDIR /app

# Clona o repositório do GitHub
RUN git clone https://github.com/fmota-dev/automacao_olx.git /app

# Copia os arquivos do seu projeto para o container
COPY pyproject.toml . 
COPY README.md . 
COPY app.py . 
COPY src ./src

# Configura o Poetry para não usar ambiente virtual
RUN poetry config virtualenvs.create false

# Instala dependências diretamente no ambiente global
RUN poetry install --no-root --no-interaction

# Define variáveis de ambiente
ENV SCRAPY_SETTINGS_MODULE=etl_olx.settings

# Garantir que o Scrapy esteja no PATH global
ENV PATH="/app/.venv/bin:$PATH"

# Comando padrão para rodar o app
CMD ["python", "app.py"]
