# Python base (venv and user)
FROM python:3.10-slim AS base

# Install dependencies and dumb-init
RUN apt-get update && apt-get install -y build-essential curl dumb-init && rm -rf /var/lib/apt/lists/*

RUN useradd -m roboquote && \
    mkdir /app/ && \
    chown -R roboquote /app/
USER roboquote

# Install Poetry
ENV PATH="${PATH}:/home/roboquote/.local/bin"
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry config virtualenvs.in-project true

# Dependencies
WORKDIR /app/
COPY ./pyproject.toml ./poetry.lock /app/
RUN poetry install --no-interaction --no-ansi --no-root --only main


# Prod image (app and default config)
FROM python:3.10-slim as prod

COPY --from=base /usr/bin/dumb-init /usr/bin/
COPY --from=base /app /app

WORKDIR /app/

# User
RUN useradd -m roboquote && \
    chown -R roboquote /app/
USER roboquote

# App
COPY roboquote /app/roboquote
COPY static /app/static
COPY fonts /app/fonts
COPY web_templates /app/web_templates

# Default log level
ENV LOG_LEVEL=WARNING

# Expose and run app
EXPOSE 8080
CMD ["dumb-init", "/app/.venv/bin/gunicorn", "roboquote.web.app:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8080", "--log-file=-"]
