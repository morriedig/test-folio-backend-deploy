# Section 1- Base Image
FROM python:3.8-slim AS development_build

# Section 2- Python Interpreter Flags
ARG DJANGO_ENV
ENV DJANGO_ENV=${DJANGO_ENV} \
	# python:
	PYTHONFAULTHANDLER=1 \
	PYTHONUNBUFFERED=1 \
	PYTHONHASHSEED=random \
	# pip:
	PIP_NO_CACHE_DIR=off \
	PIP_DISABLE_PIP_VERSION_CHECK=on \
	PIP_DEFAULT_TIMEOUT=100 \
	# poetry:
	POETRY_VERSION=1.1.13 \
	POETRY_VIRTUALENVS_CREATE=false \
	POETRY_CACHE_DIR='/var/cache/pypoetry'

RUN apt-get update \
	&& apt-get -y install libpq-dev gcc

COPY pyproject.toml .
COPY poetry.lock .
RUN pip install "poetry==$POETRY_VERSION" && poetry --version \
	&& poetry install --no-dev

WORKDIR /folio_backend

# create user，避免檔案檔案都是 root 權限，導致有機會發生 injection
RUN adduser --disabled-password --no-create-home code
USER code
