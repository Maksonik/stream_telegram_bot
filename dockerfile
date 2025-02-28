FROM --platform=linux/amd64 python:3.12-alpine AS builder

RUN true \
    && apk --no-cache add \
            chromium \
            chromium-chromedriver
            gcc \
            musl-dev \
            libffi-dev \
            bash \
            nano \
            vim \
    && true

RUN true \
    && python3 -m venv /venv \
    && . /venv/bin/activate \
    && python3 -m pip install --no-cache-dir -U pip \
    && python3 -m pip install --no-cache-dir -U poetry==1.8.2 poetry-plugin-export \
    && poetry config warnings.export false \
    && true

ENV PATH=/venv/bin:$PATH \
    VIRTUAL_ENV=/venv

COPY pyproject.toml poetry.lock /tmp/

RUN true \
    && cd /tmp \
    && poetry export --only=main --format requirements.txt --output requirements.txt \
    && rm pyproject.toml poetry.lock \
    && python3 -m pip install --no-cache-dir -U -r requirements.txt \
    && rm requirements.txt \
    && true

ENV CODE_DIR=/code

COPY . $CODE_DIR/

WORKDIR $CODE_DIR

ARG APP_VERSION="0.1.0"
ENV APP_VERSION=$APP_VERSION