FROM python:3-alpine AS dependencies

RUN pip install poetry

WORKDIR /app/

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

COPY ./pyproject.toml ./poetry.lock ./

RUN poetry install --without dev --without admin --no-root

FROM python:3-alpine AS prod

WORKDIR /app/

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/src"

# I know Docker doesn't require venv but poetry does it this way so.
COPY --from=dependencies /app/.venv ./.venv/

COPY ./src/user/ ./src/user/
COPY ./src/common/ ./src/common/

WORKDIR /app/src/user/


RUN chmod +x entrypoint.sh

EXPOSE 80
ENTRYPOINT [ "./entrypoint.sh" ]
