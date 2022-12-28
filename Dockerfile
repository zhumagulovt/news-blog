FROM python:3.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install --no-dev --no-root

EXPOSE 8000
