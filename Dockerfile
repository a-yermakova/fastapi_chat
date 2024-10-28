# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем зависимости для PostgreSQL и других библиотек
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Устанавливаем переменные для Poetry
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_NO_INTERACTION=1

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы pyproject.toml и poetry.lock перед копированием всего проекта
# Это позволит установить зависимости отдельно и использовать кэш
COPY pyproject.toml poetry.lock /app/

# Устанавливаем зависимости с помощью Poetry
RUN poetry install --no-root --no-dev

# Копируем все остальные файлы проекта
COPY . .

# Устанавливаем Celery команду для запуска воркера по умолчанию
CMD ["poetry", "run", "celery", "-A", "src.worker.celery_app", "worker", "--loglevel=info"]
# Добавляем команду для запуска FastAPI-приложения с помощью Uvicorn
CMD ["poetry", "run", "gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "src.main:app", "--bind", "0.0.0.0:8000"]
