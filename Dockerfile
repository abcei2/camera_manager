FROM python:latest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_CREATE 0

WORKDIR /opt/app

RUN pip3 install poetry
RUN apt-get update
RUN apt-get install -y libgl1-mesa-glx

COPY poetry.lock pyproject.toml /opt/app/
RUN poetry install --no-dev
WORKDIR /opt/app/camerasdjango
