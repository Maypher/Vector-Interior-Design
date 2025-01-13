FROM python:3

WORKDIR /app/

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock ./

RUN poetry install --with dev,admin --no-root

ENV PYTHONPATH="/app/src/"

COPY ./src ./src
COPY ./tests ./tests

WORKDIR /

RUN mkdir -p storage/images/

WORKDIR /app/tests/

CMD ["poetry", "run", "pytest", "-rP"]
