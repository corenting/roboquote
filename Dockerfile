# Python base (venv and user)
FROM python:3.13-slim AS base

# Install dumb-init
RUN apt-get update && apt-get install -y dumb-init

# Create user
RUN useradd -m roboquote && \
    mkdir /app/ && \
    chown -R roboquote /app/
USER roboquote

# Create a fake roboquote package to install dependencies
WORKDIR /app/
RUN mkdir /app/roboquote
COPY roboquote/__init__.py /app/roboquote/

# Install dependencies with poetry with only the needed files
COPY pyproject.toml poetry.lock README.md /app/
ENV CPPFLAGS=-I/usr/local/include/python3.13/ \
    PATH=/home/roboquote/.local/bin:$PATH
RUN /usr/local/bin/pip install --user .

# Prod image (app and default config)
FROM python:3.13-slim AS prod

COPY --from=base /home/roboquote/.local /home/roboquote/.local
COPY --from=base /usr/bin/dumb-init /usr/bin/

WORKDIR /app/

# User
RUN useradd -m roboquote && \
    chown -R roboquote /app/ && \
    chown -R roboquote /home/roboquote/
USER roboquote

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/home/roboquote/.local/bin:$PATH

# App
COPY roboquote /app/roboquote
COPY static /app/static
COPY fonts /app/fonts
COPY web_templates /app/web_templates

# Default log level
ENV LOG_LEVEL=WARNING

# Expose and run app
EXPOSE 8080
ENTRYPOINT ["dumb-init", "--"]
CMD ["uvicorn", "roboquote.web.app:app", "--workers", "2", "--host", "0.0.0.0", "--port", "8080"]
