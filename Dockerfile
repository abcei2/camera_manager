FROM toolboc/jetson-nano-l4t-cuda-cudnn-opencv


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_CREATE 0

WORKDIR /opt/app

COPY InstallPackages.sh darknet/ poetry.lock pyproject.toml /opt/app/

RUN /bin/bash -c "source InstallPackages.sh"
RUN pip3 install poetry
RUN poetry install --no-dev
WORKDIR /opt/app/camerasdjango

