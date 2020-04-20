FROM python:latest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_CREATE 0

# Install system requirements
# RUN apk update \
#     && apk add \
#         # system & psutil dependencies
#         gcc musl-dev linux-headers jq \
#         # psycopg2 dependencies
#         postgresql-dev \
#         # Pillow dependencies
#         zlib-dev jpeg-dev \
#     && rm -Rf /var/cache/apk/*

WORKDIR /opt/app

RUN pip install poetry
COPY poetry.lock pyproject.toml /opt/app/

# to prevent poetry from installing my actual app,
# and keep docker able to cache layers
# RUN mkdir -p /app/src/app
# RUN touch /app/src/app/__init__.py

RUN poetry install --no-dev

CMD ["python", "camerasdjango/manage.py", "runserver"]
