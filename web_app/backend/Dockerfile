FROM python:3.11 as python-base

# https://python-poetry.org/docs#ci-recommendations
ENV POETRY_VERSION=1.7.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

FROM python-base as poetry-base

RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

FROM python-base as example-app

COPY --from=poetry-base ${POETRY_VENV} ${POETRY_VENV}

ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app

COPY poetry.lock pyproject.toml .
RUN poetry install

COPY . .

EXPOSE 8000
CMD [ "poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000" ]