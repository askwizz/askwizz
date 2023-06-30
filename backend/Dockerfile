# syntax=docker/dockerfile:1

FROM python:3.11-slim
WORKDIR /app
ENV POETRY_VIRTUALENVS_CREATE=0

# system deps
RUN pip install "poetry==1.5.0"

# project deps
ADD ./pyproject.toml ./poetry.lock /app/
RUN poetry install --only main --no-root

# project
ADD . /app/
RUN poetry install --only-root

ENTRYPOINT ["poetry", "run", "uvicorn", "esearch.api.app:create_app", "--factory", "--host", "0.0.0.0"]
