# folio-backend

### Usage

```
pip install poetry
poetry install -no-dev
```

### Setup the Development Environment

1. We user [poetry](https://python-poetry.org/docs/) as a tool for dependency management and packaging in Python.

```
pip install poetry
poetry install
```

2. Enable pre-commit hooks

```
pre-commit install # linting for every commit
pre-commit install pre-push # run pytest before push
pre-commit install --hook-type commit-msg # commit message format checking
```
