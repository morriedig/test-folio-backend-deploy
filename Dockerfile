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

COPY ./folio_backend /folio_backend
COPY pyproject.toml poetry.lock /folio_backend/

# set work directory
WORKDIR /folio_backend
EXPOSE 8000

#adduser: 如果沒有 create user，這樣產生出來的檔案都會是 root 權限
RUN apt-get update \
    && apt-get -y install libpq-dev gcc
RUN pip install "poetry==$POETRY_VERSION" && poetry --version \
	&& poetry install \
	&& adduser --disabled-password --no-create-home code 

#用 user 可以指定使用者權限來寫入特定的 volume 
USER code
