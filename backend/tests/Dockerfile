FROM python:3

WORKDIR /app/

COPY ./pyproject.toml ./poetry.lock ./

RUN pip install poetry

RUN poetry install --with dev

ENV PYTHONPATH="/app/src/"

COPY ./src/ ./src/
COPY ./tests/ ./tests/

WORKDIR /app/tests/

CMD ["poetry", "run", "pytest"]
