FROM python:3 AS dependencies

WORKDIR /app/

RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

COPY ./pyproject.toml ./poetry.lock ./

RUN poetry install --without dev --with admin --no-root

FROM python:3 AS prod

WORKDIR /app/

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/src"

COPY --from=dependencies /app/.venv ./.venv/

COPY ./src/admin/ ./src/admin/
COPY ./src/common/ ./src/common/

WORKDIR /app/src/admin/

CMD ["python", "-u", "app.py", "migrate"]
