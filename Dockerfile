FROM python:3.10-slim

RUN mkdir /fastapi_chat

WORKDIR /fastapi_chat

RUN apt-get update && \
    apt-get install -y curl libpq-dev gcc nginx && \
    apt-get clean

RUN curl -sL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    apt-get clean

ENV PATH="/root/.local/bin:$PATH"

ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_NO_INTERACTION=1

COPY pyproject.toml poetry.lock /fastapi_chat/

RUN poetry install --no-root --no-dev

COPY . .

RUN chmod a+x *.sh

COPY nginx.conf /etc/nginx/conf.d/default.conf
