### Base stage
FROM python:3.7-slim AS base-stage

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    BASE_DIR=/app

RUN adduser --no-create-home --disabled-password --home /app --shell /bin/ash app
WORKDIR /app

COPY docker/entrypoint*.sh /
COPY verzekeringen_api/manage.py ./
COPY verzekeringen_api/apps ./apps

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
        default-libmysqlclient-dev

RUN pip install "poetry==${POETRY_VERSION}"

COPY pyproject.toml poetry.lock* ./

### Development stage
FROM preparation-stage AS development-stage

RUN poetry config virtualenvs.create false
RUN poetry install

CMD ["--no-migrate"]
