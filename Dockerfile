FROM python:3.10-slim-buster AS base

ARG UID=1000
ARG GID=1000

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    RUN_USER=bank_app \
    RUN_GROUP=bank_app \
    APP_DIR=/opt/bank_app

ENV PATH="/home/${RUN_USER}/.local/bin:${PATH}"
ENV PYTHONPATH="/opt/bank-app/:{$PYTHONPATH}"
ENV PYTHONPATH="/opt/bank-app/src/:{$PYTHONPATH}"

RUN apt-get update && apt install -y build-essential libpq-dev postgresql-client netcat libmagic1

RUN groupadd -g ${GID} -o ${RUN_GROUP} \
    && useradd -m -u ${UID} -g ${GID} -o ${RUN_USER} \
    && mkdir -p ${APP_DIR} \
    && chmod -R 775 ${APP_DIR} \
    && chown ${UID}:${GID} ${APP_DIR}

RUN python -m pip install --upgrade pip

COPY --chown=${RUN_USER}:${RUN_GROUP} . ${APP_DIR}

WORKDIR ${APP_DIR}/src

FROM base AS prod

USER ${RUN_USER}:${RUN_GROUP}

RUN pip install pipenv==2020.11.15 --no-cache-dir --user \
    && pipenv install --system --deploy --ignore-pipfile


FROM base AS dev

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget curl vim htop bash gettext \
    && apt-get clean

USER ${RUN_USER}:${RUN_GROUP}

RUN pip install pipenv==2020.11.15 --no-cache-dir --user \
    && pipenv install --system --deploy --ignore-pipfile --dev

ENTRYPOINT ["sh", "/opt/bank_app/docker-entrypoint.sh"]
