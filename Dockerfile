FROM python:3.10-slim

RUN mkdir /fastapi_chat
WORKDIR /fastapi_chat

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_NO_INTERACTION=1

COPY pyproject.toml poetry.lock /fastapi_chat/

RUN poetry install --no-root --no-dev

COPY . .
