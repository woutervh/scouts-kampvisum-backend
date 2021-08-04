### Base stage
FROM python:3.7-slim AS base-stage

ENV PYTHONFAULTHANDLER=1 \
        PYTHONHASHSEED=random \
        PYTHONUNBUFFERED=1 \
        BASE_DIR=/app

RUN adduser --no-create-home --disabled-password --home /app --shell /bin/bash app
WORKDIR /app

COPY docker/entrypoint*.sh /
COPY scouts_kampvisum_api/manage.py ./
COPY scouts_kampvisum_api/apps ./apps

ENTRYPOINT ["/entrypoint.sh"]

### Preparation stage
FROM base-stage AS preparation-stage

ARG APP_ENV

ENV APP_ENV=${APP_ENV} \
        PIP_DEFAULT_TIMEOUT=100 \
        PIP_DISABLE_PIP_VERSION_CHECK=1 \
        PIP_NO_CACHE_DIR=1 \
        POETRY_VERSION=1.1.4

RUN apt-get update; \
        apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        libffi-dev \
        python3-dev \
        default-libmysqlclient-dev \
        openssh-client \
        git
RUN pip install "poetry==${POETRY_VERSION}"
COPY pyproject.toml poetry.lock* ./

# SSH
RUN mkdir ~/.ssh
ADD ./scripts/ssh/id_rsa ~/.ssh/id_rsa

### Development stage
FROM preparation-stage AS development-stage

RUN poetry config virtualenvs.create false
RUN poetry install

CMD ["--no-migrate"]
