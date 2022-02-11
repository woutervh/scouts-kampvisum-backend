### Base stage
FROM python:3.9-slim AS base-stage

ENV PYTHONFAULTHANDLER=1 \
        PYTHONHASHSEED=random \
        PYTHONUNBUFFERED=1 \
        BASE_DIR=/app

RUN adduser --no-create-home --disabled-password --home /app --shell /bin/bash app
WORKDIR /app

COPY .env* ./
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
        POETRY_VERSION=1.1.7

RUN apt-get update; \
        apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        libffi-dev \
        python3-dev
RUN python -m pip install "poetry==${POETRY_VERSION}"
COPY pyproject.toml poetry.lock* ./

# # SSH
# ADD ./scripts/ssh/id_rsa /
# RUN chmod 600 /id_rsa
# RUN cp /etc/ssh/ssh_config /etc/ssh/ssh_config.backup
# RUN echo "    IdentityFile /id_rsa" >> /etc/ssh/ssh_config
# # Avoids the need to perform a ssh-keyscan on the repository
# RUN echo "    StrictHostKeyChecking no" >> /etc/ssh/ssh_config
# RUN git config --global user.email "boro@inuits.eu"
# RUN git config --global user.name "inuits"

### Development stage
FROM preparation-stage AS development-stage

RUN poetry config virtualenvs.create false
RUN poetry install

# # Cleanup SSH
# RUN rm -f /id_rsa
# RUN rm -f /etc/ssh/ssh_config
# RUN mv /etc/ssh/ssh_config.backup /etc/ssh/ssh_config
# RUN apt-get purge -y \
#         openssh-client \
#         git
# RUN apt-get autoremove -y

CMD ["--no-migrate"]



